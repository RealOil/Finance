"""
입력 검증 모듈

사용자 입력 데이터의 유효성을 검증하고, 오류 메시지를 제공합니다.
"""

from typing import Dict, Any, Tuple, List


def validate_age(age: int) -> Tuple[bool, str]:
    """
    나이 검증
    
    Args:
        age: 검증할 나이
        
    Returns:
        Tuple[bool, str]: (검증 성공 여부, 오류 메시지)
    """
    if age < 0:
        return False, "나이는 0 이상이어야 합니다."
    if age > 150:
        return False, "나이는 150 이하여야 합니다."
    return True, ""


def validate_retirement_age(current_age: int, retirement_age: int) -> Tuple[bool, str]:
    """
    은퇴 나이 검증
    
    Args:
        current_age: 현재 나이
        retirement_age: 은퇴 나이
        
    Returns:
        Tuple[bool, str]: (검증 성공 여부, 오류 메시지)
    """
    if retirement_age <= current_age:
        return False, f"은퇴 나이({retirement_age}세)는 현재 나이({current_age}세)보다 커야 합니다."
    if retirement_age < 1:
        return False, "은퇴 나이는 1 이상이어야 합니다."
    if retirement_age > 100:
        return False, "은퇴 나이는 100 이하여야 합니다."
    return True, ""


def validate_salary(salary: float) -> Tuple[bool, str]:
    """
    연봉 검증
    
    Args:
        salary: 검증할 연봉 (만원)
        
    Returns:
        Tuple[bool, str]: (검증 성공 여부, 오류 메시지)
    """
    if salary < 0:
        return False, "연봉은 0 이상이어야 합니다."
    if salary > 1000000:  # 10억 만원
        return False, "연봉은 10억 만원 이하여야 합니다."
    return True, ""


def validate_salary_growth_rate(rate: float) -> Tuple[bool, str]:
    """
    연봉 증가율 검증
    
    Args:
        rate: 검증할 연봉 증가율 (%)
        
    Returns:
        Tuple[bool, str]: (검증 성공 여부, 오류 메시지)
    """
    if rate < 0:
        return False, "연봉 증가율은 0 이상이어야 합니다."
    if rate > 20:
        return False, "연봉 증가율은 20% 이하여야 합니다."
    return True, ""


def validate_expense(expense: float) -> Tuple[bool, str]:
    """
    지출 검증
    
    Args:
        expense: 검증할 지출 (만원)
        
    Returns:
        Tuple[bool, str]: (검증 성공 여부, 오류 메시지)
    """
    if expense < 0:
        return False, "지출은 0 이상이어야 합니다."
    return True, ""


def validate_assets(assets: float) -> Tuple[bool, str]:
    """
    자산 검증
    
    Args:
        assets: 검증할 자산 (만원)
        
    Returns:
        Tuple[bool, str]: (검증 성공 여부, 오류 메시지)
    """
    if assets < 0:
        return False, "자산은 0 이상이어야 합니다."
    return True, ""


def validate_debt(debt: float) -> Tuple[bool, str]:
    """
    부채 검증
    
    Args:
        debt: 검증할 부채 (만원)
        
    Returns:
        Tuple[bool, str]: (검증 성공 여부, 오류 메시지)
    """
    if debt < 0:
        return False, "부채는 0 이상이어야 합니다."
    return True, ""


