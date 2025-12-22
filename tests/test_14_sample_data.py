"""
작업 1.14: 샘플 데이터 기능 테스트

테스트 항목:
1. 샘플 데이터 로드 테스트
2. 샘플 데이터 적용 테스트
"""

import sys
from pathlib import Path
import unittest

# 프로젝트 루트 디렉토리를 경로에 추가
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from data.sample_data import (
    get_sample_scenarios,
    get_sample_data,
    apply_sample_data
)


class TestSampleData(unittest.TestCase):
    """샘플 데이터 테스트"""
    
    def test_get_sample_scenarios(self):
        """샘플 시나리오 목록 반환 테스트"""
        scenarios = get_sample_scenarios()
        
        self.assertIsInstance(scenarios, dict)
        self.assertGreater(len(scenarios), 0)
        self.assertIn('일반 직장인', scenarios)
        self.assertIn('신입 직장인', scenarios)
        self.assertIn('중년 직장인', scenarios)
        self.assertIn('은퇴 준비 중', scenarios)
        print("[OK] 샘플 시나리오 목록 반환 테스트 통과")
    
    def test_get_sample_data(self):
        """특정 시나리오의 샘플 데이터 반환 테스트"""
        # 일반 직장인 시나리오
        data = get_sample_data('일반 직장인')
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data['current_age'], 30)
        self.assertEqual(data['retirement_age'], 60)
        self.assertEqual(data['salary'], 5000)
        self.assertEqual(data['total_assets'], 1000)
        self.assertEqual(data['total_debt'], 0)
        print("[OK] 특정 시나리오 데이터 반환 테스트 통과")
    
    def test_get_sample_data_invalid(self):
        """존재하지 않는 시나리오 테스트"""
        with self.assertRaises(KeyError):
            get_sample_data('존재하지 않는 시나리오')
        print("[OK] 존재하지 않는 시나리오 에러 처리 테스트 통과")
    
    def test_apply_sample_data(self):
        """샘플 데이터 적용 테스트"""
        # Mock session state
        class MockSessionState:
            def __init__(self):
                self._data = {}
            
            def __getitem__(self, key):
                return self._data[key]
            
            def __setitem__(self, key, value):
                self._data[key] = value
        
        session_state = MockSessionState()
        
        # 샘플 데이터 적용
        apply_sample_data('일반 직장인', session_state)
        
        # 세션 상태 확인
        self.assertEqual(session_state['current_age'], 30)
        self.assertEqual(session_state['retirement_age'], 60)
        self.assertEqual(session_state['salary'], 5000)
        self.assertEqual(session_state['sample_applied'], '일반 직장인')
        print("[OK] 샘플 데이터 적용 테스트 통과")
    
    def test_sample_data_structure(self):
        """모든 샘플 데이터의 구조 검증"""
        scenarios = get_sample_scenarios()
        required_keys = [
            'current_age', 'retirement_age', 'salary', 
            'salary_growth_rate', 'bonus', 'monthly_expense',
            'annual_fixed_expense', 'total_assets', 'total_debt'
        ]
        
        for scenario_name, data in scenarios.items():
            for key in required_keys:
                self.assertIn(key, data, f"{scenario_name}에 {key}가 없습니다")
            # 나이 검증
            self.assertLess(data['current_age'], data['retirement_age'], 
                          f"{scenario_name}의 나이 설정이 잘못되었습니다")
        
        print("[OK] 샘플 데이터 구조 검증 테스트 통과")


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 60)
    print("작업 1.14: 샘플 데이터 기능 테스트 시작")
    print("=" * 60)
    
    # 테스트 스위트 생성
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSampleData)
    
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

