"""
시각화 모듈

Plotly를 사용하여 데이터 시각화 차트를 생성합니다.
"""

from typing import Dict, Any, List, Optional

try:
    import plotly.graph_objects as go
    import plotly.express as px
except ImportError:
    # 테스트 환경에서 plotly가 없을 경우를 대비
    class MockFigure:
        def __init__(self, *args, **kwargs):
            self.data = []
            self.layout = {}
            # add_trace로 추가된 데이터를 저장
            if args:
                self.data.append(args[0])

        def add_trace(self, *args, **kwargs):
            if args:
                self.data.append(args[0])
            elif "trace" in kwargs:
                self.data.append(kwargs["trace"])

        def update_layout(self, *args, **kwargs):
            self.layout.update(kwargs)

        def add_annotation(self, *args, **kwargs):
            pass

        def add_hline(self, *args, **kwargs):
            pass

    class MockGo:
        class Scatter:
            def __init__(self, *args, **kwargs):
                pass

        class Bar:
            def __init__(self, *args, **kwargs):
                pass

        class Indicator:
            def __init__(self, *args, **kwargs):
                pass

        def __init__(self):
            self.Figure = MockFigure
            self.Scatter = self.Scatter
            self.Bar = self.Bar
            self.Indicator = self.Indicator

    go = MockGo()


