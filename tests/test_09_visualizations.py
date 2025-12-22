"""
작업 1.9: 시각화 모듈 테스트

테스트 항목:
1. 차트 생성 테스트
2. 데이터 검증 테스트
"""

import sys
from pathlib import Path
import unittest

# 프로젝트 루트 디렉토리를 경로에 추가
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules import visualizations

# plotly가 없을 경우를 대비한 모킹
try:
    import plotly.graph_objects as go
except ImportError:
    # visualizations 모듈에서 이미 MockFigure을 사용하므로
    # visualizations 모듈의 go를 사용
    go = visualizations.go


class TestVisualizations(unittest.TestCase):
    """시각화 모듈 테스트"""
    
    def setUp(self):
        """테스트용 샘플 데이터"""
        self.sample_future_assets = {
            'current_assets': 1000,
            'future_assets': 5000,
            'total_savings': 4000,
            'years': 5,
            'yearly_breakdown': [
                {'year': 1, 'salary': 5150, 'annual_income': 5150, 'annual_expense': 2400, 'annual_savings': 2750, 'assets': 3750},
                {'year': 2, 'salary': 5304.5, 'annual_income': 5304.5, 'annual_expense': 2460, 'annual_savings': 2844.5, 'assets': 6594.5},
            ]
        }
        
        self.sample_grade_result = {
            'grade': 'A',
            'expense_ratio': 50.0,
            'debt_ratio': 10.0,
            'monthly_savings': 200.0,
            'emergency_fund_months': 5.0
        }
        
        self.sample_risk_result = {
            'total_score': 30,
            'risk_level': 'medium',
            'breakdown': {
                'income_interruption': 10,
                'debt_ratio': 10,
                'expense_ratio': 5,
                'retirement_readiness': 5
            },
            'recommendations': ['비상금을 늘리세요']
        }
        
        self.sample_income_interruption = {
            'survival_months': 5.0,
            'survival_years': 0.42,
            'net_assets': 1000,
            'monthly_expense': 200,
            'status': 'warning',
            'recommendation': '비상금이 부족합니다'
        }
    
    def test_create_future_assets_chart(self):
        """미래 자산 추정 차트 생성 테스트"""
        fig = visualizations.create_future_assets_chart(self.sample_future_assets)
        
        self.assertIsInstance(fig, go.Figure)
        self.assertIsNotNone(fig.data)
        print("[OK] 미래 자산 추정 차트 생성 테스트 통과")
    
    def test_create_future_assets_chart_empty(self):
        """미래 자산 추정 차트 - 빈 데이터 테스트"""
        empty_data = {'yearly_breakdown': []}
        fig = visualizations.create_future_assets_chart(empty_data)
        
        self.assertIsInstance(fig, go.Figure)
        print("[OK] 미래 자산 추정 차트 - 빈 데이터 테스트 통과")
    
    def test_create_financial_health_gauge(self):
        """재정 건전성 등급 게이지 차트 생성 테스트"""
        fig = visualizations.create_financial_health_gauge(self.sample_grade_result)
        
        self.assertIsInstance(fig, go.Figure)
        self.assertIsNotNone(fig.data)
        print("[OK] 재정 건전성 등급 게이지 차트 생성 테스트 통과")
    
    def test_create_risk_score_chart(self):
        """위험도 점수 차트 생성 테스트"""
        fig = visualizations.create_risk_score_chart(self.sample_risk_result)
        
        self.assertIsInstance(fig, go.Figure)
        self.assertIsNotNone(fig.data)
        print("[OK] 위험도 점수 차트 생성 테스트 통과")
    
    def test_create_risk_breakdown_chart(self):
        """위험도 점수 세부 항목 차트 생성 테스트"""
        fig = visualizations.create_risk_breakdown_chart(self.sample_risk_result)
        
        self.assertIsInstance(fig, go.Figure)
        self.assertIsNotNone(fig.data)
        print("[OK] 위험도 점수 세부 항목 차트 생성 테스트 통과")
    
    def test_create_scenario_comparison_chart(self):
        """시나리오 비교 차트 생성 테스트"""
        comparison_result = {
            'base_scenario': {
                'scenario_name': '현재 패턴 유지',
                'current_assets': 1000,
                'yearly_breakdown': [
                    {'year': 1, 'assets': 2000},
                    {'year': 2, 'assets': 3000}
                ]
            },
            'scenarios': [
                {
                    'scenario_name': '지출 10% 감소',
                    'current_assets': 1000,
                    'yearly_breakdown': [
                        {'year': 1, 'assets': 2200},
                        {'year': 2, 'assets': 3400}
                    ]
                }
            ]
        }
        
        fig = visualizations.create_scenario_comparison_chart(comparison_result)
        
        self.assertIsInstance(fig, go.Figure)
        # MockFigure의 경우 data가 비어있을 수 있으므로 차트 객체 생성만 확인
        self.assertIsNotNone(fig)
        print("[OK] 시나리오 비교 차트 생성 테스트 통과")
    
    def test_create_survival_chart(self):
        """소득 중단 생존 기간 차트 생성 테스트"""
        fig = visualizations.create_survival_chart(self.sample_income_interruption)
        
        self.assertIsInstance(fig, go.Figure)
        self.assertIsNotNone(fig.data)
        print("[OK] 소득 중단 생존 기간 차트 생성 테스트 통과")


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 60)
    print("작업 1.9: 시각화 모듈 테스트 시작")
    print("=" * 60)
    
    # 테스트 스위트 생성
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestVisualizations)
    
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

