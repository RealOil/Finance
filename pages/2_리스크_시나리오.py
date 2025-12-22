"""
페이지 2: 리스크 시나리오

소득 중단, 경제 위기, 은퇴 등 다양한 리스크 상황에서의 생존력을 분석합니다.
"""

import streamlit as st
from shared.session_manager import init_session_state
from shared.page_input_form import render_page_input_form, check_inputs_complete
from modules.validators import validate_inputs, validate_logical_consistency
from modules.calculations import (
    calculate_income_interruption_survival,
    calculate_crisis_scenario,
    calculate_retirement_sustainability,
    calculate_risk_score
)
from modules.formatters import (
    format_currency,
    format_percentage,
    generate_risk_insight,
    generate_retirement_insight
)
from modules.visualizations import (
    create_survival_chart,
    create_risk_score_chart,
    create_risk_breakdown_chart
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
    page_title="리스크 시나리오",
    page_icon="⚠️",
    layout="wide"
)

# 세션 상태 초기화
init_session_state()

# 메인 콘텐츠
st.title("⚠️ 리스크 시나리오")
st.markdown("다양한 리스크 상황에서의 재정 생존력을 분석합니다.")
st.divider()

# 입력 폼 표시
required_fields = [
    'current_age', 'retirement_age', 'salary',
    'monthly_fixed_expense', 'monthly_variable_expense',
    'total_assets', 'total_debt'
]
# 연봉 증가율은 기본값이 있으므로 필수 필드에서 제외

inputs = render_page_input_form("risk", required_fields)

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
    run_simulation = st.button("🚀 시뮬레이션 실행", type="primary", use_container_width=True)
else:
    st.info("💡 모든 필수 항목을 입력해주세요.")
    run_simulation = False
    st.session_state.calculation_done_risk = False

st.divider()

# 계산 결과 표시 (시뮬레이션 버튼을 눌렀을 때만)
if run_simulation:
    # 계산 전 입력값 검증
    from modules.utils import validate_calculation_inputs
    is_valid_calc, validation_error = validate_calculation_inputs(inputs)
    if not is_valid_calc:
        st.error(f"⚠️ {validation_error}")
        st.stop()
    
    # 입력 데이터 요약
    st.header("📋 입력 데이터 요약")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("현재 나이", f"{inputs['current_age']}세")
    st.metric("은퇴 예정 나이", f"{inputs['retirement_age']}세")

with col2:
    st.metric("총 자산", format_currency(inputs['total_assets']))
    st.metric("총 부채", format_currency(inputs['total_debt']))

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
    net_assets = inputs['total_assets'] - inputs['total_debt']
    st.metric("순자산", format_currency(net_assets))

    
    st.divider()
    
    # 계산 수행
# 소득 중단 생존 기간
income_interruption_result, success1, error1 = safe_calculate(
    calculate_income_interruption_survival,
    inputs,
    error_message="소득 중단 생존 기간 계산 중 오류가 발생했습니다."
)

if not success1:
    st.error(f"⚠️ {error1}")
    st.stop()

# 경제 위기 시나리오
crisis_result, success2, error2 = safe_calculate(
    calculate_crisis_scenario,
    inputs,
    30.0,
    error_message="경제 위기 시나리오 계산 중 오류가 발생했습니다."
)

if not success2:
    st.error(f"⚠️ {error2}")
    st.stop()

# 은퇴 후 생활 유지 가능 여부
retirement_result, success3, error3 = safe_calculate(
    calculate_retirement_sustainability,
    inputs,
    error_message="은퇴 후 생활 유지 가능 여부 계산 중 오류가 발생했습니다."
)

if not success3:
    st.error(f"⚠️ {error3}")
    st.stop()

