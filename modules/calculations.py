"""
계산 로직 모듈

소득, 지출, 자산 기반 계산 로직을 구현합니다.
"""

from typing import Dict, Any, List, Tuple
import math


def apply_inflation(value: float, years: int, inflation_rate: float = 2.5) -> float:
    """
    인플레이션을 반영한 미래 가치 계산
    
    Args:
        value: 현재 가치
        years: 연수
        inflation_rate: 인플레이션율 (%)
        
    Returns:
        float: 인플레이션 반영 후 미래 가치
    """
    if years <= 0:
        return value
    
    future_value = value * ((1 + inflation_rate / 100) ** years)
    return future_value


def calculate_monthly_savings(inputs: Dict[str, Any]) -> float:
    """
    월 저축 가능액 계산
    
    Args:
        inputs: 입력 데이터 딕셔너리
        
    Returns:
        float: 월 저축 가능액 (만원)
    """
    salary = inputs.get('salary', 0)
    bonus = inputs.get('bonus', 0)
    
    # 기존 필드 호환성 (마이그레이션 지원)
    if 'monthly_fixed_expense' in inputs and 'monthly_variable_expense' in inputs:
        monthly_fixed_expense = inputs.get('monthly_fixed_expense', 0)
        monthly_variable_expense = inputs.get('monthly_variable_expense', 0)
        monthly_total_expense = monthly_fixed_expense + monthly_variable_expense
    else:
        # 기존 방식 (하위 호환성)
        monthly_expense = inputs.get('monthly_expense', 0)
        annual_fixed_expense = inputs.get('annual_fixed_expense', 0)
        monthly_total_expense = monthly_expense + (annual_fixed_expense / 12)
    
    # 월 소득 계산
    monthly_income = (salary + bonus) / 12
    
    # 월 저축 가능액
    monthly_savings = monthly_income - monthly_total_expense
    
    return monthly_savings


