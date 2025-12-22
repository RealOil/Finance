"""
작업 1.1: 프로젝트 기본 구조 설정 테스트

테스트 항목:
1. 디렉토리 존재 확인
2. requirements.txt 검증
3. .gitignore 검증
4. README.md 검증
5. .env.example 검증
6. __init__.py 파일 존재 확인
"""

import os
import sys
from pathlib import Path

# 프로젝트 루트 디렉토리
PROJECT_ROOT = Path(__file__).parent.parent


def test_directories_exist():
    """모든 필수 디렉토리가 존재하는지 확인"""
    required_dirs = [
        'pages',
        'modules',
        'shared',
        'data',
        'config',
        'plan',
        'tests',
        'docs'
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        dir_path = PROJECT_ROOT / dir_name
        if not dir_path.exists():
            missing_dirs.append(dir_name)
        assert dir_path.exists(), f"디렉토리가 존재하지 않습니다: {dir_name}"
    
    print(f"[OK] 모든 디렉토리 존재 확인 완료: {', '.join(required_dirs)}")
    return True


def test_requirements_txt():
    """requirements.txt 파일 검증"""
    requirements_path = PROJECT_ROOT / 'requirements.txt'
    
    assert requirements_path.exists(), "requirements.txt 파일이 존재하지 않습니다"
    
    with open(requirements_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 필수 패키지 확인
    required_packages = [
        'streamlit',
        'pandas',
        'plotly',
        'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        if package not in content:
            missing_packages.append(package)
        assert package in content, f"필수 패키지가 없습니다: {package}"
    
    print(f"[OK] requirements.txt 검증 완료: {', '.join(required_packages)} 포함")
    return True


def test_gitignore():
    """.gitignore 파일 검증"""
    gitignore_path = PROJECT_ROOT / '.gitignore'
    
    assert gitignore_path.exists(), ".gitignore 파일이 존재하지 않습니다"
    
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 필수 항목 확인
    required_items = [
        '__pycache__',
        '.env',
        'venv',
        '.streamlit'
    ]
    
    missing_items = []
    for item in required_items:
        if item not in content:
            missing_items.append(item)
        assert item in content, f"필수 항목이 없습니다: {item}"
    
    print(f"[OK] .gitignore 검증 완료: {', '.join(required_items)} 포함")
    return True


def test_readme():
    """README.md 파일 검증"""
    readme_path = PROJECT_ROOT / 'README.md'
    
    assert readme_path.exists(), "README.md 파일이 존재하지 않습니다"
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 필수 섹션 확인
    required_sections = [
        '프로젝트 소개',
        '설치 방법',
        '실행 방법',
        '면책 조항'
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
        assert section in content, f"필수 섹션이 없습니다: {section}"
    
    print(f"[OK] README.md 검증 완료: {', '.join(required_sections)} 포함")
    return True


def test_env_example():
    """.env.example 파일 검증 (선택적)"""
    env_example_path = PROJECT_ROOT / '.env.example'
    
    # .env.example은 선택적 파일이므로 존재 여부만 확인
    if env_example_path.exists():
        print("[OK] .env.example 파일 존재 확인 완료")
    else:
        print("[SKIP] .env.example 파일은 선택적입니다 (생성되지 않음)")
    
    # 선택적 파일이므로 항상 통과
    return True


def test_init_files():
    """각 디렉토리에 __init__.py 파일이 있는지 확인"""
    dirs_with_init = [
        'pages',
        'modules',
        'shared',
        'data',
        'config'
    ]
    
    missing_init = []
    for dir_name in dirs_with_init:
        init_path = PROJECT_ROOT / dir_name / '__init__.py'
        if not init_path.exists():
            missing_init.append(dir_name)
        assert init_path.exists(), f"__init__.py 파일이 없습니다: {dir_name}/__init__.py"
    
    print(f"[OK] __init__.py 파일 확인 완료: {', '.join(dirs_with_init)}")
    return True


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 60)
    print("작업 1.1: 프로젝트 기본 구조 설정 테스트 시작")
    print("=" * 60)
    
    tests = [
        ("디렉토리 존재 확인", test_directories_exist),
        ("requirements.txt 검증", test_requirements_txt),
        (".gitignore 검증", test_gitignore),
        ("README.md 검증", test_readme),
        (".env.example 검증", test_env_example),
        ("__init__.py 파일 확인", test_init_files),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            print(f"\n[{test_name}] 실행 중...")
            result = test_func()
            results.append((test_name, True, None))
        except AssertionError as e:
            print(f"[FAIL] 실패: {str(e)}")
            results.append((test_name, False, str(e)))
        except Exception as e:
            print(f"[ERROR] 오류: {str(e)}")
            results.append((test_name, False, str(e)))
    
    print("\n" + "=" * 60)
    print("테스트 결과 요약")
    print("=" * 60)
    
    passed = sum(1 for _, result, _ in results if result)
    total = len(results)
    
    for test_name, result, error in results:
        status = "[PASS] 통과" if result else "[FAIL] 실패"
        print(f"{status}: {test_name}")
        if error:
            print(f"   오류: {error}")
    
    print(f"\n총 {total}개 테스트 중 {passed}개 통과, {total - passed}개 실패")
    
    if passed == total:
        print("\n[SUCCESS] 모든 테스트 통과!")
        return True
    else:
        print(f"\n[WARNING] {total - passed}개 테스트 실패")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

