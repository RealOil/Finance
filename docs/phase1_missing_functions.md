# Phase 1 디자인 - 정의되지 않은 함수 및 로직

## 개요

Phase 1 디자인 문서에서 호출되거나 언급되었지만 구현이 명확히 정의되지 않은 함수 및 로직을 정리합니다.

---

## 1. 시나리오 계산 함수

### 문제

- `calculate_scenario(scenario, base_data)` 함수가 호출되지만 구현이 정의되지 않음
- 시나리오 이름 파싱 로직 불명확

### 제안 구현

```python
# modules/calculations.py

def calculate_scenario(scenario_name: str, base_inputs: dict) -> dict:
    """
    시나리오별 계산 수행

    Args:
        scenario_name: 시나리오 이름 (예: "현재 패턴", "지출 -10%", "연봉 +5%")
        base_inputs: 기본 입력 데이터

    Returns:
        dict: {
            'years': list,
            'assets': list,
            'assets_5y': float,
            'assets_10y': float,
            'total_savings': float
        }
    """
    # 시나리오에 따라 입력 데이터 수정
    modified_inputs = parse_scenario(scenario_name, base_inputs.copy())

    # 미래 자산 계산
    years = list(range(0, 11))
    assets = calculate_future_assets(
        modified_inputs['total_assets'],
        modified_inputs['salary'],
        modified_inputs['monthly_expense'],
        modified_inputs['salary_growth_rate'],
        years=10
    )

    return {
        'years': years,
        'assets': assets,
        'assets_5y': assets[5],
        'assets_10y': assets[10],
        'total_savings': assets[10] - assets[0],
        'current_assets': assets[0]
    }

def parse_scenario(scenario_name: str, inputs: dict) -> dict:
    """
    시나리오 이름을 파싱하여 입력 데이터 수정

    Args:
        scenario_name: 시나리오 이름
        inputs: 기본 입력 데이터

    Returns:
        dict: 수정된 입력 데이터
    """
    if scenario_name == "현재 패턴":
        return inputs

    # 지출 변경 시나리오
    if "지출" in scenario_name:
        if "-10%" in scenario_name:
            inputs['monthly_expense'] *= 0.9
        elif "-20%" in scenario_name:
            inputs['monthly_expense'] *= 0.8
        elif "-30%" in scenario_name:
            inputs['monthly_expense'] *= 0.7
        elif "+10%" in scenario_name:
            inputs['monthly_expense'] *= 1.1
        elif "+20%" in scenario_name:
            inputs['monthly_expense'] *= 1.2

    # 연봉 변경 시나리오
    if "연봉" in scenario_name:
        if "+3%" in scenario_name:
            inputs['salary_growth_rate'] = 3.0
        elif "+5%" in scenario_name:
            inputs['salary_growth_rate'] = 5.0
        elif "+10%" in scenario_name:
            inputs['salary_growth_rate'] = 10.0
        elif "제자리" in scenario_name or "0%" in scenario_name:
            inputs['salary_growth_rate'] = 0.0

    # 복합 시나리오
    if "+" in scenario_name and "지출" in scenario_name and "연봉" in scenario_name:
        # 예: "지출 -10% + 연봉 +5%"
        parts = scenario_name.split("+")
        for part in parts:
            part = part.strip()
            if "지출" in part:
                if "-10%" in part:
                    inputs['monthly_expense'] *= 0.9
            elif "연봉" in part:
                if "+5%" in part:
                    inputs['salary_growth_rate'] = 5.0

    return inputs
```

---

## 2. 비교 테이블 생성 함수

### 문제

- `create_comparison_table(scenarios, base_data)` 함수가 호출되지만 구현이 정의되지 않음

### 제안 구현

```python
# modules/formatters.py

import pandas as pd

def create_comparison_table(scenarios: list, scenario_results: dict) -> pd.DataFrame:
    """
    시나리오별 비교 테이블 생성

    Args:
        scenarios: 시나리오 이름 리스트
        scenario_results: 각 시나리오의 계산 결과 딕셔너리

    Returns:
        pd.DataFrame: 비교 테이블
    """
    comparison_data = []

    for scenario in scenarios:
        if scenario in scenario_results:
            result = scenario_results[scenario]
            comparison_data.append({
                '시나리오': scenario,
                '5년 후 자산 (만원)': f"{result['assets_5y']:,.0f}",
                '10년 후 자산 (만원)': f"{result['assets_10y']:,.0f}",
                '총 저축액 (만원)': f"{result['total_savings']:,.0f}",
                '자산 증가율 (%)': f"{(result['assets_10y'] / result['current_assets'] - 1) * 100:.1f}"
            })

    return pd.DataFrame(comparison_data)
```

