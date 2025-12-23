"""
페이지 1: 소득 지출 분석

미래 자산 추정, 재정 건전성 등급, 월 저축 가능 금액 등을 표시합니다.
"""

import streamlit as st
from shared.session_manager import init_session_state
from shared.page_input_form import render_page_input_form, check_inputs_complete
from modules.validators import validate_inputs, validate_logical_consistency
from modules.calculations import (
    calculate_future_assets,
    calculate_financial_health_grade,
    calculate_monthly_savings,
    calculate_retirement_goal,
    find_optimal_contribution_rate,
    find_required_return_rate
)
from modules.formatters import (
    format_currency,
    format_percentage,
    generate_future_assets_insight,
    generate_financial_health_insight
)
from modules.visualizations import (
    create_future_assets_chart,
    create_financial_health_gauge,
    create_retirement_goal_chart
)
from modules.download import (
    create_json_download,
    get_download_filename
)
from modules.utils import (
    safe_calculate,
    validate_calculation_inputs
)

# 페이지 설정
st.set_page_config(
    page_title="소득 지출 분석",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 페이지 네비게이션 사이드바 숨기기 (CSS)
st.markdown("""
<style>
    /* 페이지 네비게이션 사이드바 숨기기 */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    /* 메인 컨텐츠 영역 패딩 조정 */
    [data-testid="stAppViewContainer"] > div {
        padding-left: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
init_session_state()

# 메인 콘텐츠
st.title("📈 소득 지출 분석")
st.markdown("현재 소비 패턴을 기반으로 미래 자산을 예측하고 재정 건전성을 평가합니다.")
st.divider()

# 입력 폼 표시
required_fields = [
    'current_age', 'retirement_age', 'salary',
    'monthly_fixed_expense', 'monthly_variable_expense', 
    'total_assets', 'total_debt'
]
# 연봉 증가율은 기본값이 있으므로 필수 필드에서 제외

inputs = render_page_input_form("income", required_fields)

# 입력 완료 여부 확인
inputs_complete = check_inputs_complete(inputs, required_fields)

# 입력 검증
is_valid, errors = validate_inputs(inputs)
if not is_valid:
    st.error("⚠️ 입력 오류가 있습니다. 다음 항목을 확인해주세요:")
    for error in errors:
        st.error(f"- {error}")
    inputs_complete = False

# 논리적 일관성 검증 (경고)
warnings = validate_logical_consistency(inputs)
if warnings:
    st.warning("⚠️ 입력 경고:")
    for warning in warnings:
        st.warning(f"- {warning}")

st.divider()

# 시뮬레이션 버튼
if inputs_complete and is_valid:
    if st.button("🚀 시뮬레이션 실행", type="primary", use_container_width=True):
        # 시뮬레이션 버튼을 누르면 세션 상태에 저장
        st.session_state.calculation_done_income = True
    run_simulation = st.session_state.get('calculation_done_income', False)
else:
    st.info("💡 모든 필수 항목을 입력해주세요.")
    run_simulation = False
    st.session_state.calculation_done_income = False

st.divider()

# 계산 결과 표시 (시뮬레이션 버튼을 한 번 누르면 이후 슬라이더 변경 시에도 유지)
if run_simulation:
    # 계산 전 입력값 검증
    is_valid_calc, validation_error = validate_calculation_inputs(inputs)
    if not is_valid_calc:
        st.error(f"⚠️ {validation_error}")
        st.stop()
    
    # 계산 수행
    years_to_retirement = inputs['retirement_age'] - inputs['current_age']
    
    # 인플레이션율 가져오기 (기본값 2.5%)
    inflation_rate = inputs.get('inflation_rate', 2.5)
    
    # 미래 자산 추정 (은퇴 후 포함, 평균 수명까지)
    future_assets_result, success1, error1 = safe_calculate(
        calculate_future_assets,
        inputs,
        years_to_retirement,
        inflation_rate,
        True,  # include_post_retirement
        83,    # life_expectancy (한국 평균 기대수명)
        error_message="미래 자산 추정 중 오류가 발생했습니다."
    )
    
    if not success1:
        st.error(f"⚠️ {error1}")
        st.stop()
    
    # 재정 건전성 등급
    grade_result, success2, error2 = safe_calculate(
        calculate_financial_health_grade,
        inputs,
        error_message="재정 건전성 등급 계산 중 오류가 발생했습니다."
    )
    
    if not success2:
        st.error(f"⚠️ {error2}")
        st.stop()
    
    # 월 저축 가능액
    monthly_savings, success3, error3 = safe_calculate(
        calculate_monthly_savings,
        inputs,
        error_message="월 저축 가능액 계산 중 오류가 발생했습니다."
    )
    
    if not success3:
        st.error(f"⚠️ {error3}")
        st.stop()
    
    # 계산 완료 상태 저장
    st.session_state.calculation_done_income = True
    st.session_state.results_income = {
        'future_assets': future_assets_result,
        'grade': grade_result,
        'monthly_savings': monthly_savings
    }
    
    # 입력 데이터 요약
    st.header("📋 입력 데이터 요약")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("현재 나이", f"{inputs['current_age']}세")
        st.metric("은퇴 예정 나이", f"{inputs['retirement_age']}세")
    
    with col2:
        st.metric("연봉", format_currency(inputs['salary']))
        st.metric("연봉 증가율", format_percentage(inputs['salary_growth_rate']))
    
    with col3:
        # 기존 필드 호환성
        if 'monthly_fixed_expense' in inputs and 'monthly_variable_expense' in inputs:
            st.metric("월간 고정비", format_currency(inputs['monthly_fixed_expense']))
            st.metric("월간 변동비", format_currency(inputs['monthly_variable_expense']))
            monthly_total = inputs['monthly_fixed_expense'] + inputs['monthly_variable_expense']
            st.metric("총 월 지출", format_currency(monthly_total))
        else:
            st.metric("월 지출", format_currency(inputs.get('monthly_expense', 0)))
            st.metric("연간 고정 지출", format_currency(inputs.get('annual_fixed_expense', 0)))
    
    with col4:
        st.metric("총 자산", format_currency(inputs['total_assets']))
        st.metric("총 부채", format_currency(inputs['total_debt']))
    
    # 추가 설정 표시
    if 'inflation_rate' in inputs:
        st.info(f"📊 사용된 설정: 인플레이션율 {inputs.get('inflation_rate', 2.5):.1f}%")
    
    st.divider()
    
    # 결과 표시
    st.header("📊 계산 결과")
    
    # 주요 지표
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "미래 자산 (은퇴 시점)",
            format_currency(future_assets_result.get('future_assets', 0)),
            delta=format_currency(future_assets_result.get('future_assets', 0) - inputs['total_assets'])
        )
    
    with col2:
        st.metric(
            "재정 건전성 등급",
            grade_result.get('grade', 'D')
        )
    
    with col3:
        st.metric(
            "월 저축 가능액",
            format_currency(monthly_savings)
        )
    
    st.divider()
    
    # 시각화
    st.header("📊 시각화")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("나이별 자산 변화")
        chart = create_future_assets_chart(future_assets_result, current_age=inputs.get('current_age'))
        st.plotly_chart(chart, use_container_width=True)
    
    with col2:
        st.subheader("재정 건전성 등급")
        gauge = create_financial_health_gauge(grade_result)
        st.plotly_chart(gauge, use_container_width=True)
    
    st.divider()
    
    # 상세 정보
    st.header("📝 상세 정보")
    
    # 재정 건전성 상세
    st.subheader("재정 건전성 상세")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("소득 대비 지출 비율", format_percentage(grade_result.get('expense_ratio', 0)))
    
    with col2:
        st.metric("자산 대비 부채 비율", format_percentage(grade_result.get('debt_ratio', 0)))
    
    with col3:
        st.metric("비상금 지속 가능 개월", f"{grade_result.get('emergency_fund_months', 0):.1f}개월")
    
    with col4:
        st.metric("월 저축 가능액", format_currency(grade_result.get('monthly_savings', 0)))
    
    st.divider()
    
    # 인사이트
    st.header("💡 인사이트")
    
    # 미래 자산 인사이트
    future_insight = generate_future_assets_insight(future_assets_result)
    st.info(f"**미래 자산 분석**: {future_insight}")
    
    # 재정 건전성 인사이트
    health_insight = generate_financial_health_insight(grade_result)
    st.info(f"**재정 건전성 평가**: {health_insight}")
    
    st.divider()
    
    # 은퇴 자금 목표 계산 (시뮬레이션 버튼 클릭 후에만 표시)
    st.header("🎯 은퇴 자금 목표 계산")
    st.markdown("""
    은퇴 후 생활비와 의료비를 지속적으로 충당하기 위해 필요한 목표 자산을 계산합니다.
    다양한 저축 금액과 수익률 조합의 추이를 확인할 수 있습니다.
    
    **4% 현금화율 기준**: 은퇴 자산의 4%를 매년 인출하여 생활비로 사용하는 방식입니다.
    이는 자산이 지속적으로 유지되면서 생활비를 충당할 수 있는 안전한 비율로 알려져 있습니다.
    """)
    
    # 현재 저축 가능 금액 기준으로 필요한 수익률 먼저 계산
    default_monthly_contribution = max(50, int(monthly_savings / 50) * 50) if monthly_savings > 0 else 100
    
    # 초기 필요한 수익률 계산
    initial_required_rate, initial_result = find_required_return_rate(inputs, default_monthly_contribution, 4.0)
    initial_required_rate = max(0.0, min(15.0, initial_required_rate))  # 0-15% 범위로 제한
    
    # 인터랙티브 그래프 먼저 표시
    st.subheader("📈 저축 금액 vs 수익률 관계 그래프")
    st.markdown("**💡 그래프에서 초록색 영역은 목표 달성이 가능한 조합입니다. 슬라이더를 움직여 추이를 확인하세요.**")
    
    # 추이를 보여주는 슬라이더 (그래프와 연동)
    col_slider1, col_slider2 = st.columns(2)
    
    with col_slider1:
        monthly_contribution = st.slider(
            "매달 저축 금액 (만원)",
            min_value=50,
            max_value=500,
            value=default_monthly_contribution,
            step=50,
            help="저축 금액에 따른 필요한 수익률 추이를 확인하세요"
        )
    
    with col_slider2:
        annual_return_rate = st.slider(
            "연간 수익률 (%)",
            min_value=0.0,
            max_value=15.0,
            value=float(initial_required_rate),
            step=0.5,
            help="수익률에 따른 필요한 저축 금액 추이를 확인하세요"
        )
    
    # 그래프 표시
    retirement_chart = create_retirement_goal_chart(
        inputs,
        monthly_contribution,
        annual_return_rate,
        4.0
    )
    st.plotly_chart(retirement_chart, use_container_width=True)
    
    # 현재 선택한 값에 대한 계산 결과
    goal_result, success_goal, error_goal = safe_calculate(
        calculate_retirement_goal,
        inputs,
        monthly_contribution,
        annual_return_rate,
        4.0,
        error_message="은퇴 자금 목표 계산 중 오류가 발생했습니다."
    )
    
    if success_goal and goal_result:
        st.divider()
        
        # 목표 자산 정보 표시
        col_goal1, col_goal2, col_goal3, col_goal4 = st.columns(4)
        
        with col_goal1:
            st.metric(
                "목표 자산",
                format_currency(goal_result.get('target_assets', 0)),
                help="은퇴 후 생활비와 의료비를 지속적으로 충당하기 위해 필요한 자산"
            )
        
        with col_goal2:
            st.metric(
                "예상 자산",
                format_currency(goal_result.get('projected_assets', 0)),
                delta=format_currency(goal_result.get('projected_assets', 0) - goal_result.get('target_assets', 0)),
                delta_color="normal" if goal_result.get('is_achievable', False) else "inverse",
                help="현재 저축 계획으로 예상되는 은퇴 시점 자산"
            )
        
        with col_goal3:
            if goal_result.get('is_achievable', False):
                st.metric(
                    "여유 자산",
                    format_currency(goal_result.get('surplus', 0)),
                    delta_color="normal"
                )
            else:
                st.metric(
                    "부족 자산",
                    format_currency(goal_result.get('shortfall', 0)),
                    delta_color="inverse"
                )
        
        with col_goal4:
            st.metric(
                "은퇴까지 기간",
                f"{goal_result.get('years_to_retirement', 0)}년",
                help="현재 나이부터 은퇴 나이까지의 기간"
            )
        
        # 상세 정보
        col_detail1, col_detail2 = st.columns(2)
        
        with col_detail1:
            st.subheader("📊 계산 상세")
            st.markdown(f"""
            - **은퇴 시점 월 필요 금액**: {format_currency(goal_result.get('monthly_expense_at_retirement', 0))}
            - **연간 필요 금액**: {format_currency(goal_result.get('annual_expense_needed', 0))}
            - **현금화율**: {goal_result.get('withdrawal_rate', 4.0)}%
            - **현재 자산**: {format_currency(goal_result.get('current_assets', 0))}
            """)
        
        with col_detail2:
            st.subheader("💡 인사이트")
            if goal_result.get('is_achievable', False):
                st.success(f"""
                ✅ **목표 달성 가능**
                
                현재 계획으로는 은퇴 후 생활비를 충당할 수 있습니다.
                여유 자산이 {format_currency(goal_result.get('surplus', 0))}만큼 있습니다.
                """)
            else:
                st.warning(f"""
                ⚠️ **목표 달성 어려움**
                
                현재 계획으로는 목표 자산에 {format_currency(goal_result.get('shortfall', 0))} 부족합니다.
                
                **개선 방안**:
                - 매달 저축 금액을 늘리기
                - 투자 수익률을 높이기
                - 은퇴 나이를 늦추기
                """)
    
    else:
        st.error(f"⚠️ {error_goal}")
    
    st.divider()
    
    # 데이터 출처 및 면책 조항
    st.header("📚 데이터 출처 및 면책 조항")
    
    with st.expander("데이터 출처"):
        st.markdown("""
        ### 사용된 데이터 출처
        
        - **인플레이션**: 한국은행 경제통계시스템(ECOS) 기준 (사용자 입력 또는 기본값 2.5%)
        - **연봉 인상률**: 통계청 근로형태별 근로실태조사 기준 (연 3.0% 가정)
        - **재정 건전성 등급 기준**:
          - A+: 소득 대비 지출 < 50%, 비상금 6개월 이상, 부채 없음
          - A: 소득 대비 지출 < 60%, 비상금 3개월 이상, 부채 비율 < 20%
          - B: 소득 대비 지출 < 70%, 비상금 1개월 이상, 부채 비율 < 40%
          - C: 소득 대비 지출 < 80%, 부채 비율 < 60%
          - D: 그 외
        - **비상금 기준**: 6개월 생활비 권장 기준
        
        자세한 내용은 `docs/data_sources.md`를 참고하세요.
        """)
    
    st.warning("""
    **면책 조항**
    
    이 도구는 교육 및 참고 목적으로 제공됩니다. 실제 투자 및 재정 결정에 앞서 전문가의 조언을 구하시기 바랍니다.
    
    - 계산 결과는 입력 데이터와 가정에 기반한 추정치입니다.
    - 실제 경제 상황과 다를 수 있습니다.
    - 투자 손실에 대한 책임을 지지 않습니다.
    """)
    
    st.divider()
    
    # 결과 다운로드
    st.header("📥 결과 다운로드")
    
    # 다운로드 데이터 생성
    download_data = {
        'future_assets': future_assets_result,
        'grade': grade_result,
        'monthly_savings': monthly_savings
    }
    
    json_data = create_json_download(inputs, download_data, page_type="income")
    filename = get_download_filename("income_analysis", "json")
    
    st.download_button(
        label="📥 결과 다운로드 (JSON)",
        data=json_data,
        file_name=filename,
        mime="application/json"
    )
