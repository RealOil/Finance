"""
작업 1.8: 데이터 포맷팅 모듈 테스트

테스트 항목:
1. 숫자 포맷팅 테스트
2. 인사이트 텍스트 생성 테스트
3. 상태 메시지 테스트
"""

import sys
from pathlib import Path
import unittest

# 프로젝트 루트 디렉토리를 경로에 추가
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules import formatters


class TestFormatters(unittest.TestCase):
    """데이터 포맷팅 모듈 테스트"""
    
    def test_format_currency(self):
        """금액 포맷팅 테스트"""
        result = formatters.format_currency(5000)
        self.assertEqual(result, "5,000만원")
        
        result = formatters.format_currency(12345.67)
        self.assertEqual(result, "12,346만원")
        
        result = formatters.format_currency(0)
        self.assertEqual(result, "0만원")
        
        print("[OK] 금액 포맷팅 테스트 통과")
    
    def test_format_percentage(self):
        """퍼센트 포맷팅 테스트"""
        result = formatters.format_percentage(3.0)
        self.assertEqual(result, "3.0%")
        
        result = formatters.format_percentage(3.456, decimals=2)
        self.assertEqual(result, "3.46%")
        
        print("[OK] 퍼센트 포맷팅 테스트 통과")
    
    def test_format_number(self):
        """일반 숫자 포맷팅 테스트"""
        result = formatters.format_number(1234.56)
        self.assertEqual(result, "1,235")
        
        result = formatters.format_number(1234.56, decimals=1)
        self.assertIn("1,234", result)
        
        print("[OK] 일반 숫자 포맷팅 테스트 통과")
    
    def test_generate_financial_health_insight_a_plus(self):
        """재정 건전성 인사이트 - A+ 등급 테스트"""
        grade_result = {
            'grade': 'A+',
            'expense_ratio': 40.0,
            'monthly_savings': 300.0
        }
        
        result = formatters.generate_financial_health_insight(grade_result)
        self.assertIn('매우 건강한', result)
        print("[OK] 재정 건전성 인사이트 - A+ 등급 테스트 통과")
    
    def test_generate_financial_health_insight_d(self):
        """재정 건전성 인사이트 - D 등급 테스트"""
        grade_result = {
            'grade': 'D',
            'expense_ratio': 90.0,
            'monthly_savings': -100.0
        }
        
        result = formatters.generate_financial_health_insight(grade_result)
        # '위험' 또는 '개선' 중 하나가 포함되어야 함
        self.assertTrue('위험' in result or '개선' in result)
        print("[OK] 재정 건전성 인사이트 - D 등급 테스트 통과")
    
    def test_generate_risk_insight(self):
        """위험도 인사이트 테스트"""
        risk_result = {
            'total_score': 30,
            'risk_level': 'medium',
            'recommendations': ['비상금을 늘리세요', '지출을 줄이세요']
        }
        
        result = formatters.generate_risk_insight(risk_result)
        self.assertIn('30점', result)
        self.assertIn('권장사항', result)
        print("[OK] 위험도 인사이트 테스트 통과")
    
    def test_generate_future_assets_insight(self):
        """미래 자산 인사이트 테스트"""
        future_assets_result = {
            'current_assets': 1000,
            'future_assets': 5000,
            'total_savings': 4000,
            'years': 10
        }
        
        result = formatters.generate_future_assets_insight(future_assets_result)
        self.assertIn('10년', result)
        self.assertIn('5,000만원', result)
        print("[OK] 미래 자산 인사이트 테스트 통과")
    
    def test_generate_retirement_insight(self):
        """은퇴 인사이트 테스트"""
        retirement_result = {
            'years_to_retirement': 30,
            'expected_assets_at_retirement': 10000,
            'survival_years': 25.0,
            'life_expectancy_after_retirement': 20,
            'is_sustainable': True
        }
        
        result = formatters.generate_retirement_insight(retirement_result)
        self.assertIn('30년', result)
        self.assertIn('10,000만원', result)
        print("[OK] 은퇴 인사이트 테스트 통과")
    
    def test_get_status_message(self):
        """상태 메시지 테스트"""
        result = formatters.get_status_message('safe')
        self.assertIn('안전', result)
        
        result = formatters.get_status_message('danger')
        self.assertIn('위험', result)
        
        print("[OK] 상태 메시지 테스트 통과")


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 60)
    print("작업 1.8: 데이터 포맷팅 모듈 테스트 시작")
    print("=" * 60)
    
    # 테스트 스위트 생성
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestFormatters)
    
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

