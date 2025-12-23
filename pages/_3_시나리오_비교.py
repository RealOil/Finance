"""
페이지 3: 시나리오 비교

여러 재정 전략을 비교하고 최적 시나리오를 추천합니다.
"""

import streamlit as st
from shared.session_manager import init_session_state, get_shared_inputs
from shared.input_form import render_input_form
from modules.validators import validate_inputs
from modules.calculations import (
    calculate_future_assets,
    parse_scenario,
    calculate_scenario,
    compare_scenarios
)
from modules.formatters import (
    format_currency,
    format_percentage
)
from modules.visualizations import create_scenario_comparison_chart
from modules.download import (
    create_json_download,
    create_csv_download,
    get_download_filename
)
from modules.utils import (
    safe_calculate,
    validate_calculation_inputs
)

# 페이지 설정
st.set_page_config(
    page_title="시나리오 비교",
    page_icon="🔄",
    layout="wide"
)

# 세션 상태 초기화
init_session_state()

# 사이드바에 입력 폼 표시
render_input_form()

# 메인 콘텐츠
st.title("🔄 시나리오 비교")
st.markdown("여러 재정 전략을 비교하고 최적 시나리오를 찾아보세요.")
st.divider()

# 입력 데이터 가져오기
inputs = get_shared_inputs()

# 입력 검증
is_valid, errors = validate_inputs(inputs)
if not is_valid:
    st.error("⚠️ 입력 오류가 있습니다. 다음 항목을 확인해주세요:")
    for error in errors:
        st.error(f"- {error}")
    st.stop()

# 논리적 일관성 검증 (경고)
from modules.validators import validate_logical_consistency
warnings = validate_logical_consistency(inputs)
if warnings:
    st.warning("⚠️ 입력 경고:")
    for warning in warnings:
        st.warning(f"- {warning}")

# 시나리오 입력 섹션
st.header("📝 시나리오 입력")

st.markdown("""
**시나리오 입력 형식 예시:**
- `지출 10% 감소`: 월 지출을 10% 줄임
- `연봉 5% 증가`: 연봉 증가율을 5%p 증가
- `지출 5% 감소, 연봉 3% 증가`: 여러 조건 조합

**사전 정의된 시나리오:**
- `현재 패턴 유지`: 현재 입력값 그대로 유지
""")

# 기본 시나리오 (현재 패턴 유지)
base_scenario_name = "현재 패턴 유지"

# 비교할 시나리오 입력
st.subheader("비교할 시나리오 입력")

col1, col2 = st.columns([3, 1])

with col1:
    scenario_input = st.text_input(
        "시나리오 1",
        value="지출 10% 감소",
        help="예: '지출 10% 감소', '연봉 5% 증가'"
    )

with col2:
    add_scenario = st.button("추가", use_container_width=True)

# 시나리오 목록 관리
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = []

if add_scenario and scenario_input:
    try:
        parsed = parse_scenario(scenario_input)
        if parsed:
            st.session_state.scenarios.append({
                'name': scenario_input,
                'parsed': parsed
            })
            st.success(f"시나리오 '{scenario_input}' 추가됨")
            scenario_input = ""  # 입력 필드 초기화
    except Exception as e:
        st.error(f"시나리오 파싱 오류: {str(e)}")

# 시나리오 목록 표시
if st.session_state.scenarios:
    st.subheader("추가된 시나리오")
    
    for i, scenario in enumerate(st.session_state.scenarios):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.text(f"{i+1}. {scenario['name']}")
        with col2:
            if st.button("삭제", key=f"delete_{i}", use_container_width=True):
                st.session_state.scenarios.pop(i)
                st.rerun()

# 계산 수행
st.divider()
st.header("💰 시나리오 비교 결과")

# 계산 전 입력값 검증
is_valid, validation_error = validate_calculation_inputs(inputs)
if not is_valid:
    st.error(f"⚠️ {validation_error}")
    st.stop()

years_to_retirement = inputs['retirement_age'] - inputs['current_age']
if years_to_retirement <= 0:
    st.error("⚠️ 은퇴 나이는 현재 나이보다 커야 합니다.")
    st.stop()

# 기본 시나리오 계산
base_scenario_parsed, success1, error1 = safe_calculate(
    parse_scenario,
    base_scenario_name,
    error_message="기본 시나리오 파싱 중 오류가 발생했습니다."
)

if not success1:
    st.error(f"⚠️ {error1}")
    st.stop()

base_result, success2, error2 = safe_calculate(
    calculate_scenario,
    inputs,
    base_scenario_parsed,
    years_to_retirement,
    error_message="기본 시나리오 계산 중 오류가 발생했습니다."
)

if not success2:
    st.error(f"⚠️ {error2}")
    st.stop()

base_result['scenario_name'] = base_scenario_name
base_result['current_assets'] = inputs['total_assets']

# 비교 시나리오 계산
comparison_scenarios = []
for scenario_data in st.session_state.scenarios:
    scenario_result, success, error = safe_calculate(
        calculate_scenario,
        inputs,
        scenario_data['parsed'],
        years_to_retirement,
        error_message=f"시나리오 '{scenario_data['name']}' 계산 중 오류가 발생했습니다."
    )
    
    if not success:
        st.warning(f"⚠️ 시나리오 '{scenario_data['name']}': {error}")
        continue
    
    scenario_result['scenario_name'] = scenario_data['name']
    scenario_result['current_assets'] = inputs['total_assets']
    comparison_scenarios.append(scenario_result)

if not comparison_scenarios:
    st.warning("⚠️ 비교할 수 있는 시나리오가 없습니다. 시나리오를 추가해주세요.")
    st.stop()

