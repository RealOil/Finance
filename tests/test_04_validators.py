"""
작업 1.4: 입력 검증 모듈 테스트

테스트 항목:
1. 기본 검증 테스트
2. 개별 필드 검증 테스트
3. 논리적 일관성 검증 테스트
4. 오류 메시지 테스트
"""

import sys
from pathlib import Path
import unittest

# 프로젝트 루트 디렉토리를 경로에 추가
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules import validators


class TestValidators(unittest.TestCase):
    """입력 검증 모듈 테스트"""
    
    def test_validate_age_valid(self):
        """유효한 나이 검증 테스트"""
        is_valid, error_msg = validators.validate_age(30)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
        print("[OK] 유효한 나이 검증 통과")
    
    def test_validate_age_negative(self):
        """음수 나이 검증 실패 테스트"""
        is_valid, error_msg = validators.validate_age(-1)
        self.assertFalse(is_valid)
        self.assertIn("0 이상", error_msg)
        print("[OK] 음수 나이 검증 실패 통과")
    
    def test_validate_age_too_large(self):
        """너무 큰 나이 검증 실패 테스트"""
        is_valid, error_msg = validators.validate_age(200)
        self.assertFalse(is_valid)
        self.assertIn("150 이하", error_msg)
        print("[OK] 너무 큰 나이 검증 실패 통과")
    
    def test_validate_retirement_age_valid(self):
        """유효한 은퇴 나이 검증 테스트"""
        is_valid, error_msg = validators.validate_retirement_age(30, 60)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
        print("[OK] 유효한 은퇴 나이 검증 통과")
    
    def test_validate_retirement_age_smaller_than_current(self):
        """은퇴 나이가 현재 나이보다 작은 경우 검증 실패 테스트"""
        is_valid, error_msg = validators.validate_retirement_age(30, 25)
        self.assertFalse(is_valid)
        self.assertIn("현재 나이", error_msg)
        print("[OK] 은퇴 나이 < 현재 나이 검증 실패 통과")
    
    def test_validate_retirement_age_equal_to_current(self):
        """은퇴 나이가 현재 나이와 같은 경우 검증 실패 테스트"""
        is_valid, error_msg = validators.validate_retirement_age(30, 30)
        self.assertFalse(is_valid)
        self.assertIn("현재 나이", error_msg)
        print("[OK] 은퇴 나이 = 현재 나이 검증 실패 통과")
    
    def test_validate_salary_valid(self):
        """유효한 연봉 검증 테스트"""
        is_valid, error_msg = validators.validate_salary(5000)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
        print("[OK] 유효한 연봉 검증 통과")
    
    def test_validate_salary_negative(self):
        """음수 연봉 검증 실패 테스트"""
        is_valid, error_msg = validators.validate_salary(-1000)
        self.assertFalse(is_valid)
        self.assertIn("0 이상", error_msg)
        print("[OK] 음수 연봉 검증 실패 통과")
    
    def test_validate_salary_growth_rate_valid(self):
        """유효한 연봉 증가율 검증 테스트"""
        is_valid, error_msg = validators.validate_salary_growth_rate(3.0)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
        print("[OK] 유효한 연봉 증가율 검증 통과")
    
    def test_validate_salary_growth_rate_too_high(self):
        """너무 높은 연봉 증가율 검증 실패 테스트"""
        is_valid, error_msg = validators.validate_salary_growth_rate(25.0)
        self.assertFalse(is_valid)
        self.assertIn("20% 이하", error_msg)
        print("[OK] 너무 높은 연봉 증가율 검증 실패 통과")
    
    def test_validate_inputs_valid(self):
        """유효한 입력 데이터 전체 검증 테스트"""
        inputs = {
            'current_age': 30,
            'retirement_age': 60,
            'salary': 5000,
            'salary_growth_rate': 3.0,
            'bonus': 0,
            'monthly_expense': 200,
            'annual_fixed_expense': 0,
            'total_assets': 1000,
            'total_debt': 0
        }
        is_valid, errors = validators.validate_inputs(inputs)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        print("[OK] 유효한 입력 데이터 전체 검증 통과")
    
    def test_validate_inputs_with_errors(self):
        """오류가 있는 입력 데이터 검증 테스트"""
        inputs = {
            'current_age': -5,
            'retirement_age': 25,
            'salary': -1000,
            'salary_growth_rate': 25.0,
            'bonus': 0,
            'monthly_expense': -100,
            'annual_fixed_expense': 0,
            'total_assets': -500,
            'total_debt': -200
        }
        is_valid, errors = validators.validate_inputs(inputs)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        print(f"[OK] 오류가 있는 입력 데이터 검증 통과 (오류 {len(errors)}개)")
    
    def test_validate_logical_consistency_valid(self):
        """논리적으로 일관된 입력 데이터 검증 테스트"""
        inputs = {
            'current_age': 30,
            'retirement_age': 60,
            'salary': 5000,
            'monthly_expense': 200,
            'total_assets': 1000,
            'total_debt': 500
        }
        warnings = validators.validate_logical_consistency(inputs)
        self.assertEqual(len(warnings), 0)
        print("[OK] 논리적으로 일관된 입력 데이터 검증 통과")
    
    def test_validate_logical_consistency_warnings(self):
        """논리적 경고가 있는 입력 데이터 검증 테스트"""
        inputs = {
            'current_age': 30,
            'retirement_age': 25,  # 현재 나이보다 작음
            'salary': 5000,
            'monthly_expense': 600,  # 월 소득(416.67)보다 큼
            'total_assets': 1000,
            'total_debt': 2000  # 자산보다 큼
        }
        warnings = validators.validate_logical_consistency(inputs)
        self.assertGreater(len(warnings), 0)
        print(f"[OK] 논리적 경고가 있는 입력 데이터 검증 통과 (경고 {len(warnings)}개)")
    
    def test_validate_inputs_boundary_values(self):
        """경계값 검증 테스트"""
        # 최소값
        inputs_min = {
            'current_age': 0,
            'retirement_age': 1,
            'salary': 0,
            'salary_growth_rate': 0.0,
            'bonus': 0,
            'monthly_expense': 0,
            'annual_fixed_expense': 0,
            'total_assets': 0,
            'total_debt': 0
        }
        is_valid, errors = validators.validate_inputs(inputs_min)
        self.assertTrue(is_valid)
        
        # 최대값 (현재 나이가 150이면 은퇴 나이는 100보다 클 수 없으므로 조정)
        inputs_max = {
            'current_age': 99,
            'retirement_age': 100,
            'salary': 1000000,
            'salary_growth_rate': 20.0,
            'bonus': 0,
            'monthly_expense': 100000,
            'annual_fixed_expense': 0,
            'total_assets': 10000000,
            'total_debt': 0
        }
        is_valid, errors = validators.validate_inputs(inputs_max)
        self.assertTrue(is_valid)
        print("[OK] 경계값 검증 통과")


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 60)
    print("작업 1.4: 입력 검증 모듈 테스트 시작")
    print("=" * 60)
    
    # 테스트 스위트 생성
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestValidators)
    
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