def create_future_assets_chart(
    future_assets_result: Dict[str, Any], current_age: int = None
) -> go.Figure:
    """
    미래 자산 추정 차트 생성

    Args:
        future_assets_result: 미래 자산 추정 결과
        current_age: 현재 나이 (나이 축 표시용)

    Returns:
        go.Figure: Plotly 그래프 객체
    """
    yearly_breakdown = future_assets_result.get("yearly_breakdown", [])

    if not yearly_breakdown:
        # 빈 차트 반환
        fig = go.Figure()
        fig.add_annotation(
            text="데이터가 없습니다",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        return fig

    # 나이 축 사용 여부 결정
    use_age_axis = current_age is not None and current_age > 0

    if use_age_axis:
        # 나이와 자산 추출 (yearly_breakdown에 age 정보가 있으면 사용)
        if yearly_breakdown and "age" in yearly_breakdown[0]:
            ages = [current_age] + [item["age"] for item in yearly_breakdown]
        else:
            ages = [current_age] + [
                current_age + item["year"] for item in yearly_breakdown
            ]
        assets = [future_assets_result.get("current_assets", 0)] + [
            item["assets"] for item in yearly_breakdown
        ]
        x_data = ages
        x_title = "나이 (세)"
        hovertemplate = "%{x}세: %{y:,.0f}만원<extra></extra>"
    else:
        # 연도와 자산 추출 (하위 호환성)
        years = [0] + [item["year"] for item in yearly_breakdown]
        assets = [future_assets_result.get("current_assets", 0)] + [
            item["assets"] for item in yearly_breakdown
        ]
        x_data = years
        x_title = "연도"
        hovertemplate = "%{x}년: %{y:,.0f}만원<extra></extra>"

    fig = go.Figure()

    # 은퇴 전/후 구분하여 표시
    if use_age_axis and yearly_breakdown and "is_retired" in yearly_breakdown[0]:
        # 은퇴 전 구간
        pre_retirement_ages = [current_age]
        pre_retirement_assets = [future_assets_result.get("current_assets", 0)]
        retirement_age = None

        for item in yearly_breakdown:
            if not item.get("is_retired", False):
                if "age" in item:
                    pre_retirement_ages.append(item["age"])
                else:
                    pre_retirement_ages.append(current_age + item["year"])
                pre_retirement_assets.append(item["assets"])
            else:
                if retirement_age is None:
                    # 은퇴 직전 나이 찾기
                    if "age" in item:
                        retirement_age = item["age"] - 1
                    else:
                        retirement_age = current_age + item["year"] - 1
                    pre_retirement_ages.append(retirement_age)
                    # 은퇴 직전 자산 찾기
                    if len(pre_retirement_assets) > 0:
                        pre_retirement_assets.append(pre_retirement_assets[-1])
                break

        # 은퇴 후 구간
        post_retirement_ages = []
        post_retirement_assets = []
        for item in yearly_breakdown:
            if item.get("is_retired", False):
                if "age" in item:
                    post_retirement_ages.append(item["age"])
                else:
                    post_retirement_ages.append(current_age + item["year"])
                post_retirement_assets.append(item["assets"])

        # 은퇴 전 구간
        if len(pre_retirement_ages) > 1:
            fig.add_trace(
                go.Scatter(
                    x=pre_retirement_ages,
                    y=pre_retirement_assets,
                    mode="lines+markers",
                    name="은퇴 전",
                    line=dict(color="#1f77b4", width=3),
                    marker=dict(size=8),
                    hovertemplate="%{x}세: %{y:,.0f}만원<extra></extra>",
                )
            )

        # 은퇴 후 구간
        if post_retirement_ages:
            fig.add_trace(
                go.Scatter(
                    x=post_retirement_ages,
                    y=post_retirement_assets,
                    mode="lines+markers",
                    name="은퇴 후",
                    line=dict(color="#d62728", width=3),
                    marker=dict(size=8),
                    hovertemplate="%{x}세: %{y:,.0f}만원<extra></extra>",
                )
            )

        # 은퇴 시점 수직선 표시
        if retirement_age:
            fig.add_vline(
                x=retirement_age + 1,
                line_dash="dash",
                line_color="gray",
                annotation_text="은퇴",
                annotation_position="top",
            )
    else:
        # 기존 방식 (은퇴 전/후 구분 없음)
        fig.add_trace(
            go.Scatter(
                x=x_data,
                y=assets,
                mode="lines+markers",
                name="예상 자산",
                line=dict(color="#1f77b4", width=3),
                marker=dict(size=8),
                hovertemplate=hovertemplate,
            )
        )

    fig.update_layout(
        title="나이별 자산 변화 추이" if use_age_axis else "연도별 자산 변화 추이",
        xaxis_title=x_title,
        yaxis_title="자산 (만원)",
        hovermode="x unified",
        template="plotly_white",
        height=400,
        showlegend=use_age_axis
        and yearly_breakdown
        and "is_retired" in yearly_breakdown[0],
    )

    return fig


def create_financial_health_gauge(grade_result: Dict[str, Any]) -> go.Figure:
    """
    재정 건전성 등급 게이지 차트 생성

    Args:
        grade_result: 재정 건전성 등급 결과

    Returns:
        go.Figure: Plotly 그래프 객체
    """
    grade = grade_result.get("grade", "D")

    # 등급별 값 매핑
    grade_values = {"A+": 100, "A": 80, "B": 60, "C": 40, "D": 20}

    value = grade_values.get(grade, 20)

    # 등급별 색상
    grade_colors = {
        "A+": "green",
        "A": "lightgreen",
        "B": "yellow",
        "C": "orange",
        "D": "red",
    }

    color = grade_colors.get(grade, "red")

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": f"재정 건전성 등급: {grade}"},
            delta={"reference": 50},
            gauge={
                "axis": {"range": [None, 100]},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, 20], "color": "lightgray"},
                    {"range": [20, 40], "color": "gray"},
                    {"range": [40, 60], "color": "lightyellow"},
                    {"range": [60, 80], "color": "lightgreen"},
                    {"range": [80, 100], "color": "green"},
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 50,
                },
            },
        )
    )

    fig.update_layout(height=300)

    return fig


def create_risk_score_chart(risk_result: Dict[str, Any]) -> go.Figure:
    """
    위험도 점수 차트 생성

    Args:
        risk_result: 위험도 점수 결과

    Returns:
        go.Figure: Plotly 그래프 객체
    """
    total_score = risk_result.get("total_score", 0)
    breakdown = risk_result.get("breakdown", {})

    # 게이지 차트
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=total_score,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": f"위험도 점수: {total_score}점"},
            gauge={
                "axis": {"range": [None, 100]},
                "bar": {
                    "color": (
                        "darkred"
                        if total_score >= 75
                        else (
                            "orange"
                            if total_score >= 50
                            else "yellow" if total_score >= 25 else "green"
                        )
                    )
                },
                "steps": [
                    {"range": [0, 25], "color": "lightgreen"},
                    {"range": [25, 50], "color": "lightyellow"},
                    {"range": [50, 75], "color": "lightcoral"},
                    {"range": [75, 100], "color": "lightgray"},
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 50,
                },
            },
        )
    )

    fig.update_layout(height=300)

    return fig


