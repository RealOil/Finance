"""
작업 1.3: 공통 입력 폼 컴포넌트 테스트

테스트 항목:
1. 입력 폼 렌더링 테스트 (모의)
2. 세션 상태 업데이트 테스트
3. 반환값 검증
"""

import sys
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch, call

# 프로젝트 루트 디렉토리를 경로에 추가
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# MockSessionState 재사용
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
        """속성 접근 지원"""
        if key == '_data':
            return object.__getattribute__(self, '_data')
        return self._data.get(key)
    
    def __setattr__(self, key, value):
        """속성 설정 지원"""
        if key == '_data':
            object.__setattr__(self, key, value)
        else:
            self._data[key] = value
    
    def get(self, key, default=None):
        return self._data.get(key, default)


class TestInputForm(unittest.TestCase):
    """공통 입력 폼 컴포넌트 테스트"""
    
    def setUp(self):
        """테스트 전 설정"""
        # 모듈 재로드
        if 'shared.input_form' in sys.modules:
            del sys.modules['shared.input_form']
        if 'shared.session_manager' in sys.modules:
            del sys.modules['shared.session_manager']
        
        # Streamlit 모의 객체 생성
        self.mock_streamlit = MagicMock()
        self.mock_session_state = MockSessionState()
        self.mock_streamlit.session_state = self.mock_session_state
        
        # streamlit 모듈 패치
        self.streamlit_patcher = patch.dict('sys.modules', {'streamlit': self.mock_streamlit})
        self.streamlit_patcher.start()
        
        # sidebar 모의
        self.mock_sidebar = MagicMock()
        self.mock_streamlit.sidebar = self.mock_sidebar
        
        # number_input, slider, markdown 모의
        self.mock_number_input = MagicMock(side_effect=self._mock_number_input)
        self.mock_slider = MagicMock(side_effect=self._mock_slider)
        self.mock_markdown = MagicMock()
        
        self.mock_sidebar.number_input = self.mock_number_input
        self.mock_sidebar.slider = self.mock_slider
        self.mock_sidebar.markdown = self.mock_markdown
        
        # 모듈 import
        from shared import input_form
        input_form.st = self.mock_streamlit
        input_form.st.sidebar = self.mock_sidebar
        
        self.input_form = input_form
        self.input_values = {
            'current_age': 35,
            'retirement_age': 65,
            'salary': 6000,
            'salary_growth_rate': 5.0,
            'bonus': 500,
            'monthly_expense': 300,
            'annual_fixed_expense': 200,
            'total_assets': 2000,
            'total_debt': 500
        }
    
    def _mock_number_input(self, *args, **kwargs):
        """number_input 모의 - value 반환"""
        label = kwargs.get('label', args[0] if args else '')
        default_value = kwargs.get('value', 0)
        
        # 입력값이 있으면 해당 값 반환
        if label in ['현재 나이']:
            return self.input_values.get('current_age', default_value)
        elif label in ['기대 은퇴 나이']:
            return self.input_values.get('retirement_age', default_value)
        elif label in ['연봉 (만원)']:
            return self.input_values.get('salary', default_value)
        elif label in ['보너스 (만원/년, 선택)']:
            return self.input_values.get('bonus', default_value)
        elif label in ['월 지출 (만원)']:
            return self.input_values.get('monthly_expense', default_value)
        elif label in ['연간 고정 지출 (만원, 선택)']:
            return self.input_values.get('annual_fixed_expense', default_value)
        elif label in ['현재 총 자산 (만원)']:
            return self.input_values.get('total_assets', default_value)
        elif label in ['현재 총 부채 (만원)']:
            return self.input_values.get('total_debt', default_value)
        
        return default_value
    
    def _mock_slider(self, *args, **kwargs):
        """slider 모의 - value 반환"""
        label = kwargs.get('label', args[0] if args else '')
        default_value = kwargs.get('value', 0.0)
        
        if '소득 증가율' in label:
            return self.input_values.get('salary_growth_rate', default_value)
        
        return default_value
    
    def tearDown(self):
        """테스트 후 정리"""
        self.streamlit_patcher.stop()
    
    def test_render_input_form_returns_dict(self):
        """입력 폼 렌더링이 딕셔너리를 반환하는지 테스트"""
        inputs = self.input_form.render_input_form()
        
        self.assertIsInstance(inputs, dict)
        print("[OK] 반환값이 딕셔너리인지 확인 통과")
    
    def test_render_input_form_contains_required_keys(self):
        """반환값에 필수 키가 포함되어 있는지 테스트"""
        inputs = self.input_form.render_input_form()
        
        required_keys = [
            'current_age', 'retirement_age', 'salary', 'salary_growth_rate',
            'bonus', 'monthly_expense', 'annual_fixed_expense',
            'total_assets', 'total_debt'
        ]
        
        for key in required_keys:
            self.assertIn(key, inputs, f"{key}가 반환값에 없습니다")
        
        print("[OK] 필수 키 포함 확인 통과")
    
    def test_render_input_form_updates_session_state(self):
        """입력 폼 렌더링 시 세션 상태가 업데이트되는지 테스트"""
        # 초기 상태 확인
        self.assertNotIn('current_age', self.mock_session_state._data)
        
        # 입력 폼 렌더링
        inputs = self.input_form.render_input_form()
        
        # 세션 상태 업데이트 확인
        for key, value in inputs.items():
            self.assertEqual(
                self.mock_session_state._data.get(key),
                value,
                f"{key}가 세션 상태에 올바르게 저장되지 않았습니다"
            )
        
        print("[OK] 세션 상태 업데이트 확인 통과")
    
    def test_render_input_form_calls_sidebar_methods(self):
        """sidebar 메서드가 호출되는지 테스트"""
        self.input_form.render_input_form()
        
        # markdown이 호출되었는지 확인 (섹션 구분)
        self.assertGreater(self.mock_markdown.call_count, 0)
        
        # number_input이 호출되었는지 확인
        self.assertGreater(self.mock_number_input.call_count, 0)
        
        # slider가 호출되었는지 확인
        self.assertGreater(self.mock_slider.call_count, 0)
        
        print("[OK] sidebar 메서드 호출 확인 통과")


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 60)
    print("작업 1.3: 공통 입력 폼 컴포넌트 테스트 시작")
    print("=" * 60)
    
    # 테스트 스위트 생성
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestInputForm)
    
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

