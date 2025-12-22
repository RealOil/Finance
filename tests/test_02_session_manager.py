"""
작업 1.2: 세션 상태 관리 모듈 테스트

테스트 항목:
1. 세션 상태 초기화 테스트
2. 공유 입력 데이터 반환 테스트
3. 타입 검증
"""

import sys
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch

# 프로젝트 루트 디렉토리를 경로에 추가
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Streamlit 모의 객체 생성
class MockSessionState:
    """Streamlit session_state 모의 객체"""
    def __init__(self):
        self._data = {}
    
    def __contains__(self, key):
        return key in self._data
    
    def __getitem__(self, key):
        return self._data.get(key)
    
    def __setitem__(self, key, value):
        self._data[key] = value
    
    def __getattr__(self, key):
        """속성 접근 지원 (st.session_state.current_age)"""
        if key == '_data':
            return object.__getattribute__(self, '_data')
        return self._data.get(key)
    
    def __setattr__(self, key, value):
        """속성 설정 지원 (st.session_state.current_age = 30)"""
        if key == '_data':
            object.__setattr__(self, key, value)
        else:
            self._data[key] = value
    
    def get(self, key, default=None):
        return self._data.get(key, default)


class TestSessionManager(unittest.TestCase):
    """세션 상태 관리 모듈 테스트"""
    
    def setUp(self):
        """테스트 전 설정"""
        # 모듈 재로드
        if 'shared.session_manager' in sys.modules:
            del sys.modules['shared.session_manager']
        
        # MockSessionState를 streamlit으로 패치
        self.mock_session_state = MockSessionState()
        
        # streamlit 모듈을 모의로 패치
        mock_streamlit = MagicMock()
        mock_streamlit.session_state = self.mock_session_state
        
        self.streamlit_patcher = patch.dict('sys.modules', {'streamlit': mock_streamlit})
        self.streamlit_patcher.start()
        
        # 모듈 import
        from shared import session_manager
        session_manager.st = mock_streamlit
        session_manager.st.session_state = self.mock_session_state
        
        self.session_manager = session_manager
        self.mock_streamlit = mock_streamlit
    
    def tearDown(self):
        """테스트 후 정리"""
        self.streamlit_patcher.stop()
    
    def test_init_session_state(self):
        """세션 상태 초기화 테스트"""
        st = self.mock_streamlit
        st.session_state = self.mock_session_state
        
        # 초기화 전 상태 확인
        self.assertNotIn('current_age', st.session_state._data)
        
        # 세션 상태 초기화
        self.session_manager.init_session_state()
        
        # 입력 데이터 확인
        required_keys = [
            'current_age', 'retirement_age', 'salary', 'salary_growth_rate',
            'bonus', 'monthly_expense', 'annual_fixed_expense',
            'total_assets', 'total_debt'
        ]
        
        for key in required_keys:
            self.assertIn(key, st.session_state._data, f"{key}가 세션 상태에 없습니다")
        
        # 기본값 확인
        self.assertEqual(st.session_state._data['current_age'], 30)
        self.assertEqual(st.session_state._data['retirement_age'], 60)
        self.assertEqual(st.session_state._data['salary'], 5000)
        self.assertEqual(st.session_state._data['salary_growth_rate'], 3.0)
        self.assertEqual(st.session_state._data['bonus'], 0)
        self.assertEqual(st.session_state._data['monthly_expense'], 200)
        self.assertEqual(st.session_state._data['annual_fixed_expense'], 0)
        self.assertEqual(st.session_state._data['total_assets'], 1000)
        self.assertEqual(st.session_state._data['total_debt'], 0)
        
        # 페이지별 계산 완료 상태 확인
        self.assertFalse(st.session_state._data['calculation_done_income'])
        self.assertFalse(st.session_state._data['calculation_done_risk'])
        self.assertFalse(st.session_state._data['calculation_done_comparison'])
        
        # 페이지별 결과 저장소 확인
        self.assertIsNone(st.session_state._data['results_income'])
        self.assertIsNone(st.session_state._data['results_risk'])
        self.assertIsNone(st.session_state._data['results_comparison'])
        
        print("[OK] 세션 상태 초기화 테스트 통과")
    
    def test_init_session_state_idempotent(self):
        """세션 상태 초기화가 멱등성(idempotent)을 가지는지 테스트"""
        st = self.mock_streamlit
        st.session_state = self.mock_session_state
        
        # 첫 번째 초기화
        self.session_manager.init_session_state()
        first_age = st.session_state._data['current_age']
        
        # 값 변경
        st.session_state._data['current_age'] = 40
        
        # 두 번째 초기화 (기존 값이 있으면 변경하지 않아야 함)
        self.session_manager.init_session_state()
        
        # 값이 변경되지 않았는지 확인
        self.assertEqual(st.session_state._data['current_age'], 40)
        
        print("[OK] 세션 상태 초기화 멱등성 테스트 통과")
    
    def test_get_shared_inputs(self):
        """공유 입력 데이터 반환 테스트"""
        st = self.mock_streamlit
        st.session_state = self.mock_session_state
        
        # 세션 상태 초기화
        self.session_manager.init_session_state()
        
        # 공유 입력 데이터 가져오기
        inputs = self.session_manager.get_shared_inputs()
        
        # 반환값이 딕셔너리인지 확인
        self.assertIsInstance(inputs, dict)
        
        # 필수 키 확인
        required_keys = [
            'current_age', 'retirement_age', 'salary', 'salary_growth_rate',
            'bonus', 'monthly_expense', 'annual_fixed_expense',
            'total_assets', 'total_debt'
        ]
        
        for key in required_keys:
            self.assertIn(key, inputs, f"{key}가 반환값에 없습니다")
        
        # 값 확인
        self.assertEqual(inputs['current_age'], 30)
        self.assertEqual(inputs['retirement_age'], 60)
        self.assertEqual(inputs['salary'], 5000)
        
        print("[OK] 공유 입력 데이터 반환 테스트 통과")
    
    def test_get_shared_inputs_with_changes(self):
        """세션 상태 변경 시 반환값 업데이트 테스트"""
        st = self.mock_streamlit
        st.session_state = self.mock_session_state
        
        # 세션 상태 초기화
        self.session_manager.init_session_state()
        
        # 값 변경
        st.session_state._data['current_age'] = 35
        st.session_state._data['salary'] = 6000
        
        # 공유 입력 데이터 가져오기
        inputs = self.session_manager.get_shared_inputs()
        
        # 변경된 값이 반영되었는지 확인
        self.assertEqual(inputs['current_age'], 35)
        self.assertEqual(inputs['salary'], 6000)
        
        print("[OK] 세션 상태 변경 반영 테스트 통과")
    
    def test_get_shared_inputs_default_values(self):
        """세션 상태가 없을 때 기본값 반환 테스트"""
        st = self.mock_streamlit
        st.session_state = self.mock_session_state
        
        # 세션 상태 초기화하지 않고 바로 가져오기
        inputs = self.session_manager.get_shared_inputs()
        
        # 기본값이 반환되는지 확인
        self.assertEqual(inputs['current_age'], 30)
        self.assertEqual(inputs['retirement_age'], 60)
        self.assertEqual(inputs['salary'], 5000)
        
        print("[OK] 기본값 반환 테스트 통과")


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 60)
    print("작업 1.2: 세션 상태 관리 모듈 테스트 시작")
    print("=" * 60)
    
    # 테스트 스위트 생성
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSessionManager)
    
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

