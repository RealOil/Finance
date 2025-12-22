"""
작업 1.6: 리스크 계산 로직 테스트

테스트 항목:
1. 소득 중단 생존 기간 테스트
2. 경제 위기 시나리오 테스트
3. 은퇴 시나리오 테스트
4. 위험도 점수 테스트
"""

import sys
from pathlib import Path
import unittest

# 프로젝트 루트 디렉토리를 경로에 추가
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules import calculations


class TestCalculationsRisk(unittest.TestCase):
    """리스크 계산 로직 테스트"""
    
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
    
    def test_calculate_income_interruption_survival_safe(self):
        """소득 중단 생존 기간 - 안전 케이스 테스트"""
        inputs = self.sample_inputs.copy()
        inputs['total_assets'] = 2000  # 6개월 이상 생존 가능
        
        result = calculations.calculate_income_interruption_survival(inputs)
        
        self.assertGreaterEqual(result['survival_months'], 6)
        self.assertEqual(result['status'], 'safe')
        print("[OK] 소득 중단 생존 기간 - 안전 케이스 테스트 통과")
    
    def test_calculate_income_interruption_survival_warning(self):
        """소득 중단 생존 기간 - 경고 케이스 테스트"""
        inputs = self.sample_inputs.copy()
        inputs['total_assets'] = 1000  # 3-6개월 생존 가능
        
        result = calculations.calculate_income_interruption_survival(inputs)
        
        self.assertGreaterEqual(result['survival_months'], 3)
        self.assertLess(result['survival_months'], 6)
        self.assertEqual(result['status'], 'warning')
        print("[OK] 소득 중단 생존 기간 - 경고 케이스 테스트 통과")
    
    def test_calculate_income_interruption_survival_danger(self):
        """소득 중단 생존 기간 - 위험 케이스 테스트"""
        inputs = self.sample_inputs.copy()
        inputs['total_assets'] = 300  # 3개월 미만
        
        result = calculations.calculate_income_interruption_survival(inputs)
        
        self.assertLess(result['survival_months'], 3)
        self.assertEqual(result['status'], 'danger')
        print("[OK] 소득 중단 생존 기간 - 위험 케이스 테스트 통과")
    
    def test_calculate_crisis_scenario_30_percent(self):
        """경제 위기 시나리오 - 30% 하락 테스트"""
        inputs = self.sample_inputs.copy()
        inputs['total_assets'] = 1000
        
        result = calculations.calculate_crisis_scenario(inputs, asset_drop_rate=30.0)
        
        self.assertEqual(result['asset_drop_rate'], 30.0)
        self.assertEqual(result['assets_before'], 1000)
        self.assertEqual(result['assets_after'], 700)
        self.assertGreater(result['survival_months'], 0)
        print("[OK] 경제 위기 시나리오 - 30% 하락 테스트 통과")
    
    def test_calculate_crisis_scenario_50_percent(self):
        """경제 위기 시나리오 - 50% 하락 테스트"""
        inputs = self.sample_inputs.copy()
        inputs['total_assets'] = 1000
        
        result = calculations.calculate_crisis_scenario(inputs, asset_drop_rate=50.0)
        
        self.assertEqual(result['asset_drop_rate'], 50.0)
        self.assertEqual(result['assets_after'], 500)
        print("[OK] 경제 위기 시나리오 - 50% 하락 테스트 통과")
    
    def test_calculate_retirement_sustainability(self):
        """은퇴 시나리오 테스트"""
        inputs = self.sample_inputs.copy()
        inputs['current_age'] = 30
        inputs['retirement_age'] = 60
        inputs['total_assets'] = 5000
        
        result = calculations.calculate_retirement_sustainability(inputs)
        
        self.assertEqual(result['years_to_retirement'], 30)
        self.assertGreater(result['expected_assets_at_retirement'], 0)
        self.assertGreater(result['survival_months'], 0)
        self.assertIn(result['status'], ['sustainable', 'warning', 'danger'])
        print("[OK] 은퇴 시나리오 테스트 통과")
    
    def test_calculate_retirement_sustainability_error(self):
        """은퇴 시나리오 - 오류 케이스 테스트 (은퇴 나이 <= 현재 나이)"""
        inputs = self.sample_inputs.copy()
        inputs['current_age'] = 60
        inputs['retirement_age'] = 60
        
        result = calculations.calculate_retirement_sustainability(inputs)
        
        self.assertEqual(result['status'], 'error')
        print("[OK] 은퇴 시나리오 - 오류 케이스 테스트 통과")
    
    def test_calculate_risk_score_low(self):
        """위험도 점수 - 낮은 위험 테스트"""
        inputs = {
            'current_age': 30,
            'retirement_age': 60,
            'salary': 10000,
            'bonus': 0,
            'monthly_expense': 300,  # 소득 대비 36%
            'annual_fixed_expense': 0,
            'total_assets': 10000,  # 비상금 충분
            'total_debt': 0
        }
        
        result = calculations.calculate_risk_score(inputs)
        
        self.assertLess(result['total_score'], 25)
        self.assertEqual(result['risk_level'], 'low')
        print("[OK] 위험도 점수 - 낮은 위험 테스트 통과")
    
    def test_calculate_risk_score_high(self):
        """위험도 점수 - 높은 위험 테스트"""
        inputs = {
            'current_age': 30,
            'retirement_age': 60,
            'salary': 5000,
            'bonus': 0,
            'monthly_expense': 600,  # 소득 대비 144%
            'annual_fixed_expense': 0,
            'total_assets': 100,  # 비상금 부족
            'total_debt': 5000  # 부채 비율 높음
        }
        
        result = calculations.calculate_risk_score(inputs)
        
        self.assertGreaterEqual(result['total_score'], 50)
        self.assertIn(result['risk_level'], ['high', 'critical'])
        print("[OK] 위험도 점수 - 높은 위험 테스트 통과")
    
    def test_calculate_risk_score_breakdown(self):
        """위험도 점수 - 세부 항목 테스트"""
        inputs = self.sample_inputs.copy()
        
        result = calculations.calculate_risk_score(inputs)
        
        self.assertIn('breakdown', result)
        self.assertIn('income_interruption', result['breakdown'])
        self.assertIn('debt_ratio', result['breakdown'])
        self.assertIn('expense_ratio', result['breakdown'])
        self.assertIn('retirement_readiness', result['breakdown'])
        self.assertIn('recommendations', result)
        print("[OK] 위험도 점수 - 세부 항목 테스트 통과")


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 60)
    print("작업 1.6: 리스크 계산 로직 테스트 시작")
    print("=" * 60)
    
    # 테스트 스위트 생성
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCalculationsRisk)
    
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

