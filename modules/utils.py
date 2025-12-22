"""
유틸리티 모듈

에러 처리 및 안전한 계산을 위한 유틸리티 함수를 제공합니다.
"""

from typing import Callable, Any, Dict, Tuple
import traceback


def safe_calculate(
    func: Callable,
    *args,
    error_message: str = "계산 중 오류가 발생했습니다.",
    **kwargs
) -> Tuple[Any, bool, str]:
    """
    안전한 계산 래퍼 함수
    
    계산 함수를 실행하고 에러를 안전하게 처리합니다.
    
    Args:
        func: 실행할 계산 함수
        *args: 함수에 전달할 위치 인자
        error_message: 기본 에러 메시지
        **kwargs: 함수에 전달할 키워드 인자
        
    Returns:
        Tuple[Any, bool, str]: (결과, 성공 여부, 에러 메시지)
            - 결과: 계산 결과 (성공 시) 또는 None (실패 시)
            - 성공 여부: True (성공) 또는 False (실패)
            - 에러 메시지: 에러 발생 시 사용자 친화적인 메시지
    """
    try:
        result = func(*args, **kwargs)
        return result, True, ""
    except ZeroDivisionError:
        error_msg = "0으로 나누기를 시도했습니다. 입력값을 확인해주세요."
        return None, False, error_msg
    except ValueError as e:
        error_msg = f"입력값 오류: {str(e)}. 올바른 값을 입력해주세요."
        return None, False, error_msg
    except TypeError as e:
        error_msg = f"데이터 타입 오류: {str(e)}. 입력 형식을 확인해주세요."
        return None, False, error_msg
    except KeyError as e:
        error_msg = f"필수 데이터 누락: {str(e)}. 모든 필수 항목을 입력해주세요."
        return None, False, error_msg
    except Exception as e:
        # 예상치 못한 오류
        error_msg = f"{error_message} 오류 내용: {str(e)}"
        # 개발 환경에서만 상세 정보 표시
        # traceback.print_exc()  # 필요시 주석 해제
        return None, False, error_msg


def get_user_friendly_error_message(error: Exception) -> str:
    """
    사용자 친화적인 에러 메시지 생성
    
    Args:
        error: 발생한 예외 객체
        
    Returns:
        str: 사용자 친화적인 에러 메시지
    """
    error_type = type(error).__name__
    
    error_messages = {
        'ZeroDivisionError': "0으로 나누기를 시도했습니다. 입력값을 확인해주세요.",
        'ValueError': f"입력값 오류: {str(error)}. 올바른 값을 입력해주세요.",
        'TypeError': f"데이터 타입 오류: {str(error)}. 입력 형식을 확인해주세요.",
        'KeyError': f"필수 데이터 누락: {str(error)}. 모든 필수 항목을 입력해주세요.",
        'IndexError': "데이터 인덱스 오류가 발생했습니다. 입력값을 확인해주세요.",
        'AttributeError': f"데이터 속성 오류: {str(error)}. 입력 형식을 확인해주세요."
    }
    
    return error_messages.get(error_type, f"계산 중 오류가 발생했습니다: {str(error)}")


def validate_calculation_inputs(inputs: Dict[str, Any]) -> Tuple[bool, str]:
    """
    계산 전 입력값 검증
    
    Args:
        inputs: 입력 데이터 딕셔너리
        
    Returns:
        Tuple[bool, str]: (검증 통과 여부, 에러 메시지)
    """
    # 필수 필드 확인 (기본 필드)
    required_fields = [
        'current_age', 'retirement_age', 'salary',
        'total_assets', 'total_debt'
    ]
    
    missing_fields = []
    for field in required_fields:
        if field not in inputs or inputs[field] is None:
            missing_fields.append(field)
    
    # 지출 정보는 새 구조 또는 기존 구조 중 하나는 필수
    has_new_structure = 'monthly_fixed_expense' in inputs and 'monthly_variable_expense' in inputs
    has_old_structure = 'monthly_expense' in inputs
    if not (has_new_structure or has_old_structure):
        missing_fields.append("월간 고정비/변동비 또는 월 지출")
    
    if missing_fields:
        return False, f"필수 입력 항목이 누락되었습니다: {', '.join(missing_fields)}"
    
    # 논리적 검증
    if inputs['current_age'] >= inputs['retirement_age']:
        return False, "은퇴 나이는 현재 나이보다 커야 합니다."
    
    if inputs['salary'] < 0:
        return False, "연봉은 0 이상이어야 합니다."
    
    # 새 구조 필드 검증
    if 'monthly_fixed_expense' in inputs and inputs.get('monthly_fixed_expense', 0) < 0:
        return False, "월간 고정비는 0 이상이어야 합니다."
    if 'monthly_variable_expense' in inputs and inputs.get('monthly_variable_expense', 0) < 0:
        return False, "월간 변동비는 0 이상이어야 합니다."
    # 하위 호환성
    if 'monthly_expense' in inputs and inputs.get('monthly_expense', 0) < 0:
        return False, "월 지출은 0 이상이어야 합니다."
    
    if inputs['total_assets'] < 0:
        return False, "총 자산은 0 이상이어야 합니다."
    
    if inputs['total_debt'] < 0:
        return False, "총 부채는 0 이상이어야 합니다."
    
    return True, ""