def create_risk_breakdown_chart(risk_result: Dict[str, Any]) -> go.Figure:
    """
    위험도 점수 세부 항목 막대 그래프

    Args:
        risk_result: 위험도 점수 결과

    Returns:
        go.Figure: Plotly 그래프 객체
    """
    breakdown = risk_result.get("breakdown", {})

    categories = list(breakdown.keys())
    values = list(breakdown.values())

    # 카테고리 한글 변환
    category_names = {
        "income_interruption": "소득 중단",
        "debt_ratio": "부채 비율",
        "expense_ratio": "지출 비율",
        "retirement_readiness": "은퇴 준비도",
    }

    labels = [category_names.get(cat, cat) for cat in categories]

    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                marker_color=[
                    "#d62728" if v > 20 else "#ff7f0e" if v > 10 else "#2ca02c"
                    for v in values
                ],
                text=values,
                textposition="auto",
            )
        ]
    )

    fig.update_layout(
        title="위험도 점수 세부 항목",
        xaxis_title="항목",
        yaxis_title="점수",
        yaxis_range=[0, 50],
        height=300,
        template="plotly_white",
    )

    return fig


def create_scenario_comparison_chart(comparison_result: Dict[str, Any]) -> go.Figure:
    """
    시나리오 비교 차트 생성

    Args:
        comparison_result: 시나리오 비교 결과

    Returns:
        go.Figure: Plotly 그래프 객체
    """
    fig = go.Figure()

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

    # 기본 시나리오
    base_scenario = comparison_result.get("base_scenario", {})
    base_breakdown = base_scenario.get("yearly_breakdown", [])

    if base_breakdown:
        years = [0] + [item["year"] for item in base_breakdown]
        assets = [base_scenario.get("current_assets", 0)] + [
            item["assets"] for item in base_breakdown
        ]

        fig.add_trace(
            go.Scatter(
                x=years,
                y=assets,
                mode="lines+markers",
                name="현재 패턴 유지",
                line=dict(color="#1f77b4", width=3, dash="dash"),
                marker=dict(size=8),
            )
        )

    # 각 시나리오
    scenarios = comparison_result.get("scenarios", [])
    for i, scenario_data in enumerate(scenarios):
        scenario_name = scenario_data.get("scenario_name", f"시나리오 {i+1}")
        yearly_breakdown = scenario_data.get("yearly_breakdown", [])

        if yearly_breakdown:
            years = [0] + [item["year"] for item in yearly_breakdown]
            assets = [scenario_data.get("current_assets", 0)] + [
                item["assets"] for item in yearly_breakdown
            ]

            fig.add_trace(
                go.Scatter(
                    x=years,
                    y=assets,
                    mode="lines+markers",
                    name=scenario_name,
                    line=dict(color=colors[(i + 1) % len(colors)], width=2),
                    marker=dict(size=6),
                )
            )

    fig.update_layout(
        title="시나리오별 자산 변화 비교",
        xaxis_title="연도",
        yaxis_title="자산 (만원)",
        hovermode="x unified",
        template="plotly_white",
        height=500,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    )

    return fig


def create_survival_chart(income_interruption_result: Dict[str, Any]) -> go.Figure:
    """
    소득 중단 생존 기간 차트 생성

    Args:
        income_interruption_result: 소득 중단 생존 기간 결과

    Returns:
        go.Figure: Plotly 그래프 객체
    """
    survival_months = income_interruption_result.get("survival_months", 0)
    status = income_interruption_result.get("status", "danger")

    # 상태별 색상
    status_colors = {"safe": "green", "warning": "orange", "danger": "red"}

    color = status_colors.get(status, "red")

    # 권장 기준선 (6개월)
    recommended_months = 6

    fig = go.Figure()

    # 생존 가능 개월 막대
    fig.add_trace(
        go.Bar(
            x=["생존 가능 기간"],
            y=[survival_months],
            name="생존 가능 개월",
            marker_color=color,
            text=f"{survival_months:.1f}개월",
            textposition="auto",
        )
    )

    # 권장 기준선
    fig.add_hline(
        y=recommended_months,
        line_dash="dash",
        line_color="blue",
        annotation_text="권장 기준 (6개월)",
        annotation_position="right",
    )

    fig.update_layout(
        title="소득 중단 시 생존 가능 기간",
        yaxis_title="개월",
        height=300,
        template="plotly_white",
        showlegend=False,
    )

    return fig