def calculate_financial_health_grade(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    재정 건전성 등급 평가
    
    등급 기준:
    - A+: 소득 대비 지출 < 50%, 비상금 6개월 이상, 부채 없음
    - A: 소득 대비 지출 < 60%, 비상금 3개월 이상, 부채 비율 < 20%
    - B: 소득 대비 지출 < 70%, 비상금 1개월 이상, 부채 비율 < 40%
    - C: 소득 대비 지출 < 80%, 부채 비율 < 60%
    - D: 그 외
    
    Args:
        inputs: 입력 데이터 딕셔너리
        
    Returns:
        Dict[str, Any]: 재정 건전성 등급 및 상세 정보
    """
    salary = inputs.get('salary', 0)
    bonus = inputs.get('bonus', 0)
    total_assets = inputs.get('total_assets', 0)
    total_debt = inputs.get('total_debt', 0)
    
    # 기존 필드 호환성 (마이그레이션 지원)
    if 'monthly_fixed_expense' in inputs and 'monthly_variable_expense' in inputs:
        monthly_fixed_expense = inputs.get('monthly_fixed_expense', 0)
        monthly_variable_expense = inputs.get('monthly_variable_expense', 0)
        monthly_total_expense = monthly_fixed_expense + monthly_variable_expense
    else:
        # 기존 방식 (하위 호환성)
        monthly_expense = inputs.get('monthly_expense', 0)
        annual_fixed_expense = inputs.get('annual_fixed_expense', 0)
        monthly_total_expense = monthly_expense + (annual_fixed_expense / 12)
    
    # 연간 소득 및 지출 계산
    annual_income = salary + bonus
    annual_expense = monthly_total_expense * 12
    
    # 소득 대비 지출 비율
    expense_ratio = (annual_expense / annual_income * 100) if annual_income > 0 else 0
    
    # 자산 대비 부채 비율
    debt_ratio = (total_debt / total_assets * 100) if total_assets > 0 else 0
    
    # 월 저축 가능액
    monthly_savings = calculate_monthly_savings(inputs)
    
    # 비상금 지속 가능 개월 계산
    net_assets = total_assets - total_debt
    # monthly_total_expense는 위에서 이미 계산됨
    emergency_fund_months = (net_assets / monthly_total_expense) if monthly_total_expense > 0 else 0
    
    # 등급 산출
    grade = 'D'
    
    # A+ 조건
    if (expense_ratio < 50 and 
        emergency_fund_months >= 6 and 
        total_debt == 0):
        grade = 'A+'
    # A 조건
    elif (expense_ratio < 60 and 
          emergency_fund_months >= 3 and 
          debt_ratio < 20):
        grade = 'A'
    # B 조건
    elif (expense_ratio < 70 and 
          emergency_fund_months >= 1 and 
          debt_ratio < 40):
        grade = 'B'
    # C 조건
    elif (expense_ratio < 80 and 
          debt_ratio < 60):
        grade = 'C'
    else:
        grade = 'D'
    
    return {
        'grade': grade,
        'expense_ratio': expense_ratio,
        'debt_ratio': debt_ratio,
        'monthly_savings': monthly_savings,
        'emergency_fund_months': emergency_fund_months,
        'details': {
            'annual_income': annual_income,
            'annual_expense': annual_expense,
            'net_assets': net_assets,
            'total_assets': total_assets,
            'total_debt': total_debt
        }
    }


def calculate_future_assets(
    inputs: Dict[str, Any], 
    years: int = 10,
    inflation_rate: float = 2.5,
    include_post_retirement: bool = True,
    life_expectancy: int = 83
) -> Dict[str, Any]:
    """
    미래 자산 추정
    
    Args:
        inputs: 입력 데이터 딕셔너리
        years: 예측 연수 (기본값: 10년)
        inflation_rate: 인플레이션율 (%)
        
    Returns:
        Dict[str, Any]: 미래 자산 추정 결과
    """
    current_assets = inputs.get('total_assets', 0)
    salary = inputs.get('salary', 0)
    bonus = inputs.get('bonus', 0)
    salary_growth_rate = inputs.get('salary_growth_rate', 3.0)
    
    # 기존 필드 호환성 (마이그레이션 지원)
    if 'monthly_fixed_expense' in inputs and 'monthly_variable_expense' in inputs:
        monthly_fixed_expense = inputs.get('monthly_fixed_expense', 0)
        monthly_variable_expense = inputs.get('monthly_variable_expense', 0)
    else:
        # 기존 방식 (하위 호환성)
        monthly_expense = inputs.get('monthly_expense', 0)
        annual_fixed_expense = inputs.get('annual_fixed_expense', 0)
        # 기존 값을 새 구조로 변환 (대략적 추정)
        monthly_fixed_from_annual = annual_fixed_expense / 12
        monthly_fixed_expense = monthly_expense * 0.6 + monthly_fixed_from_annual
        monthly_variable_expense = monthly_expense * 0.4
    
    # 초기값 설정
    assets = current_assets
    current_salary = salary
    
    # 연도별 상세 내역
    yearly_breakdown = []
    current_age = inputs.get('current_age', 30)
    retirement_age = inputs.get('retirement_age', 60)
    
    # 은퇴 전 기간만 계산
    years_to_retirement = retirement_age - current_age if retirement_age > current_age else years
    actual_years = min(years, years_to_retirement) if years_to_retirement > 0 else years
    
    for year in range(1, actual_years + 1):
        # 연봉 증가 반영
        current_salary = current_salary * (1 + salary_growth_rate / 100)
        
        # 연간 소득
        annual_income = current_salary + bonus
        
        # 인플레이션 반영한 월간 지출
        inflated_monthly_fixed = apply_inflation(monthly_fixed_expense, year, inflation_rate)
        inflated_monthly_variable = apply_inflation(monthly_variable_expense, year, inflation_rate)
        inflated_monthly_total = inflated_monthly_fixed + inflated_monthly_variable
        annual_expense = inflated_monthly_total * 12
        
        # 연간 순 저축액
        annual_savings = annual_income - annual_expense
        
        # 자산 증가
        assets = assets + annual_savings
        
        # 연도별 상세 내역 저장
        yearly_breakdown.append({
            'year': year,
            'age': current_age + year,
            'salary': current_salary,
            'annual_income': annual_income,
            'annual_expense': annual_expense,
            'annual_savings': annual_savings,
            'assets': assets,
            'is_retired': False
        })
    
    # 은퇴 후 기간 계산 (평균 수명까지)
    if include_post_retirement and retirement_age > current_age and actual_years >= years_to_retirement:
        years_after_retirement = life_expectancy - retirement_age
        
        # 은퇴 후 생활비 정보
        retirement_monthly_expense = inputs.get('retirement_monthly_expense', 0)
        retirement_medical_expense = inputs.get('retirement_medical_expense', 45)
        
        # 은퇴 후 생활비 계산
        if retirement_monthly_expense > 0:
            monthly_expense_base = retirement_monthly_expense
        else:
            monthly_total_expense = monthly_fixed_expense + monthly_variable_expense
            retirement_expense_ratio = inputs.get('retirement_expense_ratio', 80.0) / 100.0
            monthly_expense_base = monthly_total_expense * retirement_expense_ratio
        
        # 은퇴 후 기간 계산
        for year_after in range(1, years_after_retirement + 1):
            total_year = actual_years + year_after
            
            # 은퇴 후에는 소득 없음
            annual_income = 0
            
            # 은퇴 후 생활비 (인플레이션 반영)
            monthly_expense_inflated = apply_inflation(
                monthly_expense_base,
                years_to_retirement + year_after,
                inflation_rate
            )
            
            # 의료비 (인플레이션 반영)
            medical_expense_inflated = apply_inflation(
                retirement_medical_expense,
                years_to_retirement + year_after,
                inflation_rate
            )
            
            # 연간 지출
            annual_expense = (monthly_expense_inflated + medical_expense_inflated) * 12
            
            # 자산 감소
            annual_savings = -annual_expense  # 음수 (지출)
            assets = assets + annual_savings
            
            # 자산이 0 이하가 되면 중단
            if assets <= 0:
                assets = 0
                yearly_breakdown.append({
                    'year': total_year,
                    'age': retirement_age + year_after,
                    'salary': 0,
                    'annual_income': 0,
                    'annual_expense': annual_expense,
                    'annual_savings': annual_savings,
                    'assets': assets,
                    'is_retired': True
                })
                break
            
            # 연도별 상세 내역 저장
            yearly_breakdown.append({
                'year': total_year,
                'age': retirement_age + year_after,
                'salary': 0,
                'annual_income': 0,
                'annual_expense': annual_expense,
                'annual_savings': annual_savings,
                'assets': assets,
                'is_retired': True
            })
    
    # 총 저축액 계산
    total_savings = assets - current_assets
    
    return {
        'current_assets': current_assets,
        'future_assets': assets,
        'total_savings': total_savings,
        'yearly_breakdown': yearly_breakdown,
        'years': years
    }


def calculate_income_interruption_survival(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    소득 중단 생존 기간 계산
    
    Args:
        inputs: 입력 데이터 딕셔너리
        
    Returns:
        Dict[str, Any]: 소득 중단 생존 기간 정보
    """
    total_assets = inputs.get('total_assets', 0)
    total_debt = inputs.get('total_debt', 0)
    
    # 기존 필드 호환성 (마이그레이션 지원)
    if 'monthly_fixed_expense' in inputs and 'monthly_variable_expense' in inputs:
        monthly_fixed_expense = inputs.get('monthly_fixed_expense', 0)
        monthly_variable_expense = inputs.get('monthly_variable_expense', 0)
        monthly_total_expense = monthly_fixed_expense + monthly_variable_expense
    else:
        # 기존 방식 (하위 호환성)
        monthly_expense = inputs.get('monthly_expense', 0)
        annual_fixed_expense = inputs.get('annual_fixed_expense', 0)
        monthly_total_expense = monthly_expense + (annual_fixed_expense / 12)
    
    # 순자산 계산
    net_assets = total_assets - total_debt
    
    # 생존 가능 개월 계산
    if monthly_total_expense > 0:
        survival_months = net_assets / monthly_total_expense
        survival_years = survival_months / 12
    else:
        survival_months = float('inf')
        survival_years = float('inf')
    
    # 상태 판단
    if survival_months >= 6:
        status = 'safe'
        recommendation = '비상금이 충분합니다. 권장 기준(6개월)을 충족합니다.'
    elif survival_months >= 3:
        status = 'warning'
        recommendation = '비상금이 부족합니다. 최소 6개월치 생활비를 준비하는 것을 권장합니다.'
    else:
        status = 'danger'
        recommendation = '비상금이 매우 부족합니다. 즉시 비상금 마련을 시작하세요.'
    
    return {
        'survival_months': survival_months,
        'survival_years': survival_years,
        'net_assets': net_assets,
        'monthly_expense': monthly_total_expense,
        'status': status,
        'recommendation': recommendation
    }


def calculate_crisis_scenario(
    inputs: Dict[str, Any], 
    asset_drop_rate: float = 30.0
) -> Dict[str, Any]:
    """
    경제 위기 시나리오 계산
    
    Args:
        inputs: 입력 데이터 딕셔너리
        asset_drop_rate: 자산 하락률 (%)
        
    Returns:
        Dict[str, Any]: 경제 위기 시나리오 결과
    """
    total_assets = inputs.get('total_assets', 0)
    total_debt = inputs.get('total_debt', 0)
    
    # 기존 필드 호환성 (마이그레이션 지원)
    if 'monthly_fixed_expense' in inputs and 'monthly_variable_expense' in inputs:
        monthly_fixed_expense = inputs.get('monthly_fixed_expense', 0)
        monthly_variable_expense = inputs.get('monthly_variable_expense', 0)
        monthly_total_expense = monthly_fixed_expense + monthly_variable_expense
    else:
        # 기존 방식 (하위 호환성)
        monthly_expense = inputs.get('monthly_expense', 0)
        annual_fixed_expense = inputs.get('annual_fixed_expense', 0)
        monthly_total_expense = monthly_expense + (annual_fixed_expense / 12)
    
    # 위기 전 자산
    assets_before = total_assets
    
    # 위기 후 자산
    assets_after = total_assets * (1 - asset_drop_rate / 100)
    
    # 위기 후 순자산
    net_assets_after = assets_after - total_debt
    
    # 생존 가능 개월
    if monthly_total_expense > 0:
        survival_months = net_assets_after / monthly_total_expense
    else:
        survival_months = float('inf')
    
    # 상태 판단
    if survival_months >= 6:
        status = 'safe'
    elif survival_months >= 3:
        status = 'warning'
    else:
        status = 'danger'
    
    return {
        'asset_drop_rate': asset_drop_rate,
        'assets_before': assets_before,
        'assets_after': assets_after,
        'net_assets_after': net_assets_after,
        'survival_months': survival_months,
        'status': status
    }


def calculate_retirement_sustainability(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    은퇴 시 생활비 유지 가능 여부 계산
    
    Args:
        inputs: 입력 데이터 딕셔너리
        
    Returns:
        Dict[str, Any]: 은퇴 시나리오 결과
    """
    current_age = inputs.get('current_age', 30)
    retirement_age = inputs.get('retirement_age', 60)
    life_expectancy_after_retirement = 20  # 기본값: 20년
    inflation_rate = inputs.get('inflation_rate', 2.5)  # 사용자 입력 또는 기본값
    
    # 기존 필드 호환성 (마이그레이션 지원)
    if 'monthly_fixed_expense' in inputs and 'monthly_variable_expense' in inputs:
        monthly_fixed_expense = inputs.get('monthly_fixed_expense', 0)
        monthly_variable_expense = inputs.get('monthly_variable_expense', 0)
        monthly_total_expense = monthly_fixed_expense + monthly_variable_expense
    else:
        # 기존 방식 (하위 호환성)
        monthly_expense = inputs.get('monthly_expense', 0)
        annual_fixed_expense = inputs.get('annual_fixed_expense', 0)
        monthly_total_expense = monthly_expense + (annual_fixed_expense / 12)
    
    # 은퇴까지 남은 연수
    years_to_retirement = retirement_age - current_age
    
    if years_to_retirement <= 0:
        return {
            'years_to_retirement': 0,
            'expected_assets_at_retirement': 0,
            'monthly_expense_at_retirement': 0,
            'survival_months': 0,
            'survival_years': 0,
            'life_expectancy_after_retirement': life_expectancy_after_retirement,
            'is_sustainable': False,
            'status': 'error',
            'recommendation': '은퇴 나이는 현재 나이보다 커야 합니다.'
        }
    
    # 은퇴 시점 예상 자산 계산
    future_assets_result = calculate_future_assets(inputs, years=years_to_retirement, inflation_rate=inflation_rate)
    expected_assets_at_retirement = future_assets_result['future_assets']
    
    # 은퇴 후 생활비 계산 (개선된 버전 - 평균값 기반, 기혼/미혼 구분)
    # 사용자가 직접 입력한 은퇴 후 생활비 사용 (평균값 기반 기본값 제공)
    retirement_monthly_expense = inputs.get('retirement_monthly_expense', 0)
    
    # 은퇴 후 생활비가 입력되지 않은 경우, 기존 방식 사용 (하위 호환성)
    if retirement_monthly_expense == 0:
        # 기존 방식: 현재 생활비 비율 기반
        retirement_expense_ratio = inputs.get('retirement_expense_ratio', 80.0) / 100.0
        monthly_expense_base = monthly_total_expense * retirement_expense_ratio
    else:
        # 새 방식: 사용자 입력값 사용 (이미 현재 가격 기준)
        monthly_expense_base = retirement_monthly_expense
    
    # 인플레이션 반영 (은퇴 시점까지)
    monthly_expense_inflated = apply_inflation(
        monthly_expense_base, 
        years_to_retirement, 
        inflation_rate
    )
    
    # 추가 의료비 반영 (인플레이션 반영)
    # 65세 이상 평균 의료비: 연평균 543만원 → 월 약 45만원
    retirement_medical_expense = inputs.get('retirement_medical_expense', 45)  # 기본값 45만원
    retirement_medical_expense_inflated = apply_inflation(
        retirement_medical_expense,
        years_to_retirement,
        inflation_rate
    )
    
    monthly_expense_at_retirement = monthly_expense_inflated + retirement_medical_expense_inflated
    
    # 은퇴 후 생존 가능 개월
    if monthly_expense_at_retirement > 0:
        survival_months = expected_assets_at_retirement / monthly_expense_at_retirement
        survival_years = survival_months / 12
    else:
        survival_months = float('inf')
        survival_years = float('inf')
    
    # 지속 가능 여부 판단
    required_months = life_expectancy_after_retirement * 12
    is_sustainable = survival_months >= required_months
    
    # 상태 판단
    if is_sustainable:
        status = 'sustainable'
        recommendation = f'은퇴 후 {life_expectancy_after_retirement}년간 생활비를 유지할 수 있습니다.'
    elif survival_years >= life_expectancy_after_retirement * 0.5:
        status = 'warning'
        recommendation = f'은퇴 후 생활비가 부족할 수 있습니다. 추가 저축이 필요합니다.'
    else:
        status = 'danger'
        recommendation = '은퇴 후 생활비가 크게 부족합니다. 즉시 저축 계획을 수립하세요.'
    
    return {
        'years_to_retirement': years_to_retirement,
        'expected_assets_at_retirement': expected_assets_at_retirement,
        'monthly_expense_at_retirement': monthly_expense_at_retirement,
        'survival_months': survival_months,
        'survival_years': survival_years,
        'life_expectancy_after_retirement': life_expectancy_after_retirement,
        'is_sustainable': is_sustainable,
        'status': status,
        'recommendation': recommendation
    }


def calculate_risk_score(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    위험도 점수 계산
    
    Args:
        inputs: 입력 데이터 딕셔너리
        
    Returns:
        Dict[str, Any]: 위험도 점수 및 상세 정보
    """
    # 소득 중단 생존 기간 점수 (40점)
    income_interruption = calculate_income_interruption_survival(inputs)
    survival_months = income_interruption['survival_months']
    
    if survival_months >= 6:
        income_interruption_score = 0
    elif survival_months >= 3:
        income_interruption_score = 20
    else:
        income_interruption_score = 40
    
    # 부채 비율 점수 (30점)
    total_assets = inputs.get('total_assets', 0)
    total_debt = inputs.get('total_debt', 0)
    
    if total_assets > 0:
        debt_ratio = (total_debt / total_assets) * 100
    else:
        debt_ratio = 100 if total_debt > 0 else 0
    
    if debt_ratio == 0:
        debt_ratio_score = 0
    elif debt_ratio < 20:
        debt_ratio_score = 10
    elif debt_ratio < 40:
        debt_ratio_score = 20
    else:
        debt_ratio_score = 30
    
    # 소득 대비 지출 비율 점수 (20점)
    salary = inputs.get('salary', 0)
    bonus = inputs.get('bonus', 0)
    
    # 기존 필드 호환성 (마이그레이션 지원)
    if 'monthly_fixed_expense' in inputs and 'monthly_variable_expense' in inputs:
        monthly_fixed_expense = inputs.get('monthly_fixed_expense', 0)
        monthly_variable_expense = inputs.get('monthly_variable_expense', 0)
        monthly_total_expense = monthly_fixed_expense + monthly_variable_expense
    else:
        # 기존 방식 (하위 호환성)
        monthly_expense = inputs.get('monthly_expense', 0)
        annual_fixed_expense = inputs.get('annual_fixed_expense', 0)
        monthly_total_expense = monthly_expense + (annual_fixed_expense / 12)
    
    annual_income = salary + bonus
    annual_expense = monthly_total_expense * 12
    
    if annual_income > 0:
        expense_ratio = (annual_expense / annual_income) * 100
    else:
        expense_ratio = 100
    
    if expense_ratio < 50:
        expense_ratio_score = 0
    elif expense_ratio < 70:
        expense_ratio_score = 10
    elif expense_ratio < 90:
        expense_ratio_score = 20
    else:
        expense_ratio_score = 20
    
    # 은퇴 준비도 점수 (10점)
    retirement = calculate_retirement_sustainability(inputs)
    survival_years = retirement.get('survival_years', 0)
    life_expectancy = retirement.get('life_expectancy_after_retirement', 20)
    
    if survival_years >= life_expectancy:
        retirement_readiness_score = 0
    elif survival_years >= life_expectancy * 0.5:
        retirement_readiness_score = 5
    else:
        retirement_readiness_score = 10
    
    # 종합 점수 계산
    total_score = (
        income_interruption_score +
        debt_ratio_score +
        expense_ratio_score +
        retirement_readiness_score
    )
    
    # 위험도 등급
    if total_score < 25:
        risk_level = 'low'
    elif total_score < 50:
        risk_level = 'medium'
    elif total_score < 75:
        risk_level = 'high'
    else:
        risk_level = 'critical'
    
    # 권장사항 생성
    recommendations = []
    if income_interruption_score > 0:
        recommendations.append('비상금을 늘려 소득 중단에 대비하세요.')
    if debt_ratio_score > 0:
        recommendations.append('부채를 줄여 재정 안정성을 높이세요.')
    if expense_ratio_score > 0:
        recommendations.append('지출을 줄여 저축률을 높이세요.')
    if retirement_readiness_score > 0:
        recommendations.append('은퇴 자금 마련을 위해 추가 저축이 필요합니다.')
    
    if not recommendations:
        recommendations.append('현재 재정 상태가 양호합니다. 지속적인 관리를 유지하세요.')
    
    return {
        'total_score': total_score,
        'risk_level': risk_level,
        'breakdown': {
            'income_interruption': income_interruption_score,
            'debt_ratio': debt_ratio_score,
            'expense_ratio': expense_ratio_score,
            'retirement_readiness': retirement_readiness_score
        },
        'recommendations': recommendations
    }


def parse_scenario(scenario_string: str) -> Dict[str, Any]:
    """
    시나리오 문자열 파싱
    
    Args:
        scenario_string: 시나리오 문자열 (예: "지출 10% 감소", "연봉 5% 증가")
        
    Returns:
        Dict[str, Any]: 시나리오 정보
    """
    import re
    
    expense_change = 0.0
    salary_change = 0.0
    description = scenario_string.strip()
    
    # 기본 시나리오
    if scenario_string in ["현재 패턴 유지", "현재 패턴", "기본"]:
        return {
            'expense_change': 0.0,
            'salary_change': 0.0,
            'description': '현재 패턴 유지'
        }
    
    # 지출 변경 파싱
    expense_pattern = r'지출\s*(\d+(?:\.\d+)?)\s*%\s*(감소|증가)'
    expense_match = re.search(expense_pattern, scenario_string)
    if expense_match:
        value = float(expense_match.group(1))
        direction = expense_match.group(2)
        expense_change = -value if direction == '감소' else value
    
    # 연봉 변경 파싱
    salary_pattern = r'연봉\s*(\d+(?:\.\d+)?)\s*%\s*(증가|감소)'
    salary_match = re.search(salary_pattern, scenario_string)
    if salary_match:
        value = float(salary_match.group(1))
        direction = salary_match.group(2)
        salary_change = value if direction == '증가' else -value
    
    return {
        'expense_change': expense_change,
        'salary_change': salary_change,
        'description': description
    }


def calculate_scenario(
    inputs: Dict[str, Any], 
    scenario: Dict[str, Any], 
    years: int = 10
) -> Dict[str, Any]:
    """
    시나리오 적용 계산
    
    Args:
        inputs: 입력 데이터 딕셔너리
        scenario: 시나리오 정보
        years: 예측 연수
        
    Returns:
        Dict[str, Any]: 시나리오 적용 결과
    """
    # 입력 데이터 복사
    modified_inputs = inputs.copy()
    
    # 지출 변경 적용
    expense_change = scenario.get('expense_change', 0.0)
    if expense_change != 0:
        current_expense = modified_inputs.get('monthly_expense', 0)
        modified_inputs['monthly_expense'] = current_expense * (1 + expense_change / 100)
    
    # 연봉 변경 적용 (연봉 증가율에 추가)
    salary_change = scenario.get('salary_change', 0.0)
    if salary_change != 0:
        current_growth_rate = modified_inputs.get('salary_growth_rate', 3.0)
        modified_inputs['salary_growth_rate'] = current_growth_rate + salary_change
    
    # 미래 자산 계산
    # 인플레이션율 가져오기
    inflation_rate = modified_inputs.get('inflation_rate', 2.5)
    future_assets_result = calculate_future_assets(modified_inputs, years=years, inflation_rate=inflation_rate)
    
    return {
        'scenario': scenario,
        'future_assets': future_assets_result['future_assets'],
        'total_savings': future_assets_result['total_savings'],
        'yearly_breakdown': future_assets_result['yearly_breakdown']
    }


def compare_scenarios(
    inputs: Dict[str, Any], 
    scenarios: List[str], 
    years: int = 10
) -> Dict[str, Any]:
    """
    여러 시나리오 비교
    
    Args:
        inputs: 입력 데이터 딕셔너리
        scenarios: 시나리오 문자열 리스트
        years: 예측 연수
        
    Returns:
        Dict[str, Any]: 시나리오 비교 결과
    """
    # 기본 시나리오 계산
    base_scenario = parse_scenario("현재 패턴 유지")
    base_result = calculate_scenario(inputs, base_scenario, years)
    
    # 각 시나리오 계산
    scenario_results = []
    for scenario_str in scenarios:
        scenario = parse_scenario(scenario_str)
        result = calculate_scenario(inputs, scenario, years)
        scenario_results.append({
            'scenario_name': scenario_str,
            'scenario': scenario,
            'future_assets': result['future_assets'],
            'total_savings': result['total_savings'],
            'yearly_breakdown': result['yearly_breakdown']
        })
    
    # 최고/최저 시나리오 찾기
    if scenario_results:
        best_scenario = max(scenario_results, key=lambda x: x['future_assets'])
        worst_scenario = min(scenario_results, key=lambda x: x['future_assets'])
        
        # 차이 계산
        differences = {}
        for result in scenario_results:
            diff = result['future_assets'] - base_result['future_assets']
            differences[result['scenario_name']] = diff
    else:
        best_scenario = None
        worst_scenario = None
        differences = {}
    
    return {
        'base_scenario': {
            'scenario_name': '현재 패턴 유지',
            'future_assets': base_result['future_assets'],
            'total_savings': base_result['total_savings'],
            'yearly_breakdown': base_result['yearly_breakdown']
        },
        'scenarios': scenario_results,
        'comparison': {
            'best_scenario': best_scenario['scenario_name'] if best_scenario else None,
            'worst_scenario': worst_scenario['scenario_name'] if worst_scenario else None,
            'differences': differences
        }
    }


def calculate_retirement_goal(
    inputs: Dict[str, Any],
    monthly_contribution: float,
    annual_return_rate: float,
    withdrawal_rate: float = 4.0
) -> Dict[str, Any]:
    """
    은퇴 자금 목표 계산
    
    은퇴 후 생활비와 의료비를 지속적으로 충당하기 위한 목표 자산을 계산하고,
    매달 저축 금액과 수익률 조합으로 목표 달성 여부를 계산합니다.
    
    Args:
        inputs: 입력 데이터 딕셔너리
        monthly_contribution: 매달 저축 금액 (만원)
        annual_return_rate: 연간 수익률 (%)
        withdrawal_rate: 현금화율 (%) - 기본값 4%
        
    Returns:
        Dict[str, Any]: 은퇴 자금 목표 계산 결과
    """
    current_age = inputs.get('current_age', 30)
    retirement_age = inputs.get('retirement_age', 60)
    current_assets = inputs.get('total_assets', 0)
    retirement_monthly_expense = inputs.get('retirement_monthly_expense', 0)
    retirement_medical_expense = inputs.get('retirement_medical_expense', 0)
    inflation_rate = inputs.get('inflation_rate', 2.5)
    
    # 은퇴까지 남은 연수
    years_to_retirement = retirement_age - current_age
    
    if years_to_retirement <= 0:
        return {
            'target_assets': 0,
            'projected_assets': current_assets,
            'is_achievable': False,
            'shortfall': 0,
            'monthly_contribution': monthly_contribution,
            'annual_return_rate': annual_return_rate,
            'years_to_retirement': 0,
            'error': '은퇴 나이가 현재 나이보다 작거나 같습니다.'
        }
    
    # 은퇴 시점의 월 생활비 (인플레이션 반영)
    monthly_expense_at_retirement = apply_inflation(
        retirement_monthly_expense + retirement_medical_expense,
        years_to_retirement,
        inflation_rate
    )
    
    # 목표 자산 계산 (4% 현금화율 기준)
    # 목표 자산 = 연간 필요 금액 / 현금화율
    annual_expense_needed = monthly_expense_at_retirement * 12
    target_assets = annual_expense_needed / (withdrawal_rate / 100)
    
    # 복리 계산으로 예상 자산 계산
    # FV = PV * (1 + r)^n + PMT * (((1 + r)^n - 1) / r)
    # FV: 미래 가치, PV: 현재 가치, PMT: 매달 저축, r: 월 수익률, n: 기간(월)
    
    monthly_return_rate = annual_return_rate / 100 / 12
    months_to_retirement = years_to_retirement * 12
    
    if monthly_return_rate > 0:
        # 복리 계산
        future_value_from_current = current_assets * ((1 + monthly_return_rate) ** months_to_retirement)
        future_value_from_contributions = monthly_contribution * (((1 + monthly_return_rate) ** months_to_retirement - 1) / monthly_return_rate)
        projected_assets = future_value_from_current + future_value_from_contributions
    else:
        # 수익률이 0인 경우 단순 계산
        projected_assets = current_assets + (monthly_contribution * months_to_retirement)
    
    # 목표 달성 여부
    is_achievable = projected_assets >= target_assets
    shortfall = max(0, target_assets - projected_assets)
    surplus = max(0, projected_assets - target_assets)
    
    return {
        'target_assets': target_assets,
        'projected_assets': projected_assets,
        'is_achievable': is_achievable,
        'shortfall': shortfall,
        'surplus': surplus,
        'monthly_contribution': monthly_contribution,
        'annual_return_rate': annual_return_rate,
        'years_to_retirement': years_to_retirement,
        'monthly_expense_at_retirement': monthly_expense_at_retirement,
        'annual_expense_needed': annual_expense_needed,
        'withdrawal_rate': withdrawal_rate,
        'current_assets': current_assets
    }


def find_optimal_contribution_rate(
    inputs: Dict[str, Any],
    target_return_rate: float,
    withdrawal_rate: float = 4.0
) -> Tuple[float, Dict[str, Any]]:
    """
    목표 수익률에 맞는 최적의 매달 저축 금액 계산
    
    Args:
        inputs: 입력 데이터 딕셔너리
        target_return_rate: 목표 연간 수익률 (%)
        withdrawal_rate: 현금화율 (%) - 기본값 4%
        
    Returns:
        Tuple[float, Dict[str, Any]]: (최적 매달 저축 금액, 계산 결과)
    """
    # 목표 자산 계산
    current_age = inputs.get('current_age', 30)
    retirement_age = inputs.get('retirement_age', 60)
    years_to_retirement = retirement_age - current_age
    
    if years_to_retirement <= 0:
        return 0, {}
    
    retirement_monthly_expense = inputs.get('retirement_monthly_expense', 0)
    retirement_medical_expense = inputs.get('retirement_medical_expense', 0)
    inflation_rate = inputs.get('inflation_rate', 2.5)
    
    monthly_expense_at_retirement = apply_inflation(
        retirement_monthly_expense + retirement_medical_expense,
        years_to_retirement,
        inflation_rate
    )
    
    annual_expense_needed = monthly_expense_at_retirement * 12
    target_assets = annual_expense_needed / (withdrawal_rate / 100)
    
    # 이분 탐색으로 최적 저축 금액 찾기
    current_assets = inputs.get('total_assets', 0)
    monthly_return_rate = target_return_rate / 100 / 12
    months_to_retirement = years_to_retirement * 12
    
    if monthly_return_rate > 0:
        # 복리 공식 역산: PMT = (FV - PV * (1 + r)^n) / (((1 + r)^n - 1) / r)
        future_value_from_current = current_assets * ((1 + monthly_return_rate) ** months_to_retirement)
        required_from_contributions = target_assets - future_value_from_current
        
        if required_from_contributions > 0:
            annuity_factor = (((1 + monthly_return_rate) ** months_to_retirement - 1) / monthly_return_rate)
            optimal_monthly_contribution = required_from_contributions / annuity_factor
        else:
            optimal_monthly_contribution = 0
    else:
        # 수익률이 0인 경우
        required_from_contributions = target_assets - current_assets
        optimal_monthly_contribution = max(0, required_from_contributions / months_to_retirement)
    
    # 계산 결과 생성
    result = calculate_retirement_goal(
        inputs,
        optimal_monthly_contribution,
        target_return_rate,
        withdrawal_rate
    )
    
    return optimal_monthly_contribution, result


def find_required_return_rate(
    inputs: Dict[str, Any],
    monthly_contribution: float,
    withdrawal_rate: float = 4.0
) -> Tuple[float, Dict[str, Any]]:
    """
    매달 저축 금액에 맞는 필요한 수익률 계산
    
    Args:
        inputs: 입력 데이터 딕셔너리
        monthly_contribution: 매달 저축 금액 (만원)
        withdrawal_rate: 현금화율 (%) - 기본값 4%
        
    Returns:
        Tuple[float, Dict[str, Any]]: (필요한 연간 수익률, 계산 결과)
    """
    # 목표 자산 계산
    current_age = inputs.get('current_age', 30)
    retirement_age = inputs.get('retirement_age', 60)
    years_to_retirement = retirement_age - current_age
    
    if years_to_retirement <= 0:
        return 0, {}
    
    retirement_monthly_expense = inputs.get('retirement_monthly_expense', 0)
    retirement_medical_expense = inputs.get('retirement_medical_expense', 0)
    inflation_rate = inputs.get('inflation_rate', 2.5)
    
    monthly_expense_at_retirement = apply_inflation(
        retirement_monthly_expense + retirement_medical_expense,
        years_to_retirement,
        inflation_rate
    )
    
    annual_expense_needed = monthly_expense_at_retirement * 12
    target_assets = annual_expense_needed / (withdrawal_rate / 100)
    
    current_assets = inputs.get('total_assets', 0)
    months_to_retirement = years_to_retirement * 12
    
    # 이분 탐색으로 필요한 수익률 찾기
    # FV = PV * (1 + r)^n + PMT * (((1 + r)^n - 1) / r)
    # target_assets = current_assets * (1 + r)^n + monthly_contribution * (((1 + r)^n - 1) / r)
    
    def calculate_future_value(return_rate: float) -> float:
        """주어진 수익률로 미래 가치 계산"""
        monthly_rate = return_rate / 100 / 12
        if monthly_rate > 0:
            future_value_from_current = current_assets * ((1 + monthly_rate) ** months_to_retirement)
            future_value_from_contributions = monthly_contribution * (((1 + monthly_rate) ** months_to_retirement - 1) / monthly_rate)
            return future_value_from_current + future_value_from_contributions
        else:
            return current_assets + (monthly_contribution * months_to_retirement)
    
    # 이분 탐색으로 필요한 수익률 찾기
    low_rate = 0.0
    high_rate = 20.0  # 최대 20% 수익률
    tolerance = 0.01  # 0.01% 오차 허용
    
    required_rate = 0.0
    for _ in range(100):  # 최대 100번 반복
        mid_rate = (low_rate + high_rate) / 2
        fv = calculate_future_value(mid_rate)
        
        if abs(fv - target_assets) < tolerance:
            required_rate = mid_rate
            break
        elif fv < target_assets:
            low_rate = mid_rate
        else:
            high_rate = mid_rate
    
    # 최종 계산
    if abs(calculate_future_value(required_rate) - target_assets) > tolerance:
        # 목표 달성이 불가능한 경우 (저축 금액이 너무 적음)
        required_rate = high_rate
    
    # 계산 결과 생성
    result = calculate_retirement_goal(
        inputs,
        monthly_contribution,
        required_rate,
        withdrawal_rate
    )
    
    return required_rate, result