---

## 3. 전체 계산 수행 함수

### 문제

- `perform_calculations(inputs)` 함수가 호출되지만 구현이 정의되지 않음
- 각 페이지에서 필요한 계산 결과 구조가 불명확

### 제안 구현

```python
# modules/calculations.py

def perform_calculations_income(inputs: dict) -> dict:
    """
    소득 및 지출 분석 페이지용 계산 수행

    Returns:
        dict: {
            'assets_10y': float,
            'assets_by_year': list,
            'financial_grade': str,
            'monthly_savings': float,
            'years': list
        }
    """
    years = list(range(0, 11))
    assets_by_year = calculate_future_assets(
        inputs['total_assets'],
        inputs['salary'],
        inputs['monthly_expense'],
        inputs['salary_growth_rate'],
        years=10
    )

    financial_grade = calculate_financial_health_grade(
        inputs['salary'],
        inputs['monthly_expense']
    )

    monthly_savings = (inputs['salary'] / 12) - inputs['monthly_expense']

    return {
        'assets_10y': assets_by_year[-1],
        'assets_by_year': assets_by_year,
        'financial_grade': financial_grade,
        'monthly_savings': monthly_savings,
        'years': years
    }

def perform_calculations_risk(inputs: dict) -> dict:
    """
    리스크 시나리오 페이지용 계산 수행

    Returns:
        dict: {
            'risk_score': int,
            'survival_months': int,
            'crisis_survival_30': int,
            'crisis_survival_50': int,
            'retirement_viability': dict
        }
    """
    risk_score = calculate_risk_score(
        inputs['total_assets'],
        inputs['total_debt'],
        inputs['monthly_expense'],
        inputs['salary'],
        inputs['monthly_expense']
    )

    survival_months = calculate_survival_months(
        inputs['total_assets'],
        inputs['monthly_expense']
    )

    crisis_survival_30 = calculate_crisis_survival(
        inputs['total_assets'],
        inputs['monthly_expense'],
        asset_decline_rate=0.3
    )

    crisis_survival_50 = calculate_crisis_survival(
        inputs['total_assets'],
        inputs['monthly_expense'],
        asset_decline_rate=0.5
    )

    retirement_viability = check_retirement_viability(
        inputs['total_assets'],
        inputs['monthly_expense'],
        inputs['retirement_age'],
        inputs['current_age']
    )

    return {
        'risk_score': risk_score,
        'survival_months': survival_months,
        'crisis_survival_30': crisis_survival_30,
        'crisis_survival_50': crisis_survival_50,
        'retirement_viability': retirement_viability
    }

def perform_calculations_comparison(inputs: dict, scenarios: list) -> dict:
    """
    시나리오 비교 페이지용 계산 수행

    Returns:
        dict: {
            'scenario_results': dict,
            'comparison_table': pd.DataFrame
        }
    """
    scenario_results = {}
    for scenario in scenarios:
        scenario_results[scenario] = calculate_scenario(scenario, inputs)

    comparison_table = create_comparison_table(scenarios, scenario_results)

    return {
        'scenario_results': scenario_results,
        'comparison_table': comparison_table
    }
```

---

## 4. 입력 검증 함수 수정

### 문제

- `validate_inputs()` 함수가 `(is_valid, errors, warnings)` 튜플을 반환하지만
- 페이지 코드에서는 단일 값으로 사용됨

### 제안 수정