# 시나리오 비교
all_scenarios = [base_result] + comparison_scenarios
comparison_result, success3, error3 = safe_calculate(
    compare_scenarios,
    all_scenarios,
    error_message="시나리오 비교 중 오류가 발생했습니다."
)

if not success3:
    st.error(f"⚠️ {error3}")
    st.stop()

# 계산 완료 상태 저장
st.session_state.calculation_done_comparison = True
st.session_state.results_comparison = {
    'base_scenario': base_result,
    'scenarios': comparison_scenarios,
    'comparison': comparison_result
}

# 결과 표시
if not comparison_scenarios:
    st.info("💡 비교할 시나리오를 추가해주세요.")
else:
    # 주요 지표 비교
    st.subheader("주요 지표 비교")
    
    # 테이블로 비교
    import pandas as pd
    
    comparison_data = []
    for scenario in all_scenarios:
        comparison_data.append({
            '시나리오': scenario['scenario_name'],
            '미래 자산 (만원)': round(scenario['future_assets'], 0),
            '총 저축액 (만원)': round(scenario['total_savings'], 0),
            '자산 증가율 (%)': round(
                ((scenario['future_assets'] - inputs['total_assets']) / inputs['total_assets'] * 100) 
                if inputs['total_assets'] > 0 else 0, 
                1
            )
        })
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True)
    
    # 최적/최악 시나리오
    best_scenario = comparison_result.get('best_scenario', {})
    worst_scenario = comparison_result.get('worst_scenario', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        if best_scenario:
            st.success(f"✅ **최적 시나리오**: {best_scenario.get('scenario_name', 'N/A')}")
            st.metric(
                "미래 자산",
                format_currency(best_scenario.get('future_assets', 0))
            )
    
    with col2:
        if worst_scenario:
            st.warning(f"⚠️ **최악 시나리오**: {worst_scenario.get('scenario_name', 'N/A')}")
            st.metric(
                "미래 자산",
                format_currency(worst_scenario.get('future_assets', 0))
            )
    
    st.divider()
    
    # 시각화
    st.subheader("시나리오별 자산 변화 비교")
    
    comparison_chart_data = {
        'base_scenario': base_result,
        'scenarios': comparison_scenarios
    }
    
    chart = create_scenario_comparison_chart(comparison_chart_data)
    st.plotly_chart(chart, use_container_width=True)
    
    st.divider()
    
    # 차이점 분석
    st.subheader("차이점 분석")
    
    if best_scenario and worst_scenario:
        best_assets = best_scenario.get('future_assets', 0)
        worst_assets = worst_scenario.get('future_assets', 0)
        difference = best_assets - worst_assets
        
        st.metric(
            "최적 시나리오와 최악 시나리오 차이",
            format_currency(difference),
            delta=f"{format_percentage((difference / worst_assets * 100) if worst_assets > 0 else 0)}"
        )
        
        st.info(f"""
        **인사이트**:
        - 최적 시나리오({best_scenario.get('scenario_name', 'N/A')})를 선택하면 
          최악 시나리오({worst_scenario.get('scenario_name', 'N/A')}) 대비 
          {format_currency(difference)} 더 많은 자산을 확보할 수 있습니다.
        - 이는 {years_to_retirement}년 후 은퇴 시점의 차이입니다.
        """)

st.divider()

# 데이터 출처 및 면책 조항
st.header("📚 데이터 출처 및 면책 조항")

with st.expander("데이터 출처"):
    st.markdown("""
    ### 사용된 데이터 출처
    
    - **인플레이션**: 연 2.5% 가정 (한국은행 경제통계시스템 기준)
    - **연봉 증가율**: 사용자 입력값 사용 (기본값 3.0%)
    - **시나리오 계산**: 입력 데이터와 가정에 기반한 추정치
    
    ### 시나리오 비교 가정
    
    - 모든 시나리오는 동일한 기간({years_to_retirement}년) 동안 계산됩니다.
    - 인플레이션은 모든 시나리오에 동일하게 적용됩니다.
    - 투자 수익은 고려하지 않습니다 (저축만 고려).
    
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

if st.session_state.get('calculation_done_comparison', False) and comparison_scenarios:
    # JSON 다운로드
    download_data = {
        'base_scenario': base_result,
        'scenarios': comparison_scenarios,
        'comparison': comparison_result
    }
    
    json_data = create_json_download(inputs, download_data, page_type="comparison")
    json_filename = get_download_filename("scenario_comparison", "json")
    
    st.download_button(
        label="📥 결과 다운로드 (JSON)",
        data=json_data,
        file_name=json_filename,
        mime="application/json"
    )
    
    # CSV 다운로드 (시나리오 비교 테이블)
    comparison_data = []
    for scenario in all_scenarios:
        comparison_data.append({
            '시나리오': scenario['scenario_name'],
            '미래 자산 (만원)': round(scenario['future_assets'], 0),
            '총 저축액 (만원)': round(scenario['total_savings'], 0),
            '자산 증가율 (%)': round(
                ((scenario['future_assets'] - inputs['total_assets']) / inputs['total_assets'] * 100) 
                if inputs['total_assets'] > 0 else 0, 
                1
            )
        })
    
    csv_data = create_csv_download(comparison_data)
    csv_filename = get_download_filename("scenario_comparison", "csv")
    
    st.download_button(
        label="📊 시나리오 비교 다운로드 (CSV)",
        data=csv_data,
        file_name=csv_filename,
        mime="text/csv"
    )
else:
    st.info("시나리오를 추가하고 계산을 수행해주세요.")

