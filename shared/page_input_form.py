"""
페이지별 입력 폼 컴포넌트

각 페이지에서 필요한 입력 필드만 표시하는 컴포넌트입니다.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
from modules.formatters import format_currency
import uuid

# 지출 카테고리 정의 (가계부 앱 기준)
# 고정비 카테고리 (일반적으로 매월 고정적으로 발생하는 지출)
FIXED_EXPENSE_CATEGORIES = [
    "주거/통신",  # 월세, 관리비, 통신비 등
    "금융",  # 금융 수수료 등
    "대출이자",  # 주택담보대출, 전세자금대출 등 대출 이자
    "자동차",  # 자동차 대출이자, 보험료 등
    "의료/건강",  # 건강보험료, 생명보험료 등
    "구독서비스",  # 넷플릭스, 유튜브 프리미엄, 스포티파이 등
]

# 변동비 카테고리 (매월 변동하는 지출)
VARIABLE_EXPENSE_CATEGORIES = [
    "식비",
    "카페/간식",
    "술/유흥",
    "생활",
    "온라인쇼핑",
    "패션/쇼핑",
    "뷰티/미용",
    "교통",
    "문화/여가",
    "여행/숙박",
    "교육/학습",
    "자녀/육아",
    "반려동물",
    "경조/선물",
]

# 자산 타입 정의
ASSET_TYPES = ["예금", "적금", "부동산", "주식"]

# 대출 상환 방식 정의
DEBT_REPAYMENT_TYPES = [
    "만기 원금 상환",  # 전세 대출 등 (원금은 만기 일시 상환, 매월 이자만 납입)
    "균등 상환",  # 매월 원금+이자 동일하게 상환
    "분할 상환",  # 원금 균등 + 이자
]


def calculate_deposit_interest(
    principal: float, months: int, annual_rate: float, is_compound: bool = False
) -> float:
    """
    예금 이자 계산

    Args:
        principal: 원금 (원)
        months: 개월 수
        annual_rate: 연이율 (%)
        is_compound: True면 복리, False면 단리 (기본값: False)

    Returns:
        float: 원금 + 이자 (원)
    """
    if principal <= 0 or months <= 0 or annual_rate <= 0:
        return principal

    annual_rate_decimal = annual_rate / 100.0

    if is_compound:
        # 복리: 원금 × (1 + 연이율)^(개월수/12)
        total = principal * ((1 + annual_rate_decimal) ** (months / 12.0))
    else:
        # 단리: 원금 + (원금 × 연이율 × 개월수 / 12)
        interest = principal * annual_rate_decimal * (months / 12.0)
        total = principal + interest

    return total


def calculate_savings_interest(
    monthly_amount: float, months: int, annual_rate: float, is_compound: bool = False
) -> float:
    """
    적금 이자 계산

    Args:
        monthly_amount: 월 납입액 (원)
        months: 개월 수
        annual_rate: 연이율 (%)
        is_compound: True면 복리, False면 단리 (기본값: False)

    Returns:
        float: 원금합계 + 이자 (원)
    """
    if monthly_amount <= 0 or months <= 0 or annual_rate <= 0:
        return monthly_amount * months

    annual_rate_decimal = annual_rate / 100.0
    principal_total = monthly_amount * months

    if is_compound:
        # 복리: 매달 납입액이 복리로 계산
        monthly_rate = annual_rate_decimal / 12.0
        # 등비수열의 합: a × (r^(n+1) - r) / (r - 1)
        # 여기서 a = monthly_amount, r = (1 + monthly_rate), n = months
        if monthly_rate > 0:
            total = (
                monthly_amount
                * ((1 + monthly_rate) ** (months + 1) - (1 + monthly_rate))
                / monthly_rate
            )
        else:
            total = principal_total
    else:
        # 단리: 매달 납입액에 대해 개월수만큼 이자 계산
        # 첫 달: monthly_amount × annual_rate × months / 12
        # 둘째 달: monthly_amount × annual_rate × (months-1) / 12
        # ...
        # 합계: monthly_amount × annual_rate / 12 × (1 + 2 + ... + months)
        # = monthly_amount × annual_rate / 12 × months × (months + 1) / 2
        interest = (
            monthly_amount * annual_rate_decimal / 12.0 * months * (months + 1) / 2.0
        )
        total = principal_total + interest

    return total


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
        f"{page_type}_fixed_expense_items",
        f"{page_type}_variable_expense_items",
        f"{page_type}_asset_items",
        f"{page_type}_monthly_investment_items",
        f"{page_type}_debt_items",
        f"{page_type}_other_debt",
        f"{page_type}_adding_fixed",
        f"{page_type}_adding_variable",
        f"{page_type}_adding_asset",
        f"{page_type}_adding_monthly_investment",
        f"{page_type}_adding_debt",
    ]

    # 해당 페이지의 입력 필드만 초기화
    for key in page_input_keys:
        if key in st.session_state:
            del st.session_state[key]

    # 공유 세션 상태도 초기화 (페이지별로 독립적으로 관리)
    shared_keys = [
        "current_age",
        "retirement_age",
        "salary",
        "monthly_fixed_expense",
        "monthly_variable_expense",
        "total_assets",
        "total_debt",
    ]

    for key in shared_keys:
        if key in st.session_state:
            del st.session_state[key]


def render_page_input_form(
    page_type: str, required_fields: Optional[List[str]] = None
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
            "current_age",
            "retirement_age",
            "salary",
            "salary_growth_rate",
            "monthly_fixed_expense",
            "monthly_variable_expense",
            "total_assets",
            "total_debt",
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
            help="만 나이를 입력하세요",
        )
        inputs["current_age"] = current_age if current_age is not None else 0

        # 현재 나이가 입력되어 있으면 최소값 설정
        min_retirement_age = (current_age + 1) if current_age and current_age > 0 else 1

        retirement_age = st.number_input(
            "기대 은퇴 나이",
            min_value=min_retirement_age,
            max_value=100,
            value=st.session_state.get(f"{page_type}_retirement_age", None),
            step=1,
            key=f"{page_type}_retirement_age",
            help="은퇴를 계획하는 나이입니다",
        )
        inputs["retirement_age"] = retirement_age if retirement_age is not None else 0

        # 기혼/미혼 선택
        previous_marital_status = st.session_state.get(
            f"{page_type}_marital_status", "부부(2인 가구)"
        )
        marital_status = st.selectbox(
            "가구 형태",
            options=["부부(2인 가구)", "1인 가구"],
            index=0 if previous_marital_status == "부부(2인 가구)" else 1,
            key=f"{page_type}_marital_status",
            help="은퇴 후 가구 형태를 선택하세요. 선택에 따라 은퇴 후 생활비 기본값이 자동으로 변경됩니다.",
        )
        inputs["marital_status"] = marital_status

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
            help="세전 연봉을 입력하세요",
        )
        inputs["salary"] = salary if salary is not None else 0

        salary_growth_rate = st.slider(
            "연봉 증가율 (%)",
            min_value=0.0,
            max_value=20.0,
            value=float(st.session_state.get(f"{page_type}_salary_growth_rate", 3.0)),
            step=0.5,
            key=f"{page_type}_salary_growth_rate",
            help="매년 연봉이 증가하는 비율",
        )
        inputs["salary_growth_rate"] = salary_growth_rate

        bonus = st.number_input(
            "보너스 (만원)",
            min_value=0,
            value=st.session_state.get(f"{page_type}_bonus", 0),
            step=100,
            key=f"{page_type}_bonus",
            help="연간 보너스 금액 (선택)",
        )
        inputs["bonus"] = bonus

    with col3:
        st.subheader("소비 정보")

        # 고정비 항목 리스트 초기화
        fixed_expense_key = f"{page_type}_fixed_expense_items"
        if fixed_expense_key not in st.session_state:
            st.session_state[fixed_expense_key] = []

        # 변동비 항목 리스트 초기화
        variable_expense_key = f"{page_type}_variable_expense_items"
        if variable_expense_key not in st.session_state:
            st.session_state[variable_expense_key] = []

        # 고정비 섹션
        st.markdown("**고정비**")
        fixed_items = st.session_state[fixed_expense_key]
        fixed_total = sum(item.get("amount", 0) for item in fixed_items)  # 1원 단위
        st.markdown(
            f"**합계: {fixed_total:,}원** (만원: {fixed_total / 10000:.1f}만원)"
        )

        # 고정비 항목 표시 및 삭제
        for idx, item in enumerate(fixed_items):
            col_cat, col_amt, col_del = st.columns([3, 2, 1])
            with col_cat:
                st.text(f"{item.get('category', '')}")
            with col_amt:
                st.text(f"{item.get('amount', 0):,}원")
            with col_del:
                if st.button(
                    "삭제",
                    key=f"{page_type}_fixed_del_{item['id']}",
                    use_container_width=True,
                ):
                    st.session_state[fixed_expense_key] = [
                        i for i in fixed_items if i["id"] != item["id"]
                    ]
                    st.rerun()

        # 고정비 추가 버튼
        if st.button(
            "➕ 고정비 추가", key=f"{page_type}_add_fixed", use_container_width=True
        ):
            # 새 항목 추가 모달 대신 inline 입력
            st.session_state[f"{page_type}_adding_fixed"] = True

        # 고정비 추가 입력 폼
        if st.session_state.get(f"{page_type}_adding_fixed", False):
            with st.container():
                col_cat, col_amt = st.columns([2, 2])
                with col_cat:
                    new_category = st.selectbox(
                        "카테고리",
                        FIXED_EXPENSE_CATEGORIES,
                        key=f"{page_type}_new_fixed_category",
                    )
                with col_amt:
                    new_amount = st.number_input(
                        "금액 (원)",
                        min_value=0,
                        value=0,
                        step=1000,
                        key=f"{page_type}_new_fixed_amount",
                    )
                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button(
                        "저장", key=f"{page_type}_save_fixed", use_container_width=True
                    ):
                        new_item = {
                            "id": str(uuid.uuid4()),
                            "category": new_category,
                            "amount": new_amount,
                        }
                        st.session_state[fixed_expense_key].append(new_item)
                        st.session_state[f"{page_type}_adding_fixed"] = False
                        st.rerun()
                with col_cancel:
                    if st.button(
                        "취소",
                        key=f"{page_type}_cancel_fixed",
                        use_container_width=True,
                    ):
                        st.session_state[f"{page_type}_adding_fixed"] = False
                        st.rerun()

        st.divider()

        # 변동비 섹션
        st.markdown("**변동비**")
        variable_items = st.session_state[variable_expense_key]
        variable_total = sum(
            item.get("amount", 0) for item in variable_items
        )  # 1원 단위
        st.markdown(
            f"**합계: {variable_total:,}원** (만원: {variable_total / 10000:.1f}만원)"
        )

        # 변동비 항목 표시 및 삭제
        for idx, item in enumerate(variable_items):
            col_cat, col_amt, col_del = st.columns([3, 2, 1])
            with col_cat:
                st.text(f"{item.get('category', '')}")
            with col_amt:
                st.text(f"{item.get('amount', 0):,}원")
            with col_del:
                if st.button(
                    "삭제",
                    key=f"{page_type}_variable_del_{item['id']}",
                    use_container_width=True,
                ):
                    st.session_state[variable_expense_key] = [
                        i for i in variable_items if i["id"] != item["id"]
                    ]
                    st.rerun()

        # 변동비 추가 버튼
        if st.button(
            "➕ 변동비 추가", key=f"{page_type}_add_variable", use_container_width=True
        ):
            st.session_state[f"{page_type}_adding_variable"] = True

        # 변동비 추가 입력 폼
        if st.session_state.get(f"{page_type}_adding_variable", False):
            with st.container():
                col_cat, col_amt = st.columns([2, 2])
                with col_cat:
                    new_category = st.selectbox(
                        "카테고리",
                        VARIABLE_EXPENSE_CATEGORIES,
                        key=f"{page_type}_new_variable_category",
                    )
                with col_amt:
                    new_amount = st.number_input(
                        "금액 (원)",
                        min_value=0,
                        value=0,
                        step=1000,
                        key=f"{page_type}_new_variable_amount",
                    )
                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button(
                        "저장",
                        key=f"{page_type}_save_variable",
                        use_container_width=True,
                    ):
                        new_item = {
                            "id": str(uuid.uuid4()),
                            "category": new_category,
                            "amount": new_amount,
                        }
                        st.session_state[variable_expense_key].append(new_item)
                        st.session_state[f"{page_type}_adding_variable"] = False
                        st.rerun()
                with col_cancel:
                    if st.button(
                        "취소",
                        key=f"{page_type}_cancel_variable",
                        use_container_width=True,
                    ):
                        st.session_state[f"{page_type}_adding_variable"] = False
                        st.rerun()

        # 총 월 지출 (만원 단위로 변환하여 저장)
        monthly_total_expense_won = fixed_total + variable_total
        monthly_fixed_expense_value = fixed_total / 10000  # 만원 단위로 변환
        monthly_variable_expense_value = variable_total / 10000  # 만원 단위로 변환
        st.divider()
        st.markdown(
            f"**총 월 지출: {monthly_total_expense_won:,}원** ({monthly_fixed_expense_value + monthly_variable_expense_value:.1f}만원)"
        )

        # inputs에 저장 (만원 단위)
        inputs["monthly_fixed_expense"] = monthly_fixed_expense_value
        inputs["monthly_variable_expense"] = monthly_variable_expense_value
        inputs["fixed_expense_items"] = fixed_items
        inputs["variable_expense_items"] = variable_items

    with col4:
        st.subheader("자산 정보")

        # 자산 항목 리스트 초기화
        assets_key = f"{page_type}_asset_items"
        if assets_key not in st.session_state:
            st.session_state[assets_key] = []

        # 자산 항목 표시
        asset_items = st.session_state[assets_key]

        # 자산 합계 계산 (타입별로 다르게 계산, 예금/적금은 이자 포함)
        assets_total = 0
        for item in asset_items:
            asset_type = item.get("type", "")
            if asset_type == "예금":
                principal = item.get("amount", 0)
                months = item.get("months", 0)
                rate = item.get("rate", 0.0)
                is_compound = item.get("is_compound", False)
                assets_total += calculate_deposit_interest(
                    principal, months, rate, is_compound
                )
            elif asset_type == "적금":
                monthly_amount = item.get("monthly_amount", 0)
                months = item.get("months", 0)
                rate = item.get("rate", 0.0)
                is_compound = item.get("is_compound", False)
                assets_total += calculate_savings_interest(
                    monthly_amount, months, rate, is_compound
                )
            elif asset_type == "부동산":
                assets_total += item.get("value", 0)
            elif asset_type == "주식":
                assets_total += item.get("amount", 0)

        st.markdown(
            f"**합계: {assets_total:,}원** (만원: {assets_total / 10000:.1f}만원)"
        )

        # 자산 항목 표시 및 삭제
        for item in asset_items:
            asset_type = item.get("type", "")
            col_type, col_info, col_del = st.columns([2, 4, 1])
            with col_type:
                st.text(f"{asset_type}")
            with col_info:
                if asset_type == "예금":
                    principal = item.get("amount", 0)
                    months = item.get("months", 0)
                    rate = item.get("rate", 0.0)
                    is_compound = item.get("is_compound", False)
                    total = calculate_deposit_interest(
                        principal, months, rate, is_compound
                    )
                    interest_type = "복리" if is_compound else "단리"
                    st.text(
                        f"{principal:,}원, {months}개월, {rate:.2f}% ({interest_type}) → {total:,.0f}원"
                    )
                elif asset_type == "적금":
                    monthly_amount = item.get("monthly_amount", 0)
                    months = item.get("months", 0)
                    rate = item.get("rate", 0.0)
                    is_compound = item.get("is_compound", False)
                    total = calculate_savings_interest(
                        monthly_amount, months, rate, is_compound
                    )
                    interest_type = "복리" if is_compound else "단리"
                    st.text(
                        f"월 {monthly_amount:,}원, {months}개월, {rate:.2f}% ({interest_type}) → {total:,.0f}원"
                    )
                elif asset_type == "부동산":
                    st.text(f"{item.get('value', 0):,}원")
                elif asset_type == "주식":
                    st.text(
                        f"{item.get('amount', 0):,}원, {item.get('return_rate', 0):.2f}%"
                    )
            with col_del:
                if st.button(
                    "삭제",
                    key=f"{page_type}_asset_del_{item['id']}",
                    use_container_width=True,
                ):
                    st.session_state[assets_key] = [
                        i for i in asset_items if i["id"] != item["id"]
                    ]
                    st.rerun()

        # 자산 추가 버튼
        if st.button(
            "➕ 자산 추가", key=f"{page_type}_add_asset", use_container_width=True
        ):
            st.session_state[f"{page_type}_adding_asset"] = True

        # 자산 추가 입력 폼
        if st.session_state.get(f"{page_type}_adding_asset", False):
            with st.container():
                asset_type = st.selectbox(
                    "자산 타입", ASSET_TYPES, key=f"{page_type}_new_asset_type"
                )

                new_item = {"id": str(uuid.uuid4()), "type": asset_type}

                if asset_type == "예금":
                    col_amt, col_mon, col_rate, col_interest = st.columns(
                        [2, 1.5, 1.5, 1]
                    )
                    with col_amt:
                        amount = st.number_input(
                            "금액 (원)",
                            min_value=0,
                            value=0,
                            step=10000,
                            key=f"{page_type}_new_deposit_amount",
                        )
                    with col_mon:
                        months = st.number_input(
                            "개월 수",
                            min_value=0,
                            value=0,
                            step=1,
                            key=f"{page_type}_new_deposit_months",
                        )
                    with col_rate:
                        rate = st.number_input(
                            "금리 (%)",
                            min_value=0.0,
                            max_value=20.0,
                            value=0.0,
                            step=0.1,
                            format="%.2f",
                            key=f"{page_type}_new_deposit_rate",
                        )
                    with col_interest:
                        is_compound = st.selectbox(
                            "이자",
                            ["단리", "복리"],
                            index=0,
                            key=f"{page_type}_new_deposit_interest_type",
                        )
                    new_item.update(
                        {
                            "amount": amount,
                            "months": months,
                            "rate": rate,
                            "is_compound": is_compound == "복리",
                        }
                    )

                elif asset_type == "적금":
                    col_amt, col_mon, col_rate, col_interest = st.columns(
                        [2, 1.5, 1.5, 1]
                    )
                    with col_amt:
                        monthly_amount = st.number_input(
                            "매달 금액 (원)",
                            min_value=0,
                            value=0,
                            step=10000,
                            key=f"{page_type}_new_savings_monthly_amount",
                        )
                    with col_mon:
                        months = st.number_input(
                            "개월 수",
                            min_value=0,
                            value=0,
                            step=1,
                            key=f"{page_type}_new_savings_months",
                        )
                    with col_rate:
                        rate = st.number_input(
                            "금리 (%)",
                            min_value=0.0,
                            max_value=20.0,
                            value=0.0,
                            step=0.1,
                            format="%.2f",
                            key=f"{page_type}_new_savings_rate",
                        )
                    with col_interest:
                        is_compound = st.selectbox(
                            "이자",
                            ["단리", "복리"],
                            index=0,
                            key=f"{page_type}_new_savings_interest_type",
                        )
                    new_item.update(
                        {
                            "monthly_amount": monthly_amount,
                            "months": months,
                            "rate": rate,
                            "is_compound": is_compound == "복리",
                        }
                    )

                elif asset_type == "부동산":
                    value = st.number_input(
                        "가치 (원)",
                        min_value=0,
                        value=0,
                        step=1000000,
                        key=f"{page_type}_new_real_estate_value",
                    )
                    new_item.update({"value": value})

                elif asset_type == "주식":
                    col_amt, col_return = st.columns(2)
                    with col_amt:
                        amount = st.number_input(
                            "금액 (원)",
                            min_value=0,
                            value=0,
                            step=10000,
                            key=f"{page_type}_new_stock_amount",
                        )
                    with col_return:
                        return_rate = st.number_input(
                            "수익률 (%)",
                            min_value=-100.0,
                            max_value=100.0,
                            value=0.0,
                            step=0.5,
                            format="%.2f",
                            key=f"{page_type}_new_stock_return",
                        )
                    new_item.update({"amount": amount, "return_rate": return_rate})

                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button(
                        "저장", key=f"{page_type}_save_asset", use_container_width=True
                    ):
                        st.session_state[assets_key].append(new_item)
                        st.session_state[f"{page_type}_adding_asset"] = False
                        st.rerun()
                with col_cancel:
                    if st.button(
                        "취소",
                        key=f"{page_type}_cancel_asset",
                        use_container_width=True,
                    ):
                        st.session_state[f"{page_type}_adding_asset"] = False
                        st.rerun()

        # 총 자산 (만원 단위로 변환하여 저장)
        total_assets_value = assets_total / 10000  # 만원 단위로 변환
        inputs["total_assets"] = total_assets_value
        inputs["asset_items"] = asset_items

        st.divider()

        # 월 저축/투자 계획 섹션
        st.markdown("**월 저축/투자 계획**")

        # 월 저축/투자 계획 리스트 초기화
        monthly_investment_key = f"{page_type}_monthly_investment_items"
        if monthly_investment_key not in st.session_state:
            st.session_state[monthly_investment_key] = []

        # 월 저축/투자 계획 항목 표시
        monthly_investment_items = st.session_state[monthly_investment_key]

        # 월 저축/투자 계획 합계 계산
        monthly_investment_total = sum(
            item.get("monthly_amount", 0) for item in monthly_investment_items
        )  # 1원 단위
        st.markdown(
            f"**월 합계: {monthly_investment_total:,}원** (만원: {monthly_investment_total / 10000:.1f}만원, 연간: {monthly_investment_total * 12 / 10000:.1f}만원)"
        )

        # 월 저축/투자 계획 항목 표시 및 삭제
        for item in monthly_investment_items:
            asset_type = item.get("type", "")
            col_type, col_info, col_del = st.columns([2, 4, 1])
            with col_type:
                st.text(f"{asset_type}")
            with col_info:
                monthly_amount = item.get("monthly_amount", 0)
                if asset_type == "예금":
                    rate = item.get("rate", 0.0)
                    st.text(f"월 {monthly_amount:,}원, 예상 금리 {rate:.2f}%")
                elif asset_type == "적금":
                    rate = item.get("rate", 0.0)
                    st.text(f"월 {monthly_amount:,}원, 예상 금리 {rate:.2f}%")
                elif asset_type == "부동산":
                    st.text(f"월 {monthly_amount:,}원")
                elif asset_type == "주식":
                    return_rate = item.get("return_rate", 0.0)
                    st.text(f"월 {monthly_amount:,}원, 예상 수익률 {return_rate:.2f}%")
            with col_del:
                if st.button(
                    "삭제",
                    key=f"{page_type}_monthly_investment_del_{item['id']}",
                    use_container_width=True,
                ):
                    st.session_state[monthly_investment_key] = [
                        i for i in monthly_investment_items if i["id"] != item["id"]
                    ]
                    st.rerun()

        # 월 저축/투자 계획 추가 버튼
        if st.button(
            "➕ 월 저축/투자 계획 추가",
            key=f"{page_type}_add_monthly_investment",
            use_container_width=True,
        ):
            st.session_state[f"{page_type}_adding_monthly_investment"] = True

        # 월 저축/투자 계획 추가 입력 폼
        if st.session_state.get(f"{page_type}_adding_monthly_investment", False):
            with st.container():
                investment_type = st.selectbox(
                    "자산 타입",
                    ASSET_TYPES,
                    key=f"{page_type}_new_monthly_investment_type",
                )

                new_item = {"id": str(uuid.uuid4()), "type": investment_type}

                col_amt = st.columns(1)[0]
                with col_amt:
                    monthly_amount = st.number_input(
                        "월 투자 금액 (원)",
                        min_value=0,
                        value=0,
                        step=10000,
                        key=f"{page_type}_new_monthly_investment_amount",
                    )
                    new_item["monthly_amount"] = monthly_amount

                    if investment_type in ["예금", "적금"]:
                        rate = st.number_input(
                            "예상 금리 (%)",
                            min_value=0.0,
                            max_value=20.0,
                            value=0.0,
                            step=0.1,
                            format="%.2f",
                            key=f"{page_type}_new_monthly_investment_rate",
                        )
                        new_item["rate"] = rate
                    elif investment_type == "주식":
                        return_rate = st.number_input(
                            "예상 수익률 (%)",
                            min_value=-100.0,
                            max_value=100.0,
                            value=0.0,
                            step=0.5,
                            format="%.2f",
                            key=f"{page_type}_new_monthly_investment_return_rate",
                        )
                        new_item["return_rate"] = return_rate

                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button(
                        "저장",
                        key=f"{page_type}_save_monthly_investment",
                        use_container_width=True,
                    ):
                        st.session_state[monthly_investment_key].append(new_item)
                        st.session_state[f"{page_type}_adding_monthly_investment"] = (
                            False
                        )
                        st.rerun()
                with col_cancel:
                    if st.button(
                        "취소",
                        key=f"{page_type}_cancel_monthly_investment",
                        use_container_width=True,
                    ):
                        st.session_state[f"{page_type}_adding_monthly_investment"] = (
                            False
                        )
                        st.rerun()

        # 월 저축/투자 계획 정보를 inputs에 저장 (만원 단위)
        monthly_investment_total_won = (
            monthly_investment_total / 10000
        )  # 만원 단위로 변환
        inputs["monthly_investment_items"] = monthly_investment_items
        inputs["monthly_investment_total"] = monthly_investment_total_won

        st.divider()

        # 부채 및 대출 정보 섹션
        st.markdown("**부채 및 대출 정보**")

        # 대출 항목 리스트 초기화
        debt_items_key = f"{page_type}_debt_items"
        if debt_items_key not in st.session_state:
            st.session_state[debt_items_key] = []

        # 대출 항목 표시
        debt_items = st.session_state[debt_items_key]

        # 대출 원금 합계 계산
        # 주의: 이미 저장된 값은 단위 변환이 완료된 것이므로, 다시 변환하지 않음
        # 단, 기존 데이터 호환성을 위해 변환이 필요한 경우만 처리
        total_debt_from_items = 0
        needs_update = False  # 업데이트가 필요한지 추적

        for item in debt_items:
            # 기간이 지난 대출은 계산에서 제외 (remaining_months <= 0)
            remaining_months = item.get("remaining_months", 0)
            if remaining_months is not None and remaining_months <= 0:
                continue  # 기간이 지난 대출은 원금 합계에 포함하지 않음

            principal = item.get("principal", 0)

            # 이미 변환된 값인지 확인 (_normalized 플래그가 있거나 값이 정상 범위)
            is_normalized = item.get("_normalized", False)

            # 원금 값이 비정상적으로 큰 경우 (예: 원 단위로 입력된 기존 데이터)
            # 일반적인 대출 원금 범위: 1만원 ~ 10억만원 (만원 단위 기준)
            # 값이 100,000만원(100억원) 이상이면 원 단위로 입력된 것으로 간주
            if (
                not is_normalized and principal >= 100000
            ):  # 10억원 이상 (100,000만원 이상)
                # 원 단위를 만원 단위로 변환 (예: 150000000원 -> 15000만원)
                principal = principal / 10000
                item["principal"] = principal
                item["_normalized"] = True
                needs_update = True

            total_debt_from_items += principal

        # 월 상환액 합계 계산 (만원 단위)
        # 기간이 지난 대출은 계산에서 제외
        total_monthly_debt_payment = 0
        for item in debt_items:
            # 기간이 지난 대출은 월 상환액에도 포함하지 않음
            remaining_months = item.get("remaining_months", 0)
            if remaining_months is not None and remaining_months <= 0:
                continue  # 기간이 지난 대출은 월 상환액에 포함하지 않음

            monthly_payment = item.get("monthly_payment", 0)
            principal = item.get("principal", 0)
            is_normalized = item.get("_normalized", False)

            # 월 상환액이 비정상적으로 큰 경우 검증 (기존 데이터 호환성)
            # 일반적인 월 상환액 범위: 1만원 ~ 500만원 (만원 단위 기준)
            if not is_normalized and monthly_payment >= 500:  # 500만원 이상
                # 원 단위를 만원 단위로 변환 (예: 275000원 -> 27.5만원)
                monthly_payment = monthly_payment / 10000
                item["monthly_payment"] = monthly_payment
                item["_normalized"] = True
                needs_update = True
            elif (
                not is_normalized
                and item.get("repayment_type") == "만기 원금 상환"
                and monthly_payment > principal * 0.1
                and principal > 0
            ):
                # 만기 원금 상환인데 월 상환액이 원금의 10% 이상이면 원 단위로 간주
                monthly_payment = monthly_payment / 10000
                item["monthly_payment"] = monthly_payment
                item["_normalized"] = True
                needs_update = True

            total_monthly_debt_payment += monthly_payment

        # session state 업데이트 (변환이 실제로 일어난 경우에만, 한 번만)
        if needs_update:
            st.session_state[debt_items_key] = debt_items

        # 대출 항목이 있으면 표시 (기간이 지난 대출 제외)
        # 기간이 지난 대출 필터링 (remaining_months > 0 또는 없으면 표시)
        active_debt_items = [
            item
            for item in debt_items
            if item.get("remaining_months", 0) > 0
            or item.get("remaining_months") is None
        ]

        if active_debt_items:
            st.markdown(
                f"**등록된 대출: {len(active_debt_items)}개** (만료된 대출 {len(debt_items) - len(active_debt_items)}개 제외)"
            )
            for idx, item in enumerate(active_debt_items):
                (
                    col_principal,
                    col_rate,
                    col_type,
                    col_jeonse,
                    col_payment,
                    col_months,
                    col_del,
                ) = st.columns([1.8, 1, 1.5, 1, 1.2, 1, 0.8])
                with col_principal:
                    st.text(f"{item.get('principal', 0):,.0f}만원")
                with col_rate:
                    st.text(f"{item.get('interest_rate', 0):.2f}%")
                with col_type:
                    repayment_type = item.get("repayment_type", "만기 원금 상환")
                    st.text(f"{repayment_type}")
                with col_jeonse:
                    is_jeonse = item.get("is_jeonse", False)
                    st.text("전세" if is_jeonse else "-")
                with col_payment:
                    st.text(f"월 {item.get('monthly_payment', 0):,.0f}만원")
                with col_months:
                    remaining_months = item.get("remaining_months", 0)
                    total_months = item.get("total_months", remaining_months)
                    if remaining_months and remaining_months > 0:
                        years = remaining_months // 12
                        months = remaining_months % 12
                        if years > 0:
                            st.text(f"{years}년 {months}개월")
                        else:
                            st.text(f"{months}개월")
                    else:
                        st.text("만료")
                    if total_months != remaining_months:
                        st.caption(f"(총 {total_months}개월)")
                with col_del:
                    if st.button(
                        "삭제",
                        key=f"{page_type}_debt_del_{item['id']}",
                        use_container_width=True,
                    ):
                        st.session_state[debt_items_key] = [
                            i for i in debt_items if i["id"] != item["id"]
                        ]
                        st.rerun()
        # 활성 대출이 있는 경우 요약 정보 표시
        if active_debt_items:
            st.info(
                f"**대출 원금 합계: {total_debt_from_items:,.0f}만원** | **월 대출 상환액 합계: {total_monthly_debt_payment:,.0f}만원**"
            )
            if len(debt_items) > len(active_debt_items):
                st.caption(
                    f"💡 만료된 대출 {len(debt_items) - len(active_debt_items)}개는 계산에서 제외되었습니다."
                )
            st.divider()
        elif debt_items:
            # 모든 대출이 만료된 경우
            st.info(f"⚠️ 등록된 대출 {len(debt_items)}개가 모두 만료되었습니다.")
            st.info(
                f"**만료된 대출 원금 합계: {total_debt_from_items:,.0f}만원** | **만료된 대출은 계산에서 제외됩니다.**"
            )
            st.divider()

        # 대출 추가 버튼
        if st.button(
            "➕ 대출 추가", key=f"{page_type}_add_debt", use_container_width=True
        ):
            st.session_state[f"{page_type}_adding_debt"] = True

        # 대출 추가 입력 폼
        if st.session_state.get(f"{page_type}_adding_debt", False):
            with st.container():
                st.markdown("**새 대출 입력**")

                # 총 금액 (원 단위 입력)
                debt_principal = st.number_input(
                    "총 금액 (원)",
                    min_value=0,
                    value=0,
                    step=1,
                    key=f"{page_type}_new_debt_principal",
                    help="대출 원금 총액 (원 단위로 입력)",
                    format="%d",
                )

                col_rate, col_type = st.columns(2)
                with col_rate:
                    debt_interest_rate = st.number_input(
                        "이자율 (%)",
                        min_value=0.0,
                        max_value=20.0,
                        value=3.0,
                        step=0.1,
                        key=f"{page_type}_new_debt_interest_rate",
                        help="연 이자율",
                    )
                with col_type:
                    debt_repayment_type = st.selectbox(
                        "상환 방법",
                        DEBT_REPAYMENT_TYPES,
                        key=f"{page_type}_new_debt_repayment_type",
                        help="만기 원금 상환: 매월 이자만 납입, 만기에 원금 일시 상환",
                    )

                # 전세자금 대출 여부 체크
                is_jeonse = st.checkbox(
                    "전세자금 대출",
                    value=False,
                    key=f"{page_type}_new_debt_is_jeonse",
                    help="전세자금 대출인 경우 만기에 원금 일시 상환됩니다",
                )

                # 총 개월
                debt_total_months = st.number_input(
                    "총 개월",
                    min_value=1,
                    value=120,
                    step=1,
                    key=f"{page_type}_new_debt_total_months",
                    help="대출 총 상환 기간 (개월)",
                )

                # 전세자금 대출이면 자동으로 만기 원금 상환으로 설정
                if is_jeonse:
                    debt_repayment_type = "만기 원금 상환"
                    st.info(
                        "💡 전세자금 대출은 자동으로 '만기 원금 상환' 방식으로 설정됩니다."
                    )

                # 월 상환액 계산 및 안내 (원 단위 기준으로 계산 후 만원 단위로 표시)
                monthly_payment = 0.0
                if debt_principal > 0 and debt_interest_rate > 0:
                    # 원 단위 기준으로 계산
                    principal_in_won = debt_principal
                    if debt_repayment_type == "만기 원금 상환":
                        # 만기 원금 상환: 매월 이자만 납입 (원 단위)
                        monthly_payment_won = (
                            principal_in_won * debt_interest_rate / 100
                        ) / 12
                        monthly_payment = (
                            monthly_payment_won / 10000
                        )  # 만원 단위로 변환 (저장용)
                        st.info(
                            f"💡 월 상환액 (이자): 약 {monthly_payment:.0f}만원 ({monthly_payment_won:,.0f}원) | "
                            f"만기 시 원금 {principal_in_won:,.0f}원 ({principal_in_won/10000:.0f}만원) 일시 상환"
                        )
                    elif debt_repayment_type == "균등 상환":
                        # 균등 상환: 원리금 균등 상환 계산 (원 단위 기준)
                        if debt_total_months > 0:
                            monthly_rate = debt_interest_rate / 100 / 12
                            if monthly_rate > 0:
                                annuity_factor = (
                                    (1 + monthly_rate) ** debt_total_months - 1
                                ) / (
                                    monthly_rate
                                    * (1 + monthly_rate) ** debt_total_months
                                )
                                monthly_payment_won = (
                                    principal_in_won / annuity_factor
                                    if annuity_factor > 0
                                    else 0
                                )
                                monthly_payment = (
                                    monthly_payment_won / 10000
                                )  # 만원 단위로 변환 (저장용)
                                st.info(
                                    f"💡 월 상환액: 약 {monthly_payment:.0f}만원 ({monthly_payment_won:,.0f}원) "
                                    f"(원금+이자 균등 상환, {debt_total_months}개월)"
                                )
                    elif debt_repayment_type == "분할 상환":
                        # 분할 상환: 원금 균등 + 이자 (원 단위 기준)
                        principal_per_month_won = (
                            principal_in_won / debt_total_months
                            if debt_total_months > 0
                            else 0
                        )
                        interest_first_month_won = (
                            principal_in_won * debt_interest_rate / 100
                        ) / 12
                        monthly_payment_won = (
                            principal_per_month_won + interest_first_month_won
                        )
                        monthly_payment = (
                            monthly_payment_won / 10000
                        )  # 만원 단위로 변환 (저장용)
                        st.info(
                            f"💡 초기 월 상환액: 약 {monthly_payment:.0f}만원 ({monthly_payment_won:,.0f}원) "
                            f"(원금 {principal_per_month_won/10000:.0f}만원 + 이자 {interest_first_month_won/10000:.0f}만원, 점차 감소)"
                        )

                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button(
                        "저장", key=f"{page_type}_save_debt", use_container_width=True
                    ):
                        if debt_principal == 0:
                            st.error("총 금액을 입력해주세요.")
                        elif debt_total_months <= 0:
                            st.error("총 개월을 입력해주세요.")
                        else:
                            # 원 단위 입력값을 만원 단위로 변환하여 저장 (내부 계산은 만원 단위로 통일)
                            principal_in_manwon = (
                                debt_principal / 10000
                            )  # 원 → 만원 변환

                            # 대출 이름 생성 (전세자금 대출 여부에 따라)
                            if is_jeonse:
                                debt_name = f"전세자금대출 ({debt_total_months}개월)"
                            else:
                                debt_name = f"대출 ({debt_total_months}개월)"

                            new_debt_item = {
                                "id": str(uuid.uuid4()),
                                "name": debt_name,
                                "principal": principal_in_manwon,  # 만원 단위로 저장 (원 단위 입력값 변환)
                                "interest_rate": debt_interest_rate,
                                "repayment_type": debt_repayment_type,
                                "monthly_payment": monthly_payment,  # 계산된 월 상환액 (만원 단위)
                                "remaining_months": debt_total_months,  # 총 개월
                                "total_months": debt_total_months,  # 총 개월 저장 (참조용)
                                "is_jeonse": is_jeonse,  # 전세자금 대출 여부
                                "_normalized": True,  # 단위 변환 완료 플래그
                            }
                            st.session_state[debt_items_key].append(new_debt_item)
                            st.session_state[f"{page_type}_adding_debt"] = False
                            st.rerun()
                with col_cancel:
                    if st.button(
                        "취소",
                        key=f"{page_type}_cancel_debt",
                        use_container_width=True,
                    ):
                        st.session_state[f"{page_type}_adding_debt"] = False
                        st.rerun()

        st.divider()

        # 총 부채 입력 (대출 항목 외 다른 부채 포함)
        other_debt = st.number_input(
            "기타 부채 (만원)",
            min_value=0,
            value=st.session_state.get(f"{page_type}_other_debt", 0),
            step=100,
            key=f"{page_type}_other_debt",
            help="대출 항목 외 카드 빚, 기타 부채 등",
        )

        # 총 부채 = 대출 원금 합계 + 기타 부채
        total_debt = total_debt_from_items + other_debt

        # 총 부채 표시
        if total_debt > 0:
            st.markdown(
                f"**💰 총 부채: {total_debt:,.0f}만원** (대출 원금: {total_debt_from_items:,.0f}만원 + 기타 부채: {other_debt:,.0f}만원)"
            )

        inputs["total_debt"] = total_debt
        inputs["debt_items"] = debt_items
        inputs["total_monthly_debt_payment"] = total_monthly_debt_payment

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
            help="연간 물가 상승률입니다. 기본값은 2.5%입니다.",
        )
        inputs["inflation_rate"] = inflation_rate

    with col_setting2:
        # 은퇴 후 생활비 계산 (가구 형태에 따라 동적 기본값)
        current_monthly_total = (
            monthly_fixed_expense_value + monthly_variable_expense_value
        )
        # 가구 형태는 세션 상태에서 가져오되, 없으면 inputs에서 가져옴
        marital_status = st.session_state.get(
            f"{page_type}_marital_status",
            inputs.get("marital_status", "부부(2인 가구)"),
        )

        # 가구 형태에 따른 평균값 설정
        if marital_status == "부부(2인 가구)":
            avg_retirement_expense = 318  # 만원 단위 (부부 기준 평균)
            min_expense = 200  # 최소값
            max_expense = 500  # 최대값
            help_text = (
                "은퇴 후 예상 월 생활비입니다. 평균값: 부부 기준 월 318만원 (평균)"
            )
        else:  # 1인 가구
            avg_retirement_expense = 170  # 만원 단위 (1인 가구 평균)
            min_expense = 100  # 최소값
            max_expense = 300  # 최대값
            help_text = (
                "은퇴 후 예상 월 생활비입니다. 평균값: 1인 가구 월 170만원 (평균)"
            )

        # 현재 생활비와 평균값 중 더 적절한 값을 기본값으로 사용
        if current_monthly_total > 0:
            # 현재 생활비를 기준으로 평균값과 비교하여 적절한 값 선택
            default_retirement_expense = max(
                avg_retirement_expense, current_monthly_total * 0.7
            )
        else:
            default_retirement_expense = avg_retirement_expense

        # 가구 형태가 변경되었거나 세션에 값이 없으면 기본값 사용
        session_key = f"{page_type}_retirement_monthly_expense"
        current_marital_status = st.session_state.get(
            f"{page_type}_marital_status", marital_status
        )

        # 가구 형태가 변경되었거나 세션에 값이 없으면 새로운 기본값 사용
        if session_key not in st.session_state:
            # 처음 로드하는 경우
            current_value = default_retirement_expense
        elif current_marital_status != marital_status:
            # 가구 형태가 변경된 경우 - 새로운 기본값 사용
            current_value = default_retirement_expense
        else:
            # 기존 값 사용 (범위 내로 조정)
            existing_value = st.session_state.get(
                session_key, default_retirement_expense
            )
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
            help=help_text,
        )
        inputs["retirement_monthly_expense"] = retirement_monthly_expense

        if current_monthly_total > 0:
            ratio = (retirement_monthly_expense / current_monthly_total) * 100
            st.caption(f"현재 생활비 대비 {ratio:.1f}%")

    with col_setting3:
        avg_medical_expense = 45  # Average for 65+ (monthly)
        retirement_medical_expense = st.slider(
            "은퇴 후 월 의료비 (만원)",
            min_value=0,
            max_value=100,
            value=int(
                st.session_state.get(
                    f"{page_type}_retirement_medical_expense", avg_medical_expense
                )
            ),
            step=5,
            key=f"{page_type}_retirement_medical_expense",
            help=f"은퇴 후 예상되는 추가 의료비입니다. 65세 이상 평균 월 45만원 (통계 기반)",
        )
        inputs["retirement_medical_expense"] = retirement_medical_expense
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
            if field == "total_debt":
                continue  # 부채는 0도 유효한 값
            if field == "bonus":
                continue  # 보너스는 0도 유효한 값
            # 나머지 필드는 0이면 입력되지 않은 것으로 간주
            return False

    return True
