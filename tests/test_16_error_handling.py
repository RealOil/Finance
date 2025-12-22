"""
작업 1.16: 에러 처리 및 사용자 안내 테스트

테스트 항목:
1. safe_calculate 함수 테스트
2. 에러 메시지 생성 테스트
3. 입력값 검증 테스트
"""

import sys
from pathlib import Path
import unittest

# 프로젝트 루트 디렉토리를 경로에 추가
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.utils import (
    safe_calculate,
    get_user_friendly_error_message,
    validate_calculation_inputs
)


class TestErrorHandling(unittest.TestCase):
    """에러 처리 테스트"""
    
    def test_safe_calculate_success(self):
        """정상적인 계산 테스트"""
        def add(a, b):
            return a + b
        
        result, success, error = safe_calculate(add, 1, 2)
        
        self.assertTrue(success)
        self.assertEqual(result, 3)
        self.assertEqual(error, "")
        print("[OK] 정상적인 계산 테스트 통과")
    
    def test_safe_calculate_zero_division(self):
        """0으로 나누기 에러 처리 테스트"""
        def divide(a, b):
            return a / b
        
        result, success, error = safe_calculate(divide, 1, 0)
        
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertIn("0으로 나누기", error)
        print("[OK] 0으로 나누기 에러 처리 테스트 통과")
    
    def test_safe_calculate_value_error(self):
        """ValueError 처리 테스트"""
        def convert_to_int(value):
            return int(value)
        
        result, success, error = safe_calculate(convert_to_int, "invalid")
        
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertIn("입력값 오류", error)
        print("[OK] ValueError 처리 테스트 통과")
    
    def test_safe_calculate_key_error(self):
        """KeyError 처리 테스트"""
        def get_value(data, key):
            return data[key]
        
        result, success, error = safe_calculate(get_value, {}, 'missing_key')
        
        self.assertFalse(success)
        self.assertIsNone(result)
        self.assertIn("필수 데이터 누락", error)
        print("[OK] KeyError 처리 테스트 통과")
    
    def test_get_user_friendly_error_message(self):
        """사용자 친화적인 에러 메시지 생성 테스트"""
        zero_div_error = ZeroDivisionError("division by zero")
        message = get_user_friendly_error_message(zero_div_error)
        
        self.assertIn("0으로 나누기", message)
        print("[OK] 사용자 친화적인 에러 메시지 생성 테스트 통과")
    
    def test_validate_calculation_inputs_valid(self):
        """유효한 입력값 검증 테스트"""
        inputs = {
            'current_age': 30,
            'retirement_age': 60,
            'salary': 5000,
            'monthly_expense': 200,
            'total_assets': 1000,
            'total_debt': 0
        }
        
        is_valid, error = validate_calculation_inputs(inputs)
        
        self.assertTrue(is_valid)
        self.assertEqual(error, "")
        print("[OK] 유효한 입력값 검증 테스트 통과")
    
    def test_validate_calculation_inputs_missing(self):
        """누락된 필수 필드 검증 테스트"""
        inputs = {
            'current_age': 30,
            # 'retirement_age' 누락
            'salary': 5000
        }
        
        is_valid, error = validate_calculation_inputs(inputs)
        
        self.assertFalse(is_valid)
        self.assertIn("필수 입력 항목", error)
        print("[OK] 누락된 필수 필드 검증 테스트 통과")
    
    def test_validate_calculation_inputs_invalid_age(self):
        """잘못된 나이 검증 테스트"""
        inputs = {
            'current_age': 60,
            'retirement_age': 30,  # 현재 나이보다 작음
            'salary': 5000,
            'monthly_expense': 200,
            'total_assets': 1000,
            'total_debt': 0
        }
        
        is_valid, error = validate_calculation_inputs(inputs)
        
        self.assertFalse(is_valid)
        self.assertIn("은퇴 나이는 현재 나이보다 커야", error)
        print("[OK] 잘못된 나이 검증 테스트 통과")
    
    def test_validate_calculation_inputs_negative(self):
        """음수 입력값 검증 테스트"""
        inputs = {
            'current_age': 30,
            'retirement_age': 60,
            'salary': -1000,  # 음수
            'monthly_expense': 200,
            'total_assets': 1000,
            'total_debt': 0
        }
        
        is_valid, error = validate_calculation_inputs(inputs)
        
        self.assertFalse(is_valid)
        self.assertIn("연봉은 0 이상", error)
        print("[OK] 음수 입력값 검증 테스트 통과")


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 60)
    print("작업 1.16: 에러 처리 및 사용자 안내 테스트 시작")
    print("=" * 60)
    
    # 테스트 스위트 생성
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestErrorHandling)
    
    # 테스트 실행
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print("테스트 결과 요약")
    print("=" * 60)
    
    total = result.testsRun
    passed = total - len(result.failures) - len(result.errors)
    failed = len(result.failures) + len(result.errors)
    
    print(f"총 {total}개 테스트 중 {passed}개 통과, {failed}개 실패")
    
    if result.failures:
        print("\n실패한 테스트:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n오류가 발생한 테스트:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if failed == 0:
        print("\n[SUCCESS] 모든 테스트 통과!")
        return True
    else:
        print(f"\n[WARNING] {failed}개 테스트 실패")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