def validate_logical_consistency(inputs: Dict[str, Any]) -> List[str]:
    """
    논리적 일관성 검증
    
    입력 데이터 간의 논리적 일관성을 검증하고 경고 메시지를 반환합니다.
    
    Args:
        inputs: 입력 데이터 딕셔너리
        
    Returns:
        List[str]: 경고 메시지 리스트 (경고가 없으면 빈 리스트)
    """
    warnings = []
    
    current_age = inputs.get('current_age', 0)
    retirement_age = inputs.get('retirement_age', 0)
    salary = inputs.get('salary', 0)
    monthly_expense = inputs.get('monthly_expense', 0)
    total_assets = inputs.get('total_assets', 0)
    total_debt = inputs.get('total_debt', 0)
    
    # 은퇴 나이 검증
    if retirement_age <= current_age:
        warnings.append(f"⚠️ 은퇴 나이({retirement_age}세)가 현재 나이({current_age}세)보다 크지 않습니다.")
    
    # 월 지출이 월 소득보다 큰 경우 경고
    monthly_salary = salary / 12
    # 기존 필드 호환성
    if 'monthly_fixed_expense' in inputs and 'monthly_variable_expense' in inputs:
        monthly_fixed_expense = inputs.get('monthly_fixed_expense', 0)
        monthly_variable_expense = inputs.get('monthly_variable_expense', 0)
        monthly_total_expense = monthly_fixed_expense + monthly_variable_expense
    else:
        monthly_expense = inputs.get('monthly_expense', 0)
        annual_fixed_expense = inputs.get('annual_fixed_expense', 0)
        monthly_total_expense = monthly_expense + (annual_fixed_expense / 12)
    
    if monthly_total_expense > monthly_salary:
        warnings.append(f"⚠️ 월 지출({monthly_total_expense:.0f}만원)이 월 소득({monthly_salary:.0f}만원)보다 큽니다.")
    
    # 부채가 자산보다 큰 경우 경고
    if total_debt > total_assets:
        net_assets = total_assets - total_debt
        warnings.append(f"⚠️ 부채({total_debt:.0f}만원)가 자산({total_assets:.0f}만원)보다 큽니다. 순자산: {net_assets:.0f}만원")
    
    return warnings


def validate_inputs(inputs: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    입력 데이터 전체 검증
    
    모든 입력 필드를 검증하고 오류 메시지 리스트를 반환합니다.
    
    Args:
        inputs: 입력 데이터 딕셔너리
        
    Returns:
        Tuple[bool, List[str]]: (검증 성공 여부, 오류 메시지 리스트)
    """
    errors = []
    
    # 기본 정보 검증
    current_age = inputs.get('current_age')
    if current_age is not None:
        is_valid, error_msg = validate_age(current_age)
        if not is_valid:
            errors.append(error_msg)
    
    retirement_age = inputs.get('retirement_age')
    if retirement_age is not None and current_age is not None:
        is_valid, error_msg = validate_retirement_age(current_age, retirement_age)
        if not is_valid:
            errors.append(error_msg)
    
    # 소득 정보 검증
    salary = inputs.get('salary')
    if salary is not None:
        is_valid, error_msg = validate_salary(salary)
        if not is_valid:
            errors.append(error_msg)
    
    salary_growth_rate = inputs.get('salary_growth_rate')
    if salary_growth_rate is not None:
        is_valid, error_msg = validate_salary_growth_rate(salary_growth_rate)
        if not is_valid:
            errors.append(error_msg)
    
    bonus = inputs.get('bonus')
    if bonus is not None and bonus < 0:
        errors.append("보너스는 0 이상이어야 합니다.")
    
    # 소비 정보 검증 (새 구조 우선)
    monthly_fixed_expense = inputs.get('monthly_fixed_expense')
    if monthly_fixed_expense is not None:
        is_valid, error_msg = validate_expense(monthly_fixed_expense)
        if not is_valid:
            errors.append(f"월간 고정비: {error_msg}")
    
    monthly_variable_expense = inputs.get('monthly_variable_expense')
    if monthly_variable_expense is not None:
        is_valid, error_msg = validate_expense(monthly_variable_expense)
        if not is_valid:
            errors.append(f"월간 변동비: {error_msg}")
    
    # 하위 호환성을 위한 기존 필드 검증
    monthly_expense = inputs.get('monthly_expense')
    if monthly_expense is not None:
        is_valid, error_msg = validate_expense(monthly_expense)
        if not is_valid:
            errors.append(f"월 지출: {error_msg}")
    
    annual_fixed_expense = inputs.get('annual_fixed_expense')
    if annual_fixed_expense is not None:
        is_valid, error_msg = validate_expense(annual_fixed_expense)
        if not is_valid:
            errors.append(f"연간 고정 지출: {error_msg}")
    
    # 자산 및 부채 검증
    total_assets = inputs.get('total_assets')
    if total_assets is not None:
        is_valid, error_msg = validate_assets(total_assets)
        if not is_valid:
            errors.append(error_msg)
    
    total_debt = inputs.get('total_debt')
    if total_debt is not None:
        is_valid, error_msg = validate_debt(total_debt)
        if not is_valid:
            errors.append(error_msg)
    
    # 검증 성공 여부 반환
    is_valid = len(errors) == 0
    return is_valid, errors

