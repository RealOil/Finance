"""
샘플 데이터 정의

사용자가 빠르게 테스트할 수 있도록 다양한 시나리오의 샘플 데이터를 제공합니다.
"""

from typing import Dict, Any

# 샘플 데이터 시나리오
SAMPLE_SCENARIOS: Dict[str, Dict[str, Any]] = {
    "일반 직장인": {
        'current_age': 30,
        'retirement_age': 60,
        'salary': 5000,
        'salary_growth_rate': 3.0,
        'bonus': 0,
        'monthly_fixed_expense': 120,  # 주거비, 보험료 등
        'monthly_variable_expense': 80,  # 식비, 교통비, 여가비 등
        'total_assets': 1000,
        'total_debt': 0,
        'inflation_rate': 2.5,
        'marital_status': '부부(2인 가구)',
        'retirement_monthly_expense': 318,  # 부부 기준 평균 노후 생활비
        'retirement_medical_expense': 45  # 65세 이상 평균 의료비
    },
    "신입 직장인": {
        'current_age': 25,
        'retirement_age': 60,
        'salary': 3500,
        'salary_growth_rate': 5.0,
        'bonus': 0,
        'monthly_fixed_expense': 100,  # 주거비, 보험료 등
        'monthly_variable_expense': 67,  # 식비, 교통비 등 (연간 고정비 200만원 포함)
        'total_assets': 500,
        'total_debt': 0,
        'inflation_rate': 2.5,
        'marital_status': '1인 가구',
        'retirement_monthly_expense': 170,  # 1인 가구 평균 노후 생활비
        'retirement_medical_expense': 45  # 평균 의료비
    },
    "중년 직장인": {
        'current_age': 40,
        'retirement_age': 60,
        'salary': 7000,
        'salary_growth_rate': 2.0,
        'bonus': 500,
        'monthly_fixed_expense': 250,  # 주거비, 보험료, 대출이자 등
        'monthly_variable_expense': 92,  # 식비, 교통비, 여가비 등 (연간 고정비 500만원 포함)
        'total_assets': 5000,
        'total_debt': 2000,
        'inflation_rate': 2.5,
        'marital_status': '부부(2인 가구)',
        'retirement_monthly_expense': 318,  # 부부 기준 평균 노후 생활비
        'retirement_medical_expense': 45  # 평균 의료비
    },
    "은퇴 준비 중": {
        'current_age': 55,
        'retirement_age': 60,
        'salary': 8000,
        'salary_growth_rate': 2.0,
        'bonus': 1000,
        'monthly_fixed_expense': 300,  # 주거비, 보험료 등
        'monthly_variable_expense': 183,  # 식비, 교통비, 여가비 등 (연간 고정비 1000만원 포함)
        'total_assets': 30000,
        'total_debt': 5000,
        'inflation_rate': 2.5,
        'marital_status': '부부(2인 가구)',
        'retirement_monthly_expense': 318,  # 부부 기준 평균 노후 생활비
        'retirement_medical_expense': 45  # 평균 의료비
    }
}


def get_sample_scenarios() -> Dict[str, Dict[str, Any]]:
    """
    샘플 시나리오 목록 반환
    
    Returns:
        Dict[str, Dict[str, Any]]: 샘플 시나리오 딕셔너리
    """
    return SAMPLE_SCENARIOS


def get_sample_data(scenario_name: str) -> Dict[str, Any]:
    """
    특정 시나리오의 샘플 데이터 반환
    
    Args:
        scenario_name: 시나리오 이름
        
    Returns:
        Dict[str, Any]: 샘플 데이터 딕셔너리
        
    Raises:
        KeyError: 시나리오가 존재하지 않을 경우
    """
    if scenario_name not in SAMPLE_SCENARIOS:
        raise KeyError(f"시나리오 '{scenario_name}'가 존재하지 않습니다.")
    
    return SAMPLE_SCENARIOS[scenario_name].copy()


def apply_sample_data(scenario_name: str, session_state) -> None:
    """
    샘플 데이터를 세션 상태에 적용
    
    Args:
        scenario_name: 시나리오 이름
        session_state: Streamlit 세션 상태 객체
    """
    if scenario_name not in SAMPLE_SCENARIOS:
        raise KeyError(f"시나리오 '{scenario_name}'가 존재하지 않습니다.")
    
    sample_data = SAMPLE_SCENARIOS[scenario_name]
    
    # 세션 상태에 적용
    for key, value in sample_data.items():
        session_state[key] = value
    
    # 샘플 데이터 적용 플래그 설정
    session_state['sample_applied'] = scenario_name

