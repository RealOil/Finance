"""
작업 1.15: 결과 다운로드 기능 테스트

테스트 항목:
1. 다운로드 데이터 생성 테스트
2. JSON 다운로드 테스트
3. CSV 다운로드 테스트
"""

import sys
from pathlib import Path
import unittest
import json

# 프로젝트 루트 디렉토리를 경로에 추가
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.download import (
    create_download_data,
    create_json_download,
    create_csv_download,
    get_download_filename
)


class TestDownload(unittest.TestCase):
    """다운로드 기능 테스트"""
    
    def setUp(self):
        """테스트용 샘플 데이터"""
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
        
        self.sample_results = {
            'future_assets': 5000,
            'grade': 'A',
            'monthly_savings': 200
        }
    
    def test_create_download_data(self):
        """다운로드 데이터 생성 테스트"""
        download_data = create_download_data(self.sample_inputs, self.sample_results, "income")
        
        self.assertIsInstance(download_data, dict)
        self.assertIn('메타 정보', download_data)
        self.assertIn('입력 데이터', download_data)
        self.assertIn('계산 결과', download_data)
        self.assertIn('데이터 출처', download_data)
        print("[OK] 다운로드 데이터 생성 테스트 통과")
    
    def test_create_json_download(self):
        """JSON 다운로드 데이터 생성 테스트"""
        json_str = create_json_download(self.sample_inputs, self.sample_results, "income")
        
        self.assertIsInstance(json_str, str)
        # JSON 파싱 가능한지 확인
        parsed = json.loads(json_str)
        self.assertIsInstance(parsed, dict)
        print("[OK] JSON 다운로드 데이터 생성 테스트 통과")
    
    def test_create_csv_download(self):
        """CSV 다운로드 데이터 생성 테스트"""
        data = [
            {'시나리오': '시나리오 1', '자산': 1000},
            {'시나리오': '시나리오 2', '자산': 2000}
        ]
        
        csv_str = create_csv_download(data)
        
        self.assertIsInstance(csv_str, str)
        self.assertIn('시나리오', csv_str)
        self.assertIn('자산', csv_str)
        print("[OK] CSV 다운로드 데이터 생성 테스트 통과")
    
    def test_get_download_filename(self):
        """다운로드 파일명 생성 테스트"""
        filename = get_download_filename("test", "json")
        
        self.assertIsInstance(filename, str)
        self.assertTrue(filename.startswith("test_"))
        self.assertTrue(filename.endswith(".json"))
        print("[OK] 다운로드 파일명 생성 테스트 통과")
    
    def test_download_data_structure(self):
        """다운로드 데이터 구조 검증"""
        download_data = create_download_data(self.sample_inputs, self.sample_results, "income")
        
        # 메타 정보 검증
        self.assertIn('계산 일시', download_data['메타 정보'])
        self.assertEqual(download_data['메타 정보']['페이지 타입'], 'income')
        
        # 입력 데이터 검증
        self.assertEqual(download_data['입력 데이터']['현재 나이'], 30)
        self.assertEqual(download_data['입력 데이터']['연봉 (만원)'], 5000)
        
        # 계산 결과 검증
        self.assertEqual(download_data['계산 결과']['future_assets'], 5000)
        print("[OK] 다운로드 데이터 구조 검증 테스트 통과")


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 60)
    print("작업 1.15: 결과 다운로드 기능 테스트 시작")
    print("=" * 60)
    
    # 테스트 스위트 생성
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDownload)
    
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