def create_retirement_goal_chart(
    inputs: Dict[str, Any],
    current_monthly_contribution: float,
    current_return_rate: float,
    withdrawal_rate: float = 4.0,
) -> go.Figure:
    """
    은퇴 자금 목표 달성을 위한 수익률 vs 저축 금액 관계 그래프

    Args:
        inputs: 입력 데이터 딕셔너리
        current_monthly_contribution: 현재 선택한 매달 저축 금액
        current_return_rate: 현재 선택한 수익률
        withdrawal_rate: 현금화율

    Returns:
        go.Figure: Plotly 그래프 객체
    """
    from modules.calculations import (
        find_required_return_rate,
        find_optimal_contribution_rate,
    )

    # 여러 저축 금액에 대한 필요한 수익률 계산 (원 단위)
    contribution_scenarios = list(
        range(500000, 5000001, 500000)
    )  # 50만원부터 500만원까지 50만원 단위 (원 단위)
    required_rates = []
    achievable_flags = []

    for contrib in contribution_scenarios:
        required_rate, result = find_required_return_rate(
            inputs, contrib, withdrawal_rate
        )  # contrib는 원 단위
        required_rates.append(min(15.0, required_rate))  # 최대 15%로 제한
        achievable_flags.append(result.get("is_achievable", False) if result else False)

    # 그래프 생성
    fig = go.Figure()

    # 달성 가능한 영역과 불가능한 영역 구분
    achievable_contributions = [
        contrib
        for contrib, achievable in zip(contribution_scenarios, achievable_flags)
        if achievable
    ]
    achievable_rates = [
        rate for rate, achievable in zip(required_rates, achievable_flags) if achievable
    ]
    unachievable_contributions = [
        contrib
        for contrib, achievable in zip(contribution_scenarios, achievable_flags)
        if not achievable
    ]
    unachievable_rates = [
        rate
        for rate, achievable in zip(required_rates, achievable_flags)
        if not achievable
    ]

    # 달성 가능한 영역 (표시는 만원 단위로 변환)
    if achievable_contributions:
        fig.add_trace(
            go.Scatter(
                x=[c / 10000 for c in achievable_contributions],  # 만원 단위로 표시
                y=achievable_rates,
                mode="lines+markers",
                name="목표 달성 가능",
                line=dict(color="green", width=3),
                marker=dict(size=8, color="green"),
                fill="tozeroy",
                fillcolor="rgba(0, 255, 0, 0.1)",
            )
        )

    # 달성 불가능한 영역 (표시는 만원 단위로 변환)
    if unachievable_contributions:
        fig.add_trace(
            go.Scatter(
                x=[c / 10000 for c in unachievable_contributions],  # 만원 단위로 표시
                y=unachievable_rates,
                mode="lines+markers",
                name="목표 달성 어려움",
                line=dict(color="red", width=2, dash="dash"),
                marker=dict(size=6, color="red"),
            )
        )

    # 현재 선택한 값 표시 (원 단위로 전달, 만원 단위로 표시)
    current_required_rate, _ = find_required_return_rate(
        inputs, current_monthly_contribution, withdrawal_rate
    )
    current_required_rate = min(15.0, current_required_rate)

    # current_monthly_contribution은 원 단위이므로 만원 단위로 변환하여 표시
    current_monthly_contribution_manwon = current_monthly_contribution / 10000

    fig.add_trace(
        go.Scatter(
            x=[current_monthly_contribution_manwon],  # 만원 단위로 표시
            y=[current_return_rate],
            mode="markers",
            name="현재 선택",
            marker=dict(
                size=15,
                color="blue",
                symbol="star",
                line=dict(width=2, color="darkblue"),
            ),
            hovertemplate="<b>현재 선택</b><br>"
            + "저축 금액: %{x:,.0f}만원<br>"
            + "수익률: %{y:.2f}%<extra></extra>",
        )
    )

    # 목표 달성 기준선 (15% 수익률)
    fig.add_hline(
        y=15.0,
        line_dash="dot",
        line_color="gray",
        annotation_text="최대 수익률 (15%)",
        annotation_position="right",
    )

    fig.update_layout(
        title={
            "text": "저축 금액 vs 필요한 수익률 관계",
            "x": 0.5,
            "xanchor": "center",
        },
        xaxis_title="매달 저축 금액 (만원)",
        yaxis_title="필요한 연간 수익률 (%)",
        hovermode="closest",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        height=500,
    )

    return fig