```python
# modules/validators.py

def validate_inputs(
    current_age: int,
    retirement_age: int,
    salary: float,
    monthly_expense: float,
    total_assets: float,
    total_debt: float
) -> tuple[bool, list, list]:
    """
    입력 검증

    Returns:
        tuple: (is_valid, errors, warnings)
    """
    errors = []
    warnings = []

    # 필수 입력 확인
    if current_age is None or current_age <= 0:
        errors.append("현재 나이를 입력해주세요")

    if retirement_age is None or retirement_age <= current_age:
        errors.append("은퇴 나이는 현재 나이보다 커야 합니다")

    if salary is None or salary < 0:
        errors.append("연봉을 입력해주세요")

    if monthly_expense is None or monthly_expense < 0:
        errors.append("월 지출을 입력해주세요")

    if total_assets is None or total_assets < 0:
        errors.append("자산을 입력해주세요")

    if total_debt is None or total_debt < 0:
        errors.append("부채를 입력해주세요")

    # 논리적 검증 (경고)
    if monthly_expense > salary / 12:
        warnings.append("⚠️ 월 지출이 월 소득보다 큽니다")

    if total_debt > total_assets:
        warnings.append("⚠️ 부채가 자산보다 큽니다. 순자산이 음수입니다")

    return len(errors) == 0, errors, warnings

# 또는 간단한 버전 (페이지에서 사용)
def is_input_valid(
    current_age: int,
    retirement_age: int,
    salary: float,
    monthly_expense: float,
    total_assets: float,
    total_debt: float
) -> bool:
    """입력이 유효한지 확인 (간단 버전)"""
    is_valid, _, _ = validate_inputs(
        current_age, retirement_age, salary,
        monthly_expense, total_assets, total_debt
    )
    return is_valid
```

---

## 5. 샘플 데이터 UI

### 문제

- 샘플 데이터 적용 함수는 있지만 사이드바에 표시하는 UI가 정의되지 않음

### 제안 구현

```python
# shared/input_form.py 또는 각 페이지에 추가

def render_sample_data_selector():
    """샘플 데이터 선택 UI"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧪 샘플 데이터")

    sample_scenarios = list(SAMPLE_SCENARIOS.keys())
    selected_scenario = st.sidebar.selectbox(
        "시나리오 선택",
        ["직접 입력"] + sample_scenarios,
        help="샘플 데이터로 빠르게 테스트해보세요"
    )

    if selected_scenario != "직접 입력":
        if st.sidebar.button("샘플 데이터 적용", use_container_width=True):
            apply_sample_data(selected_scenario)
            st.rerun()

    return selected_scenario
```

---

## 6. 피드백 수집 UI

### 문제

- 피드백 수집 방법은 문서화되어 있지만 실제 UI 구현이 정의되지 않음

### 제안 구현

```python
# shared/feedback.py

def render_feedback_button():
    """피드백 버튼 렌더링"""
    st.sidebar.markdown("---")

    if st.sidebar.button("💬 피드백 보내기", use_container_width=True):
        with st.sidebar.expander("피드백 작성", expanded=True):
            feedback_type = st.radio(
                "피드백 유형",
                ["버그 신고", "기능 제안", "사용성 개선", "기타"]
            )

            feedback_text = st.text_area(
                "내용",
                placeholder="피드백을 입력해주세요...",
                height=100
            )

            rating = st.slider("만족도", 1, 5, 3)

            if st.button("제출"):
                # 피드백 저장 (JSON 파일 또는 API)
                save_feedback(feedback_type, feedback_text, rating)
                st.success("피드백이 전송되었습니다. 감사합니다!")
                st.rerun()

def save_feedback(feedback_type: str, content: str, rating: int):
    """피드백 저장"""
    import json
    from datetime import datetime

    feedback_data = {
        'type': feedback_type,
        'content': content,
        'rating': rating,
        'timestamp': datetime.now().isoformat()
    }

    # JSON 파일에 저장 (또는 API 호출)
    try:
        with open('feedback.json', 'a', encoding='utf-8') as f:
            f.write(json.dumps(feedback_data, ensure_ascii=False) + '\n')
    except Exception as e:
        st.error(f"피드백 저장 실패: {str(e)}")
```

---

## 7. 페이지별 결과 데이터 구조

### 문제

- 각 페이지의 계산 결과 데이터 구조가 명확하지 않음

### 제안 구조

