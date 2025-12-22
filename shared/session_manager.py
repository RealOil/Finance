"""
세션 상태 관리 모듈

Streamlit 세션 상태를 관리하여 모든 페이지에서 공유할 수 있는
입력 데이터와 계산 결과를 관리합니다.
"""

from typing import Dict, Any

# Streamlit import는 런타임에만 필요하므로 조건부 import
try:
    import streamlit as st
except ImportError:
    # 테스트 환경에서 streamlit이 없을 경우를 대비한 더미 객체
    class DummyStreamlit:
        class SessionState:
            def __init__(self):
                self._data = {}
            
            def __contains__(self, key):
                return key in self._data
            
            def __getitem__(self, key):
                return self._data.get(key)
            
            def __setitem__(self, key, value):
                self._data[key] = value
            
            def get(self, key, default=None):
                return self._data.get(key, default)
        
        def __init__(self):
            self.session_state = self.SessionState()
    
    st = DummyStreamlit()


def init_session_state() -> None:
    """
    세션 상태 초기화
    
    모든 페이지에서 공유할 입력 데이터와 계산 결과 저장소를 초기화합니다.
    """
    # 입력 데이터 (모든 페이지 공유)
    # 초기값은 None으로 설정하여 사용자가 직접 입력하도록 함
    if 'current_age' not in st.session_state:
        st.session_state.current_age = None
        st.session_state.retirement_age = None
        st.session_state.salary = None
        st.session_state.salary_growth_rate = 3.0  # 기본값 유지
        st.session_state.bonus = 0  # 보너스는 0도 유효
        st.session_state.monthly_fixed_expense = None
        st.session_state.monthly_variable_expense = None
        # 하위 호환성을 위한 기존 필드도 유지
        st.session_state.monthly_expense = None
        st.session_state.annual_fixed_expense = 0
        # 추가 설정 (기본값 유지)
        st.session_state.inflation_rate = 2.5
        st.session_state.marital_status = '부부(2인 가구)'
        st.session_state.retirement_monthly_expense = None  # 사용자 입력 필요
        st.session_state.retirement_medical_expense = 45  # 기본값 유지
        st.session_state.total_assets = None
        st.session_state.total_debt = 0  # 부채는 0도 유효
    
    # 페이지별 계산 완료 상태
    if 'calculation_done_income' not in st.session_state:
        st.session_state.calculation_done_income = False
        st.session_state.calculation_done_risk = False
        st.session_state.calculation_done_comparison = False
    
    # 페이지별 결과 저장소
    if 'results_income' not in st.session_state:
        st.session_state.results_income = None
        st.session_state.results_risk = None
        st.session_state.results_comparison = None


def get_shared_inputs() -> Dict[str, Any]:
    """
    공유 입력 데이터 반환
    
    세션 상태에서 입력 데이터를 딕셔너리로 반환합니다.
    모든 페이지에서 동일한 입력 데이터를 사용할 수 있습니다.
    
    Returns:
        Dict[str, Any]: 입력 데이터 딕셔너리
            - current_age: 현재 나이
            - retirement_age: 은퇴 나이
            - salary: 연봉 (만원)
            - salary_growth_rate: 연봉 증가율 (%)
            - bonus: 보너스 (만원/년)
            - monthly_fixed_expense: 월간 고정비 (만원)
            - monthly_variable_expense: 월간 변동비 (만원)
            - monthly_expense: 월 지출 (만원, 하위 호환성)
            - annual_fixed_expense: 연간 고정 지출 (만원, 하위 호환성)
            - total_assets: 총 자산 (만원)
            - total_debt: 총 부채 (만원)
    """
    return {
        'current_age': st.session_state.get('current_age', 30),
        'retirement_age': st.session_state.get('retirement_age', 60),
        'salary': st.session_state.get('salary', 5000),
        'salary_growth_rate': st.session_state.get('salary_growth_rate', 3.0),
        'bonus': st.session_state.get('bonus', 0),
        'monthly_fixed_expense': st.session_state.get('monthly_fixed_expense', 120),
        'monthly_variable_expense': st.session_state.get('monthly_variable_expense', 80),
        # 하위 호환성을 위한 기존 필드도 유지
        'monthly_expense': st.session_state.get('monthly_expense', 200),
        'annual_fixed_expense': st.session_state.get('annual_fixed_expense', 0),
        'total_assets': st.session_state.get('total_assets', 1000),
        'total_debt': st.session_state.get('total_debt', 0)
    }

