"""
공통 입력 폼 컴포넌트

모든 페이지에서 공통으로 사용할 수 있는 입력 폼을 렌더링하고,
입력된 데이터를 세션 상태에 저장합니다.
"""

import streamlit as st
from typing import Dict, Any
from shared.session_manager import init_session_state
from data.sample_data import get_sample_scenarios, apply_sample_data


def render_input_form() -> Dict[str, Any]:
    """
    공통 입력 폼 렌더링
    
    사이드바에 입력 폼을 렌더링하고, 입력된 데이터를 세션 상태에 저장합니다.
    
    Returns:
        Dict[str, Any]: 입력 데이터 딕셔너리
    """
    # 세션 상태 초기화
    init_session_state()
    
    # 샘플 데이터 선택
    st.sidebar.markdown("### 🎯 샘플 데이터")
    sample_scenarios = list(get_sample_scenarios().keys())
    sample_scenarios.insert(0, "직접 입력")
    
    selected_sample = st.sidebar.selectbox(
        "샘플 데이터 선택",
        options=sample_scenarios,
        index=0 if st.session_state.get('sample_applied') is None else 
              sample_scenarios.index(st.session_state.get('sample_applied', '직접 입력')) + 1
        if st.session_state.get('sample_applied') in sample_scenarios else 0,
        help="빠르게 테스트하기 위해 샘플 데이터를 선택할 수 있습니다"
    )
    
    if selected_sample != "직접 입력":
        if st.sidebar.button("샘플 데이터 적용", use_container_width=True):
            try:
                apply_sample_data(selected_sample, st.session_state)
                st.sidebar.success(f"'{selected_sample}' 시나리오가 적용되었습니다!")
                st.rerun()
            except KeyError as e:
                st.sidebar.error(f"오류: {str(e)}")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 기본 정보")
    
    current_age = st.sidebar.number_input(
        "현재 나이",
        min_value=0,
        max_value=150,
        value=st.session_state.get('current_age', 30),
        step=1,
        help="만 나이를 입력하세요"
    )
    
    retirement_age = st.sidebar.number_input(
        "기대 은퇴 나이",
        min_value=current_age + 1 if current_age else 1,
        max_value=100,
        value=st.session_state.get('retirement_age', 60),
        step=1,
        help="은퇴를 계획하는 나이입니다"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💰 소득 정보")
    
    salary = st.sidebar.number_input(
        "연봉 (만원)",
        min_value=0,
        value=st.session_state.get('salary', 5000),
        step=100,
        help="세전 연봉을 입력하세요"
    )
    
    salary_growth_rate = st.sidebar.slider(
        "연평균 소득 증가율 (%)",
        min_value=0.0,
        max_value=20.0,
        value=float(st.session_state.get('salary_growth_rate', 3.0)),
        step=0.5,
        help="매년 연봉이 증가하는 비율"
    )
    
    bonus = st.sidebar.number_input(
        "보너스 (만원/년, 선택)",
        min_value=0,
        value=st.session_state.get('bonus', 0),
        step=100,
        help="연간 보너스 금액 (선택 사항)"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💸 소비 정보")
    
    monthly_expense = st.sidebar.number_input(
        "월 지출 (만원)",
        min_value=0,
        value=st.session_state.get('monthly_expense', 200),
        step=10,
        help="월 평균 지출액입니다"
    )
    
    annual_fixed_expense = st.sidebar.number_input(
        "연간 고정 지출 (만원, 선택)",
        min_value=0,
        value=st.session_state.get('annual_fixed_expense', 0),
        step=100,
        help="보험료, 세금 등 연간 고정 지출"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🏦 자산 및 부채")
    
    total_assets = st.sidebar.number_input(
        "현재 총 자산 (만원)",
        min_value=0,
        value=st.session_state.get('total_assets', 1000),
        step=100,
        help="예금, 적금, 주식 등 모든 자산의 합계"
    )
    
    total_debt = st.sidebar.number_input(
        "현재 총 부채 (만원)",
        min_value=0,
        value=st.session_state.get('total_debt', 0),
        step=100,
        help="대출, 신용카드 빚 등 모든 부채의 합계"
    )
    
    # 세션 상태에 저장
    inputs = {
        'current_age': current_age,
        'retirement_age': retirement_age,
        'salary': salary,
        'salary_growth_rate': salary_growth_rate,
        'bonus': bonus,
        'monthly_expense': monthly_expense,
        'annual_fixed_expense': annual_fixed_expense,
        'total_assets': total_assets,
        'total_debt': total_debt
    }
    
    # 세션 상태 업데이트
    for key, value in inputs.items():
        st.session_state[key] = value
    
    return inputs

