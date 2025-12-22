"""
작업 1.7: 시나리오 비교 계산 로직 테스트

테스트 항목:
1. 시나리오 파싱 테스트
2. 시나리오 계산 테스트
3. 여러 시나리오 비교 테스트
"""

import sys
from pathlib import Path
import unittest

# 프로젝트 루트 디렉토리를 경로에 추가
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules import calculations


class TestCalculationsScenario(unittest.TestCase):
    """시나리오 비교 계산 로직 테스트"""
    
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
    
    def test_parse_scenario_current_pattern(self):
        """시나리오 파싱 - 현재 패턴 유지 테스트"""
        scenario = calculations.parse_scenario("현재 패턴 유지")
        
        self.assertEqual(scenario['expense_change'], 0.0)
        self.assertEqual(scenario['salary_change'], 0.0)
        self.assertEqual(scenario['description'], '현재 패턴 유지')
        print("[OK] 시나리오 파싱 - 현재 패턴 유지 테스트 통과")
    
    def test_parse_scenario_expense_decrease(self):
        """시나리오 파싱 - 지출 감소 테스트"""
        scenario = calculations.parse_scenario("지출 10% 감소")
        
        self.assertEqual(scenario['expense_change'], -10.0)
        self.assertEqual(scenario['salary_change'], 0.0)
        print("[OK] 시나리오 파싱 - 지출 감소 테스트 통과")
    
    def test_parse_scenario_salary_increase(self):
        """시나리오 파싱 - 연봉 증가 테스트"""
        scenario = calculations.parse_scenario("연봉 5% 증가")
        
        self.assertEqual(scenario['expense_change'], 0.0)
        self.assertEqual(scenario['salary_change'], 5.0)
        print("[OK] 시나리오 파싱 - 연봉 증가 테스트 통과")
    
    def test_parse_scenario_combined(self):
        """시나리오 파싱 - 복합 시나리오 테스트"""
        scenario = calculations.parse_scenario("지출 10% 감소 + 연봉 5% 증가")
        
        self.assertEqual(scenario['expense_change'], -10.0)
        self.assertEqual(scenario['salary_change'], 5.0)
        print("[OK] 시나리오 파싱 - 복합 시나리오 테스트 통과")
    
    def test_calculate_scenario_expense_decrease(self):
        """시나리오 계산 - 지출 감소 테스트"""
        scenario = calculations.parse_scenario("지출 10% 감소")
        result = calculations.calculate_scenario(self.sample_inputs, scenario, years=5)
        
        self.assertIn('future_assets', result)
        self.assertIn('total_savings', result)
        self.assertIn('yearly_breakdown', result)
        self.assertGreater(result['future_assets'], 0)
        print("[OK] 시나리오 계산 - 지출 감소 테스트 통과")
    
    def test_calculate_scenario_salary_increase(self):
        """시나리오 계산 - 연봉 증가 테스트"""
        scenario = calculations.parse_scenario("연봉 5% 증가")
        result = calculations.calculate_scenario(self.sample_inputs, scenario, years=5)
        
        self.assertIn('future_assets', result)
        self.assertGreater(result['future_assets'], 0)
        print("[OK] 시나리오 계산 - 연봉 증가 테스트 통과")
    
    def test_calculate_scenario_better_than_base(self):
        """시나리오 계산 - 기본보다 나은지 확인 테스트"""
        base_scenario = calculations.parse_scenario("현재 패턴 유지")
        base_result = calculations.calculate_scenario(self.sample_inputs, base_scenario, years=5)
        
        expense_decrease_scenario = calculations.parse_scenario("지출 10% 감소")
        expense_result = calculations.calculate_scenario(self.sample_inputs, expense_decrease_scenario, years=5)
        
        # 지출 감소 시나리오가 더 많은 자산을 가져야 함
        self.assertGreater(expense_result['future_assets'], base_result['future_assets'])
        print("[OK] 시나리오 계산 - 기본보다 나은지 확인 테스트 통과")
    
    def test_compare_scenarios(self):
        """여러 시나리오 비교 테스트"""
        scenarios = [
            "지출 10% 감소",
            "연봉 5% 증가",
            "지출 10% 감소 + 연봉 5% 증가"
        ]
        
        result = calculations.compare_scenarios(self.sample_inputs, scenarios, years=5)
        
        self.assertIn('base_scenario', result)
        self.assertIn('scenarios', result)
        self.assertIn('comparison', result)
        self.assertEqual(len(result['scenarios']), 3)
        print("[OK] 여러 시나리오 비교 테스트 통과")
    
    def test_compare_scenarios_best_worst(self):
        """여러 시나리오 비교 - 최고/최저 시나리오 테스트"""
        scenarios = [
            "지출 10% 감소",
            "연봉 5% 증가"
        ]
        
        result = calculations.compare_scenarios(self.sample_inputs, scenarios, years=5)
        
        self.assertIsNotNone(result['comparison']['best_scenario'])
        self.assertIsNotNone(result['comparison']['worst_scenario'])
        self.assertIn('differences', result['comparison'])
        print("[OK] 여러 시나리오 비교 - 최고/최저 시나리오 테스트 통과")
    
    def test_compare_scenarios_differences(self):
        """여러 시나리오 비교 - 차이 계산 테스트"""
        scenarios = ["지출 10% 감소"]
        
        result = calculations.compare_scenarios(self.sample_inputs, scenarios, years=5)
        
        self.assertIn('지출 10% 감소', result['comparison']['differences'])
        # 지출 감소 시나리오는 기본보다 더 많은 자산을 가져야 함
        diff = result['comparison']['differences']['지출 10% 감소']
        self.assertGreater(diff, 0)
        print("[OK] 여러 시나리오 비교 - 차이 계산 테스트 통과")


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 60)
    print("작업 1.7: 시나리오 비교 계산 로직 테스트 시작")
    print("=" * 60)
    
    # 테스트 스위트 생성
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCalculationsScenario)
    
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