# 종합 위험도 점수
risk_result, success4, error4 = safe_calculate(
    calculate_risk_score,
    inputs,
    error_message="위험도 점수 계산 중 오류가 발생했습니다."
)

    if not success4:
        st.error(f"⚠️ {error4}")
        st.stop()
    
    # 계산 완료 상태 저장
    st.session_state.calculation_done_risk = True
    st.session_state.results_risk = {
        'income_interruption': income_interruption_result,
        'crisis': crisis_result,
        'retirement': retirement_result,
        'risk_score': risk_result
    }
    
    # 결과 표시
    st.header("💰 리스크 분석 결과")

    # 주요 지표
    col1, col2, col3, col4 = st.columns(4)

    with col1:
    survival_months = income_interruption_result.get('survival_months', 0)
    if survival_months == float('inf'):
        st.metric("소득 중단 생존 기간", "무제한")
    else:
        st.metric(
            "소득 중단 생존 기간",
            f"{survival_months:.1f}개월",
            delta=f"{survival_months - 6:.1f}개월" if survival_months < 6 else None,
            delta_color="inverse" if survival_months < 6 else "normal"
        )

    with col2:
    crisis_survival = crisis_result.get('survival_months', 0)
    if crisis_survival == float('inf'):
        st.metric("경제 위기 생존 기간", "무제한")
    else:
        st.metric(
            "경제 위기 생존 기간",
            f"{crisis_survival:.1f}개월",
            delta=f"{crisis_survival - 6:.1f}개월" if crisis_survival < 6 else None,
            delta_color="inverse" if crisis_survival < 6 else "normal"
        )

    with col3:
    retirement_sustainable = retirement_result.get('is_sustainable', False)
    st.metric(
        "은퇴 후 생활 유지",
        "가능" if retirement_sustainable else "불가능",
        delta="안정적" if retirement_sustainable else "위험"
    )

    with col4:
    total_risk_score = risk_result.get('total_score', 0)
    risk_level = risk_result.get('risk_level', 'unknown')
    st.metric(
        "종합 위험도 점수",
        f"{total_risk_score}점",
        delta=risk_level
    )

    st.divider()

    # 상세 분석
    st.header("📊 상세 분석")

    # 소득 중단 시나리오
    st.subheader("1. 소득 중단 시나리오")

    col1, col2 = st.columns(2)

    with col1:
    st.markdown("**생존 가능 기간**")
    survival_chart = create_survival_chart(income_interruption_result)
    st.plotly_chart(survival_chart, use_container_width=True)

    with col2:
    st.markdown("**상세 정보**")
    st.metric("순자산", format_currency(income_interruption_result.get('net_assets', 0)))
    # 기존 필드 호환성
    monthly_expense_value = income_interruption_result.get('monthly_expense', 0)
    if monthly_expense_value == 0 and 'monthly_fixed_expense' in inputs:
        # 새 구조 사용
        monthly_expense_value = inputs.get('monthly_fixed_expense', 0) + inputs.get('monthly_variable_expense', 0)
    st.metric("월 총 지출", format_currency(monthly_expense_value))
    
    status = income_interruption_result.get('status', 'unknown')
    if status == 'safe':
        st.success("✅ 안전: 비상금이 충분합니다.")
    elif status == 'warning':
        st.warning("⚠️ 주의: 비상금이 부족합니다.")
    else:
        st.error("🚨 위험: 비상금이 매우 부족합니다.")
    
    recommendation = income_interruption_result.get('recommendation', '')
    if recommendation:
        st.info(f"💡 **권장 사항**: {recommendation}")

    st.divider()

    # 경제 위기 시나리오
    st.subheader("2. 경제 위기 시나리오 (자산 30% 하락)")

    col1, col2 = st.columns(2)

    with col1:
    st.markdown("**자산 변화**")
    st.metric(
        "위기 전 자산",
        format_currency(crisis_result.get('assets_before', 0))
    )
    st.metric(
        "위기 후 자산",
        format_currency(crisis_result.get('assets_after', 0)),
        delta=format_currency(crisis_result.get('assets_after', 0) - crisis_result.get('assets_before', 0))
    )
    st.metric(
        "위기 후 순자산",
        format_currency(crisis_result.get('net_assets_after', 0))
    )

    with col2:
    st.markdown("**생존 가능 기간**")
    crisis_survival = crisis_result.get('survival_months', 0)
    if crisis_survival == float('inf'):
        st.info("✅ 무제한 생존 가능")
    else:
        st.metric("생존 가능 개월", f"{crisis_survival:.1f}개월")
        
        status = crisis_result.get('status', 'unknown')
        if status == 'safe':
            st.success("✅ 안전: 경제 위기 상황에서도 생존 가능합니다.")
        elif status == 'warning':
            st.warning("⚠️ 주의: 경제 위기 상황에서 생존이 어려울 수 있습니다.")
        else:
            st.error("🚨 위험: 경제 위기 상황에서 생존이 매우 어렵습니다.")

    st.divider()

    # 은퇴 시나리오
    st.subheader("3. 은퇴 후 생활 유지 가능 여부")

    col1, col2 = st.columns(2)

    with col1:
    st.markdown("**은퇴 시점 예상 자산**")
    expected_assets = retirement_result.get('expected_assets_at_retirement', 0)
    st.metric("예상 자산", format_currency(expected_assets))
    
    years_to_retirement = retirement_result.get('years_to_retirement', 0)
    st.metric("은퇴까지 남은 기간", f"{years_to_retirement}년")

    with col2:
    st.markdown("**생활 유지 가능 여부**")
    is_sustainable = retirement_result.get('is_sustainable', False)
    
    if is_sustainable:
        st.success("✅ 은퇴 후 생활 유지 가능")
        survival_years = retirement_result.get('survival_years', 0)
        st.metric("생활 유지 가능 기간", f"{survival_years:.1f}년")
    else:
        st.error("🚨 은퇴 후 생활 유지 불가능")
        st.metric("부족한 자산", format_currency(
            retirement_result.get('shortfall', 0)
        ))
    
    recommendation = retirement_result.get('recommendation', '')
    if recommendation:
        st.info(f"💡 **권장 사항**: {recommendation}")

    st.divider()

    # 종합 위험도 점수
    st.subheader("4. 종합 위험도 점수")

    col1, col2 = st.columns(2)

    with col1:
    st.markdown("**위험도 점수**")
    risk_gauge = create_risk_score_chart(risk_result)
    st.plotly_chart(risk_gauge, use_container_width=True)

    with col2:
    st.markdown("**세부 항목 점수**")
    risk_breakdown = create_risk_breakdown_chart(risk_result)
    st.plotly_chart(risk_breakdown, use_container_width=True)

    # 위험도 점수 해석
    total_score = risk_result.get('total_score', 0)
    if total_score < 25:
    st.success("✅ **낮은 위험도**: 재정 상태가 안정적입니다.")
    elif total_score < 50:
    st.info("ℹ️ **보통 위험도**: 일부 개선이 필요합니다.")
    elif total_score < 75:
    st.warning("⚠️ **높은 위험도**: 재정 상태 개선이 필요합니다.")
    else:
    st.error("🚨 **매우 높은 위험도**: 즉시 재정 상태 개선이 필요합니다.")

    # 권장 사항
    recommendations = risk_result.get('recommendations', [])
    if recommendations:
    st.markdown("**권장 사항**")
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"{i}. {rec}")

    st.divider()

    # 인사이트
    st.header("💡 인사이트")

    # 리스크 인사이트
    risk_insight = generate_risk_insight(risk_result)
    st.info(f"**리스크 분석**: {risk_insight}")

    # 은퇴 인사이트
    retirement_insight = generate_retirement_insight(retirement_result)
    st.info(f"**은퇴 준비도**: {retirement_insight}")

    st.divider()

    # 데이터 출처 및 면책 조항
    st.header("📚 데이터 출처 및 면책 조항")

    with st.expander("데이터 출처"):
    st.markdown("""
    ### 사용된 데이터 출처
    
    - **비상금 기준**: 6개월 생활비 권장 기준
    - **경제 위기 시나리오**: 자산 30% 하락 가정 (과거 경제 위기 평균)
    - **은퇴 후 기대 수명**: 20년 가정 (통계청 기준)
    - **인플레이션**: 연 2.5% 가정 (한국은행 경제통계시스템 기준)
    
    ### 위험도 점수 계산 기준
    
    - **소득 중단 위험**: 비상금 6개월 미만 시 점수 증가
    - **부채 비율 위험**: 자산 대비 부채 비율이 높을수록 점수 증가
    - **지출 비율 위험**: 소득 대비 지출 비율이 높을수록 점수 증가
    - **은퇴 준비도 위험**: 은퇴 후 생활 유지 불가능 시 점수 증가
    
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

    if st.session_state.get('calculation_done_risk', False):
    # 다운로드 데이터 생성
    download_data = {
        'income_interruption': income_interruption_result,
        'crisis': crisis_result,
        'retirement': retirement_result,
        'risk_score': risk_result
    }
    
    json_data = create_json_download(inputs, download_data, page_type="risk")
    filename = get_download_filename("risk_analysis", "json")
    
    st.download_button(
        label="📥 결과 다운로드 (JSON)",
        data=json_data,
        file_name=filename,
        mime="application/json"
    )
    else:
    st.info("계산을 먼저 수행해주세요.")

