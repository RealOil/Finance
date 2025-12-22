"""
작업 1.5: 소득 및 지출 계산 로직 테스트

테스트 항목:
1. 미래 자산 추정 테스트
2. 재정 건전성 등급 테스트
3. 월 저축 가능액 계산 테스트
4. 인플레이션 적용 테스트
"""

import sys
from pathlib import Path
import unittest

# 프로젝트 루트 디렉토리를 경로에 추가
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules import calculations


class TestCalculationsIncome(unittest.TestCase):
    """소득 및 지출 계산 로직 테스트"""
    
    def setUp(self):
        """테스트용 기본 입력 데이터"""
        self.sample_inputs = {
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
    
    def test_apply_inflation(self):
        """인플레이션 적용 테스트"""
        # 10년 후 가치 계산
        current_value = 100
        years = 10
        inflation_rate = 2.5
        
        future_value = calculations.apply_inflation(current_value, years, inflation_rate)
        
        # 예상값: 100 * (1.025)^10 ≈ 128.01
        expected_value = 100 * (1.025 ** 10)
        self.assertAlmostEqual(future_value, expected_value, places=2)
        print("[OK] 인플레이션 적용 테스트 통과")
    
    def test_calculate_monthly_savings(self):
        """월 저축 가능액 계산 테스트"""
        inputs = self.sample_inputs.copy()
        
        monthly_savings = calculations.calculate_monthly_savings(inputs)
        
        # 예상값: (5000 + 0) / 12 - 200 = 416.67 - 200 = 216.67
        expected = (5000 / 12) - 200
        self.assertAlmostEqual(monthly_savings, expected, places=2)
        print("[OK] 월 저축 가능액 계산 테스트 통과")
    
    def test_calculate_monthly_savings_negative(self):
        """지출이 소득보다 큰 경우 테스트"""
        inputs = self.sample_inputs.copy()
        inputs['monthly_expense'] = 1000  # 월 지출이 월 소득보다 큼
        
        monthly_savings = calculations.calculate_monthly_savings(inputs)
        
        # 음수여야 함
        self.assertLess(monthly_savings, 0)
        print("[OK] 지출 > 소득 경우 테스트 통과")
    
    def test_calculate_financial_health_grade_a_plus(self):
        """재정 건전성 등급 A+ 테스트"""
        inputs = {
            'salary': 10000,
            'bonus': 0,
            'monthly_expense': 300,  # 연간 3600, 소득 대비 36%
            'annual_fixed_expense': 0,
            'total_assets': 5000,  # 비상금 6개월 이상
            'total_debt': 0
        }
        
        result = calculations.calculate_financial_health_grade(inputs)
        
        self.assertEqual(result['grade'], 'A+')
        self.assertLess(result['expense_ratio'], 50)
        self.assertGreaterEqual(result['emergency_fund_months'], 6)
        self.assertEqual(result['debt_ratio'], 0)
        print("[OK] 재정 건전성 등급 A+ 테스트 통과")
    
    def test_calculate_financial_health_grade_a(self):
        """재정 건전성 등급 A 테스트"""
        inputs = {
            'salary': 10000,
            'bonus': 0,
            'monthly_expense': 400,  # 연간 4800, 소득 대비 48%
            'annual_fixed_expense': 0,
            'total_assets': 2000,  # 비상금 3개월 이상
            'total_debt': 300  # 부채 비율 15%
        }
        
        result = calculations.calculate_financial_health_grade(inputs)
        
        self.assertEqual(result['grade'], 'A')
        self.assertLess(result['expense_ratio'], 60)
        self.assertGreaterEqual(result['emergency_fund_months'], 3)
        self.assertLess(result['debt_ratio'], 20)
        print("[OK] 재정 건전성 등급 A 테스트 통과")
    
    def test_calculate_financial_health_grade_d(self):
        """재정 건전성 등급 D 테스트"""
        inputs = {
            'salary': 5000,
            'bonus': 0,
            'monthly_expense': 500,  # 연간 6000, 소득 대비 120%
            'annual_fixed_expense': 0,
            'total_assets': 100,
            'total_debt': 5000  # 부채 비율 5000%
        }
        
        result = calculations.calculate_financial_health_grade(inputs)
        
        self.assertEqual(result['grade'], 'D')
        print("[OK] 재정 건전성 등급 D 테스트 통과")
    
    def test_calculate_future_assets_basic(self):
        """미래 자산 추정 기본 테스트"""
        inputs = self.sample_inputs.copy()
        
        result = calculations.calculate_future_assets(inputs, years=5)
        
        # 결과 구조 확인
        self.assertIn('current_assets', result)
        self.assertIn('future_assets', result)
        self.assertIn('total_savings', result)
        self.assertIn('yearly_breakdown', result)
        self.assertIn('years', result)
        
        # 현재 자산 확인
        self.assertEqual(result['current_assets'], 1000)
        
        # 연도별 내역 확인
        self.assertEqual(len(result['yearly_breakdown']), 5)
        
        # 미래 자산이 현재 자산보다 커야 함 (저축이 있는 경우)
        self.assertGreaterEqual(result['future_assets'], result['current_assets'])
        
        print("[OK] 미래 자산 추정 기본 테스트 통과")
    
    def test_calculate_future_assets_salary_growth(self):
        """연봉 증가율 반영 테스트"""
        inputs = self.sample_inputs.copy()
        inputs['salary'] = 10000
        inputs['salary_growth_rate'] = 5.0
        
        result = calculations.calculate_future_assets(inputs, years=2)
        
        # 2년차 연봉 확인
        year2_salary = result['yearly_breakdown'][1]['salary']
        expected_salary = 10000 * (1.05 ** 2)
        self.assertAlmostEqual(year2_salary, expected_salary, places=2)
        
        print("[OK] 연봉 증가율 반영 테스트 통과")
    
    def test_calculate_future_assets_inflation(self):
        """인플레이션 반영 테스트"""
        inputs = self.sample_inputs.copy()
        inputs['monthly_expense'] = 100
        
        result = calculations.calculate_future_assets(inputs, years=1, inflation_rate=2.5)
        
        # 1년차 지출 확인 (인플레이션 반영)
        year1_expense = result['yearly_breakdown'][0]['annual_expense']
        expected_expense = 100 * 12 * 1.025
        self.assertAlmostEqual(year1_expense, expected_expense, places=2)
        
        print("[OK] 인플레이션 반영 테스트 통과")
    
    def test_calculate_future_assets_negative_savings(self):
        """저축이 없는 경우 테스트"""
        inputs = self.sample_inputs.copy()
        inputs['monthly_expense'] = 1000  # 월 지출이 월 소득보다 큼
        
        result = calculations.calculate_future_assets(inputs, years=1)
        
        # 자산이 감소해야 함
        self.assertLess(result['future_assets'], result['current_assets'])
        
        print("[OK] 저축이 없는 경우 테스트 통과")


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 60)
    print("작업 1.5: 소득 및 지출 계산 로직 테스트 시작")
    print("=" * 60)
    
    # 테스트 스위트 생성
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCalculationsIncome)
    
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