```python
# 각 페이지별 결과 구조 정의

# pages/1_소득_지출_분석.py
INCOME_RESULTS_STRUCTURE = {
    'assets_10y': float,           # 10년 후 예상 자산
    'assets_by_year': list,        # 연도별 자산 리스트
    'financial_grade': str,        # 재정 건전성 등급 (A~F)
    'monthly_savings': float,     # 월 저축 가능액
    'years': list,                 # 연도 리스트
    'insight_text': str            # 인사이트 텍스트
}

# pages/2_리스크_시나리오.py
RISK_RESULTS_STRUCTURE = {
    'risk_score': int,             # 위험도 점수 (0-100)
    'survival_months': int,        # 소득 중단 시 생존 가능 기간
    'crisis_survival_30': int,     # 자산 -30% 시 생존 기간
    'crisis_survival_50': int,      # 자산 -50% 시 생존 기간
    'retirement_viability': {      # 은퇴 시나리오
        'viable': bool,
        'shortfall': float,
        'required_assets': float
    }
}

# pages/3_시나리오_비교.py
COMPARISON_RESULTS_STRUCTURE = {
    'scenario_results': dict,      # 각 시나리오별 결과
    'comparison_table': pd.DataFrame,  # 비교 테이블
    'selected_scenarios': list     # 선택된 시나리오 리스트
}
```

---

## 8. 페이지 초기화 로직

### 문제

- 각 페이지에서 세션 상태 초기화 시점이 불명확

### 제안 구현

```python
# 각 페이지 상단에 추가

# pages/1_소득_지출_분석.py
import streamlit as st
from shared.session_manager import init_session_state

# 페이지 초기화
init_session_state()

# 페이지 설정
st.set_page_config(
    page_title="소득 및 지출 분석",
    page_icon="📊",
    layout="wide"
)
```

---

## 9. 에러 처리 및 사용자 안내

### 문제

- 계산 실패 시 사용자에게 어떻게 안내할지 불명확

### 제안 구현

```python
# 각 페이지의 계산 부분에 추가

try:
    results = perform_calculations_income(inputs)
    st.session_state.results_income = results
    st.session_state.calculation_done_income = True
except Exception as e:
    st.error("계산 중 오류가 발생했습니다.")
    st.info(f"오류 내용: {str(e)}")
    st.info("입력값을 확인하고 다시 시도해주세요. 문제가 지속되면 피드백을 보내주세요.")
    st.session_state.calculation_done_income = False
```

---

## 10. 다운로드 데이터 구조

### 문제

- 다운로드할 데이터의 정확한 구조가 불명확

### 제안 수정

```python
# modules/formatters.py

def create_download_data_income(results: dict, user_inputs: dict) -> dict:
    """소득 지출 분석 결과 다운로드 데이터"""
    from datetime import datetime

    return {
        '메타데이터': {
            '생성 일시': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '페이지': '소득 및 지출 분석'
        },
        '입력 데이터': user_inputs,
        '계산 결과': {
            '10년 후 예상 자산 (만원)': results['assets_10y'],
            '재정 건전성 등급': results['financial_grade'],
            '월 저축 가능액 (만원)': results['monthly_savings'],
            '연도별 자산 변화': {
                '연도': results['years'],
                '자산 (만원)': results['assets_by_year']
            }
        },
        '인사이트': results.get('insight_text', '')
    }
```

---

## 요약

### 정의되지 않은 주요 함수

1. ✅ `calculate_scenario()` - 시나리오 계산
2. ✅ `parse_scenario()` - 시나리오 파싱
3. ✅ `create_comparison_table()` - 비교 테이블 생성
4. ✅ `perform_calculations_income()` - 소득 분석 계산
5. ✅ `perform_calculations_risk()` - 리스크 분석 계산
6. ✅ `perform_calculations_comparison()` - 시나리오 비교 계산
7. ✅ `is_input_valid()` - 간단한 입력 검증
8. ✅ `render_sample_data_selector()` - 샘플 데이터 UI
9. ✅ `render_feedback_button()` - 피드백 UI
10. ✅ `save_feedback()` - 피드백 저장

### 불명확한 부분

1. ✅ 페이지별 결과 데이터 구조
2. ✅ 페이지 초기화 로직
3. ✅ 에러 처리 및 사용자 안내
4. ✅ 다운로드 데이터 구조

이 문서의 내용을 Phase 1 디자인 문서에 반영하거나, 별도 구현 가이드로 활용할 수 있습니다.
