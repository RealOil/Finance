"""
페이지별 입력 폼 컴포넌트

각 페이지에서 필요한 입력 필드만 표시하는 컴포넌트입니다.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
from modules.formatters import format_currency


def clear_page_inputs(page_type: str):
    """
    페이지별 입력 필드 세션 상태 초기화
    
    Args:
        page_type: 페이지 타입 ("income", "risk", "comparison")
    """
    # 해당 페이지의 모든 입력 필드 키 목록
    page_input_keys = [
        f"{page_type}_current_age",
        f"{page_type}_retirement_age",
        f"{page_type}_salary",
        f"{page_type}_salary_growth_rate",
        f"{page_type}_bonus",
        f"{page_type}_monthly_fixed_expense",
        f"{page_type}_monthly_variable_expense",
        f"{page_type}_total_assets",
        f"{page_type}_total_debt",
        f"{page_type}_inflation_rate",
        f"{page_type}_marital_status",
        f"{page_type}_retirement_monthly_expense",
        f"{page_type}_retirement_medical_expense",
    ]
    
    # 해당 페이지의 입력 필드만 초기화
    for key in page_input_keys:
        if key in st.session_state:
            del st.session_state[key]
    
    # 공유 세션 상태도 초기화 (페이지별로 독립적으로 관리)
    shared_keys = [
        'current_age', 'retirement_age', 'salary',
        'monthly_fixed_expense', 'monthly_variable_expense',
        'total_assets', 'total_debt'
    ]
    
    for key in shared_keys:
        if key in st.session_state:
            del st.session_state[key]


def render_page_input_form(
    page_type: str,
    required_fields: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    페이지별 입력 폼 렌더링
    
    Args:
        page_type: 페이지 타입 ("income", "risk", "comparison")
        required_fields: 필수 입력 필드 리스트 (None이면 기본 필드 사용)
        
    Returns:
        Dict[str, Any]: 입력 데이터 딕셔너리
    """
    # 현재 페이지 추적 및 페이지 변경 감지
    current_page_key = "_current_page"
    previous_page = st.session_state.get(current_page_key, None)
    
    # 페이지가 변경되었거나 처음 로드된 경우 입력 필드 초기화
    if previous_page is None or previous_page != page_type:
        clear_page_inputs(page_type)
        st.session_state[current_page_key] = page_type
    
    inputs = {}
    
    # 기본 필수 필드
    if required_fields is None:
        required_fields = [
            'current_age', 'retirement_age', 'salary',
            'salary_growth_rate', 'monthly_fixed_expense',
            'monthly_variable_expense', 'total_assets', 'total_debt'
        ]
    
    st.header("📋 입력 정보")
    
    # 모든 정보를 한 row에 배치 (4개 컬럼)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader("기본 정보")
        current_age = st.number_input(
            "현재 나이",
            min_value=0,
            max_value=150,
            value=st.session_state.get(f"{page_type}_current_age", None),
            step=1,
            key=f"{page_type}_current_age",
            help="만 나이를 입력하세요"
        )
        inputs['current_age'] = current_age if current_age is not None else 0
        
        # 현재 나이가 입력되어 있으면 최소값 설정
        min_retirement_age = (current_age + 1) if current_age and current_age > 0 else 1
        
        retirement_age = st.number_input(
            "기대 은퇴 나이",
            min_value=min_retirement_age,
            max_value=100,
            value=st.session_state.get(f"{page_type}_retirement_age", None),
            step=1,
            key=f"{page_type}_retirement_age",
            help="은퇴를 계획하는 나이입니다"
        )
        inputs['retirement_age'] = retirement_age if retirement_age is not None else 0
        
        # 기혼/미혼 선택
        previous_marital_status = st.session_state.get(f"{page_type}_marital_status", '부부(2인 가구)')
        marital_status = st.selectbox(
            "가구 형태",
            options=["부부(2인 가구)", "1인 가구"],
            index=0 if previous_marital_status == '부부(2인 가구)' else 1,
            key=f"{page_type}_marital_status",
            help="은퇴 후 가구 형태를 선택하세요. 선택에 따라 은퇴 후 생활비 기본값이 자동으로 변경됩니다."
        )
        inputs['marital_status'] = marital_status
        
        # 가구 형태가 변경되면 은퇴 후 생활비도 초기화
        if previous_marital_status != marital_status:
            # 가구 형태가 변경되었으므로 은퇴 후 생활비 세션 상태 초기화
            session_key_retirement = f"{page_type}_retirement_monthly_expense"
            if session_key_retirement in st.session_state:
                del st.session_state[session_key_retirement]
    
    with col2:
        st.subheader("소득 정보")
        salary = st.number_input(
            "연봉 (만원)",
            min_value=0,
            value=st.session_state.get(f"{page_type}_salary", None),
            step=100,
            key=f"{page_type}_salary",
            help="세전 연봉을 입력하세요"
        )
        inputs['salary'] = salary if salary is not None else 0
        
        salary_growth_rate = st.slider(
            "연봉 증가율 (%)",
            min_value=0.0,
            max_value=20.0,
            value=float(st.session_state.get(f"{page_type}_salary_growth_rate", 3.0)),
            step=0.5,
            key=f"{page_type}_salary_growth_rate",
            help="매년 연봉이 증가하는 비율"
        )
        inputs['salary_growth_rate'] = salary_growth_rate
        
        bonus = st.number_input(
            "보너스 (만원)",
            min_value=0,
            value=st.session_state.get(f"{page_type}_bonus", 0),
            step=100,
            key=f"{page_type}_bonus",
            help="연간 보너스 금액 (선택)"
        )
        inputs['bonus'] = bonus
    
    with col3:
        st.subheader("소비 정보")
        monthly_fixed_expense = st.number_input(
            "월간 고정비 (만원)",
            min_value=0,
            value=st.session_state.get(f"{page_type}_monthly_fixed_expense", None),
            step=10,
            key=f"{page_type}_monthly_fixed_expense",
            help="주거비, 보험료, 통신비, 대출이자 등 고정 지출"
        )
        monthly_fixed_expense_value = monthly_fixed_expense if monthly_fixed_expense is not None else 0
        inputs['monthly_fixed_expense'] = monthly_fixed_expense_value
        
        monthly_variable_expense = st.number_input(
            "월간 변동비 (만원)",
            min_value=0,
            value=st.session_state.get(f"{page_type}_monthly_variable_expense", None),
            step=10,
            key=f"{page_type}_monthly_variable_expense",
            help="식비, 교통비, 여가비, 쇼핑 등 변동 지출"
        )
        monthly_variable_expense_value = monthly_variable_expense if monthly_variable_expense is not None else 0
        inputs['monthly_variable_expense'] = monthly_variable_expense_value
        
        # 총 월 지출 표시 (읽기 전용)
        monthly_total_expense = monthly_fixed_expense_value + monthly_variable_expense_value
        st.metric("총 월 지출", format_currency(monthly_total_expense))
    
    with col4:
        st.subheader("자산 정보")
        total_assets = st.number_input(
            "총 자산 (만원)",
            min_value=0,
            value=st.session_state.get(f"{page_type}_total_assets", None),
            step=100,
            key=f"{page_type}_total_assets",
            help="현금, 예금, 주식 등 모든 자산의 합계"
        )
        inputs['total_assets'] = total_assets if total_assets is not None else 0
        
        total_debt = st.number_input(
            "총 부채 (만원)",
            min_value=0,
            value=st.session_state.get(f"{page_type}_total_debt", None),
            step=100,
            key=f"{page_type}_total_debt",
            help="대출, 카드 빚 등 모든 부채의 합계"
        )
        inputs['total_debt'] = total_debt if total_debt is not None else 0
    
    # 추가 설정 (인플레이션율, 은퇴 후 생활비)
    st.divider()
    st.subheader("⚙️ 추가 설정")
    
    col_setting1, col_setting2, col_setting3 = st.columns(3)
    
    with col_setting1:
        inflation_rate = st.slider(
            "연간 물가 상승률 (인플레이션율) (%)",
            min_value=0.0,
            max_value=10.0,
            value=float(st.session_state.get(f"{page_type}_inflation_rate", 2.5)),
            step=0.1,
            key=f"{page_type}_inflation_rate",
            help="연간 물가 상승률입니다. 기본값은 2.5%입니다."
        )
        inputs['inflation_rate'] = inflation_rate
    
    with col_setting2:
        # 은퇴 후 생활비 계산 (가구 형태에 따라 동적 기본값)
        current_monthly_total = monthly_fixed_expense_value + monthly_variable_expense_value
        # 가구 형태는 세션 상태에서 가져오되, 없으면 inputs에서 가져옴
        marital_status = st.session_state.get(f"{page_type}_marital_status", inputs.get('marital_status', '부부(2인 가구)'))
        
        # 가구 형태에 따른 평균값 설정
        if marital_status == '부부(2인 가구)':
            avg_retirement_expense = 318  # 만원 단위 (부부 기준 평균)
            min_expense = 200  # 최소값
            max_expense = 500  # 최대값
            help_text = "은퇴 후 예상 월 생활비입니다. 평균값: 부부 기준 월 318만원 (평균)"
        else:  # 1인 가구
            avg_retirement_expense = 170  # 만원 단위 (1인 가구 평균)
            min_expense = 100  # 최소값
            max_expense = 300  # 최대값
            help_text = "은퇴 후 예상 월 생활비입니다. 평균값: 1인 가구 월 170만원 (평균)"
        
        # 현재 생활비와 평균값 중 더 적절한 값을 기본값으로 사용
        if current_monthly_total > 0:
            # 현재 생활비를 기준으로 평균값과 비교하여 적절한 값 선택
            default_retirement_expense = max(avg_retirement_expense, current_monthly_total * 0.7)
        else:
            default_retirement_expense = avg_retirement_expense
        
        # 가구 형태가 변경되었거나 세션에 값이 없으면 기본값 사용
        session_key = f"{page_type}_retirement_monthly_expense"
        current_marital_status = st.session_state.get(f"{page_type}_marital_status", marital_status)
        
        # 가구 형태가 변경되었거나 세션에 값이 없으면 새로운 기본값 사용
        if session_key not in st.session_state:
            # 처음 로드하는 경우
            current_value = default_retirement_expense
        elif current_marital_status != marital_status:
            # 가구 형태가 변경된 경우 - 새로운 기본값 사용
            current_value = default_retirement_expense
        else:
            # 기존 값 사용 (범위 내로 조정)
            existing_value = st.session_state.get(session_key, default_retirement_expense)
            # 범위가 변경되었을 수 있으므로 범위 내로 조정
            current_value = max(min_expense, min(max_expense, existing_value))
            # 범위 밖이면 기본값 사용
            if existing_value < min_expense or existing_value > max_expense:
                current_value = default_retirement_expense
        
        retirement_monthly_expense = st.slider(
            "은퇴 후 월 생활비 (만원)",
            min_value=min_expense,
            max_value=max_expense,
            value=int(current_value),
            step=10,
            key=session_key,
            help=help_text
        )
        inputs['retirement_monthly_expense'] = retirement_monthly_expense
        
        if current_monthly_total > 0:
            ratio = (retirement_monthly_expense / current_monthly_total) * 100
            st.caption(f"현재 생활비 대비 {ratio:.1f}%")

    with col_setting3:
        avg_medical_expense = 45  # Average for 65+ (monthly)
        retirement_medical_expense = st.slider(
            "은퇴 후 월 의료비 (만원)",
            min_value=0,
            max_value=100,
            value=int(st.session_state.get(f"{page_type}_retirement_medical_expense", avg_medical_expense)),
            step=5,
            key=f"{page_type}_retirement_medical_expense",
            help=f"은퇴 후 예상되는 추가 의료비입니다. 65세 이상 평균 월 45만원 (통계 기반)"
        )
        inputs['retirement_medical_expense'] = retirement_medical_expense
        st.caption(f"📊 평균값: {avg_medical_expense}만원")
    
    return inputs


def check_inputs_complete(inputs: Dict[str, Any], required_fields: List[str]) -> bool:
    """
    필수 입력 필드가 모두 채워졌는지 확인
    
    Args:
        inputs: 입력 데이터 딕셔너리
        required_fields: 필수 필드 리스트
        
    Returns:
        bool: 모든 필수 필드가 입력되었으면 True
    """
    for field in required_fields:
        if field not in inputs:
            return False
        
        value = inputs[field]
        
        # None이면 입력되지 않음
        if value is None:
            return False
        
        # 숫자 필드의 경우 0보다 작으면 안됨
        if isinstance(value, (int, float)) and value < 0:
            return False
        
        # 숫자 필드의 경우 0이면 입력되지 않은 것으로 간주 (단, 부채는 0도 유효)
        if isinstance(value, (int, float)) and value == 0:
            if field == 'total_debt':
                continue  # 부채는 0도 유효한 값
            if field == 'bonus':
                continue  # 보너스는 0도 유효한 값
            # 나머지 필드는 0이면 입력되지 않은 것으로 간주
            return False
    
    return True
