"""
고급 인사이트 생성 모듈

계산 기반으로 구체적이고 실행 가능한 재정 인사이트를 생성합니다.
AI 없이도 동작하는 규칙 기반 인사이트 시스템입니다.
"""

from typing import Dict, Any, List, Tuple
from modules.calculations import (
    calculate_retirement_goal,
    calculate_future_assets,
    apply_inflation,
)
from modules.formatters import format_currency, format_percentage


def generate_actionable_insights(
    inputs: Dict[str, Any],
    calculation_results: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    실행 가능한 인사이트 목록 생성

    Args:
        inputs: 입력 데이터 딕셔너리
        calculation_results: 계산 결과 딕셔너리

    Returns:
        List[Dict[str, Any]]: 인사이트 목록
            - title: 인사이트 제목
            - priority: 우선순위 (high, medium, low)
            - category: 카테고리 (debt, savings, investment, etc.)
            - message: 인사이트 메시지
            - action_items: 실행 가능한 항목 리스트
            - simulations: 시뮬레이션 결과 (있는 경우)
    """
    insights = []

    # 부채 분석 인사이트
    debt_insights = _analyze_debt_situation(inputs, calculation_results)
    insights.extend(debt_insights)

    # 저축 및 투자 인사이트
    savings_insights = _analyze_savings_and_investment(inputs, calculation_results)
    insights.extend(savings_insights)

    # 은퇴 준비도 인사이트
    retirement_insights = _analyze_retirement_readiness(inputs, calculation_results)
    insights.extend(retirement_insights)

    # 비상금 인사이트
    emergency_insights = _analyze_emergency_fund(inputs, calculation_results)
    insights.extend(emergency_insights)

    # 우선순위별 정렬 (high > medium > low)
    priority_order = {"high": 0, "medium": 1, "low": 2}
    insights.sort(key=lambda x: priority_order.get(x["priority"], 99))

    return insights


def _analyze_debt_situation(
    inputs: Dict[str, Any], calculation_results: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """부채 상황 분석 (대출 항목별 상세 정보 반영)"""
    insights = []

    total_assets = inputs.get("total_assets", 0)
    total_debt = inputs.get("total_debt", 0)
    debt_items = inputs.get("debt_items", [])

    if total_debt <= 0:
        return insights

    # 활성 대출만 필터링 (기간이 지나지 않은 대출)
    active_debt_items = [
        item
        for item in debt_items
        if item.get("remaining_months", 0) > 0 or item.get("remaining_months") is None
    ]

    # 자산 대비 부채 비율
    if total_assets > 0:
        debt_ratio = (total_debt / total_assets) * 100
    else:
        debt_ratio = 100

    monthly_savings = calculation_results.get("monthly_savings", 0)
    total_monthly_debt_payment = sum(
        item.get("monthly_payment", 0) for item in active_debt_items
    )

    # 대출이 끝난 후 저축 가능액 계산
    savings_after_debt_paid = (
        monthly_savings + total_monthly_debt_payment
        if total_monthly_debt_payment > 0
        else monthly_savings
    )

    action_items = []
    simulations = []

    # 대출 항목별 상세 분석
    if active_debt_items:
        # 가장 긴 대출 기간 찾기
        max_remaining_months = max(
            item.get("remaining_months", 0) or 0 for item in active_debt_items
        )
        max_remaining_years = (
            max_remaining_months / 12 if max_remaining_months > 0 else 0
        )

        # 전세자금 대출 여부 확인
        jeonse_loans = [
            item for item in active_debt_items if item.get("is_jeonse", False)
        ]

        # 만기 원금 상환 대출 확인
        principal_only_loans = [
            item
            for item in active_debt_items
            if item.get("repayment_type") == "만기 원금 상환"
            or item.get("is_jeonse", False)
        ]

        # 부채 비율이 높은 경우
        if debt_ratio > 60:
            if monthly_savings > 0:
                # 현재 패턴 유지 시 상환 기간 (실제 대출 만료 기간과 비교)
                if principal_only_loans:
                    # 만기 원금 상환 대출이 있으면, 만기 시점까지는 이자만 상환
                    principal_total = sum(
                        item.get("principal", 0) for item in principal_only_loans
                    )
                    years_to_payoff_principal = (
                        max_remaining_years
                        if max_remaining_years > 0
                        else (principal_total / monthly_savings / 12)
                    )
                else:
                    # 원리금 상환만 있으면 일반 상환 계산
                    years_to_payoff_principal = (
                        total_debt / monthly_savings / 12 if monthly_savings > 0 else 0
                    )

                simulations.append(
                    {
                        "scenario": "대출 끝나기 전 (현재)",
                        "years": 0,
                        "description": f"현재 월 저축 가능액: {format_currency(monthly_savings)} (대출 상환액 {format_currency(total_monthly_debt_payment)} 포함)",
                    }
                )

                if max_remaining_years > 0:
                    simulations.append(
                        {
                            "scenario": f"대출 끝난 후 ({max_remaining_years:.1f}년 후)",
                            "years": max_remaining_years,
                            "description": f"대출 만료 후 월 저축 가능액: {format_currency(savings_after_debt_paid)} ({format_currency(total_monthly_debt_payment)} 증가)",
                        }
                    )

                    if savings_after_debt_paid > monthly_savings:
                        action_items.append(
                            f"대출이 끝나면 월 저축 가능액이 {format_currency(total_monthly_debt_payment)} 증가하여 "
                            f"{format_currency(savings_after_debt_paid)}가 됩니다"
                        )

            # 전세자금 대출이 있는 경우 별도 인사이트
            if jeonse_loans:
                jeonse_total = sum(item.get("principal", 0) for item in jeonse_loans)
                jeonse_max_months = max(
                    item.get("remaining_months", 0) or 0 for item in jeonse_loans
                )

                # 전세자금 대출은 보증금 반환으로 상환되므로 별도 적립 불필요
                # 하지만 이자 납입은 필요
                monthly_jeonse_interest = sum(
                    item.get("monthly_payment", 0) for item in jeonse_loans
                )

                insights.append(
                    {
                        "title": "🏠 전세자금 대출 정보",
                        "priority": "medium",
                        "category": "debt",
                        "message": (
                            f"전세자금 대출 {format_currency(jeonse_total)}가 있습니다. "
                            f"전세자금 대출은 나갈 때 집주인이 돌려주는 보증금으로 원금이 상환되므로, "
                            f"원금 상환을 위한 별도 자금 마련은 필요하지 않습니다. "
                            f"다만 월 이자 {format_currency(monthly_jeonse_interest)}는 계속 납입해야 합니다."
                        ),
                        "action_items": [
                            f"월 이자 {format_currency(monthly_jeonse_interest)} 납입 계획 유지",
                            f"대출 만료 후 월 저축 가능액이 {format_currency(total_monthly_debt_payment)} 증가하여 "
                            f"{format_currency(savings_after_debt_paid)}가 됩니다",
                        ],
                        "simulations": [],
                    }
                )

            insights.append(
                {
                    "title": f"⚠️ 부채 비율이 {debt_ratio:.1f}%로 높습니다",
                    "priority": "high",
                    "category": "debt",
                    "message": (
                        f"총 부채가 {format_currency(total_debt)}로 자산의 {debt_ratio:.1f}%를 차지하고 있습니다. "
                        f"부채 비율이 60%를 초과하면 재정 위험이 높아집니다. "
                        f"현재 월 대출 상환액은 {format_currency(total_monthly_debt_payment)}입니다."
                    ),
                    "action_items": action_items,
                    "simulations": simulations,
                }
            )
        elif debt_ratio > 40:
            insights.append(
                {
                    "title": f"📊 부채 비율이 {debt_ratio:.1f}%입니다",
                    "priority": "medium",
                    "category": "debt",
                    "message": (
                        f"부채 비율이 {debt_ratio:.1f}%로 적정 수준을 넘었습니다. "
                        f"부채 상환을 통해 재정 안정성을 높이는 것을 권장합니다. "
                    ),
                    "action_items": (
                        [
                            "월 저축액의 일부를 부채 상환에 활용",
                            f"대출이 끝나면 월 저축 가능액이 {format_currency(total_monthly_debt_payment)} 증가할 예정입니다",
                        ]
                        if total_monthly_debt_payment > 0
                        else ["월 저축액의 일부를 부채 상환에 활용"]
                    ),
                    "simulations": [],
                }
            )

        # 대출 끝난 후 저축 가능액 인사이트
        if total_monthly_debt_payment > 0 and savings_after_debt_paid > monthly_savings:
            if max_remaining_months > 0:
                years = max_remaining_months // 12
                months = max_remaining_months % 12
                remaining_period = (
                    f"{years}년 {months}개월" if years > 0 else f"{months}개월"
                )

                insights.append(
                    {
                        "title": "💡 대출 만료 후 저축 가능액 증가",
                        "priority": "medium",
                        "category": "debt",
                        "message": (
                            f"가장 긴 대출이 {remaining_period} 후에 끝나면, "
                            f"월 저축 가능액이 {format_currency(monthly_savings)}에서 "
                            f"{format_currency(savings_after_debt_paid)}로 {format_currency(total_monthly_debt_payment)} 증가합니다."
                        ),
                        "action_items": [
                            f"대출 만료 후 추가 저축액({format_currency(total_monthly_debt_payment)}) 활용 계획 수립",
                            "퇴직 자금 또는 투자 계획에 반영",
                        ],
                        "simulations": [],
                    }
                )

    return insights


def _analyze_savings_and_investment(
    inputs: Dict[str, Any], calculation_results: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """저축 및 투자 분석"""
    insights = []

    monthly_savings = calculation_results.get("monthly_savings", 0)

    if monthly_savings <= 0:
        # 저축 여유가 없는 경우
        insights.append(
            {
                "title": "⚠️ 월 저축 가능액이 없습니다",
                "priority": "high",
                "category": "savings",
                "message": "현재 소득 대비 지출로 인해 월 저축이 불가능한 상황입니다. 지출을 줄이거나 소득을 늘리는 것이 필요합니다.",
                "action_items": [
                    "고정비 검토 및 최적화",
                    "변동비 절감 (외식, 쇼핑 등)",
                    "부수입 창출 고려",
                ],
                "simulations": [],
            }
        )
        return insights

    # 여유 자금 투자 시나리오
    if monthly_savings > 50:  # 월 50만원 이상 여유가 있는 경우
        current_age = inputs.get("current_age", 30)
        retirement_age = inputs.get("retirement_age", 60)
        years_to_retirement = retirement_age - current_age

        if years_to_retirement > 0:
            # 다양한 수익률 시나리오
            return_scenarios = [3.0, 5.0, 7.0, 10.0]  # CMA, 채권, 주식, 고위험 투자
            simulations = []

            current_assets = inputs.get("total_assets", 0)
            inflation_rate = inputs.get("inflation_rate", 2.5)

            for return_rate in return_scenarios:
                # 현재 자산과 월 저축액으로 은퇴 시점 자산 계산
                result = calculate_retirement_goal(
                    inputs,
                    monthly_savings,
                    return_rate,
                    4.0,  # withdrawal_rate
                )

                projected_assets = result.get("projected_assets", 0)

                # 인플레이션 반영하여 실질 가치 계산
                real_value = projected_assets / (
                    (1 + inflation_rate / 100) ** years_to_retirement
                )

                scenarios = {
                    3.0: "CMA/예금",
                    5.0: "채권/안정형 펀드",
                    7.0: "주식/혼합형 펀드",
                    10.0: "고위험 고수익 투자",
                }

                simulations.append(
                    {
                        "return_rate": return_rate,
                        "scenario": scenarios.get(return_rate, f"{return_rate}% 투자"),
                        "projected_assets": projected_assets,
                        "real_value": real_value,
                        "description": (
                            f"월 {format_currency(monthly_savings)}을 {return_rate}% 수익률로 투자 시 "
                            f"은퇴 시점 {format_currency(projected_assets)} 예상 (실질 가치: {format_currency(real_value)})"
                        ),
                    }
                )

            # 현재 패턴 (저축만, 수익률 0%)과 비교
            result_current = calculate_retirement_goal(
                inputs, monthly_savings, 0.0, 4.0
            )
            projected_current = result_current.get("projected_assets", 0)

            insights.append(
                {
                    "title": f"💰 월 {format_currency(monthly_savings)} 여유 자금 투자 시나리오",
                    "priority": "medium",
                    "category": "investment",
                    "message": (
                        f"현재 월 {format_currency(monthly_savings)}의 여유 자금이 있습니다. "
                        f"이를 투자에 활용하면 은퇴 시점 자산을 크게 늘릴 수 있습니다."
                    ),
                    "action_items": [
                        "위험 성향에 맞는 투자 상품 선택",
                        "장기 투자 전략 수립",
                        "다양한 자산 배분으로 리스크 분산",
                    ],
                    "simulations": simulations,
                    "baseline": {
                        "description": f"현재 패턴 유지 (저축만): {format_currency(projected_current)}",
                        "value": projected_current,
                    },
                }
            )

    return insights


def _analyze_retirement_readiness(
    inputs: Dict[str, Any], calculation_results: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """은퇴 준비도 분석"""
    insights = []

    # 은퇴 목표 계산 결과가 있다면 분석
    if "retirement_goal" in calculation_results:
        goal_result = calculation_results["retirement_goal"]
        is_achievable = goal_result.get("is_achievable", False)

        if not is_achievable:
            shortfall = goal_result.get("shortfall", 0)
            monthly_contribution = goal_result.get("monthly_contribution", 0)
            annual_return_rate = goal_result.get("annual_return_rate", 0)

            insights.append(
                {
                    "title": "🎯 은퇴 자금 목표 미달",
                    "priority": "high",
                    "category": "retirement",
                    "message": (
                        f"현재 계획으로는 은퇴 자금 목표에 {format_currency(shortfall)} 부족합니다. "
                        f"저축 금액을 늘리거나 투자 수익률을 높이는 것이 필요합니다."
                    ),
                    "action_items": [
                        f"월 저축액을 늘려 목표 달성",
                        f"투자 수익률 개선 ({annual_return_rate}% → 높은 수익률)",
                        "은퇴 나이 조정 검토",
                    ],
                    "simulations": [],
                }
            )

    return insights


def _analyze_emergency_fund(
    inputs: Dict[str, Any], calculation_results: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """비상금 분석"""
    insights = []

    if "grade" in calculation_results:
        grade_result = calculation_results["grade"]
        emergency_months = grade_result.get("emergency_fund_months", 0)

        if emergency_months < 3:
            # 기존 필드 호환성
            if (
                "monthly_fixed_expense" in inputs
                and "monthly_variable_expense" in inputs
            ):
                monthly_expense = inputs.get("monthly_fixed_expense", 0) + inputs.get(
                    "monthly_variable_expense", 0
                )
            else:
                monthly_expense = inputs.get("monthly_expense", 0)

            target_months = 6  # 권장 기준
            target_amount = monthly_expense * target_months
            current_amount = (
                monthly_expense * emergency_months if emergency_months > 0 else 0
            )
            needed_amount = target_amount - current_amount

            insights.append(
                {
                    "title": f"⚠️ 비상금이 {emergency_months:.1f}개월치로 부족합니다",
                    "priority": "high" if emergency_months < 1 else "medium",
                    "category": "emergency_fund",
                    "message": (
                        f"현재 비상금이 {emergency_months:.1f}개월치 생활비 수준입니다. "
                        f"권장 기준인 6개월치를 준비하려면 추가로 {format_currency(needed_amount)}가 필요합니다."
                    ),
                    "action_items": [
                        f"월 저축액을 비상금으로 우선 적립하여 {target_months}개월치 목표 달성",
                        "비상금은 유동성이 높은 상품(예금, CMA)에 보관",
                    ],
                    "simulations": [],
                }
            )

    return insights
