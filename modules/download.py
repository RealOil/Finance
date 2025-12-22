"""
다운로드 기능 모듈

계산 결과를 JSON 및 CSV 형식으로 다운로드할 수 있는 기능을 제공합니다.
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional

try:
    import pandas as pd
except ImportError:
    # pandas가 없을 경우를 대비
    pd = None


def create_download_data(
    inputs: Dict[str, Any],
    results: Optional[Dict[str, Any]] = None,
    page_type: str = "income"
) -> Dict[str, Any]:
    """
    다운로드용 데이터 생성
    
    Args:
        inputs: 입력 데이터 딕셔너리
        results: 계산 결과 딕셔너리 (선택)
        page_type: 페이지 타입 ("income", "risk", "comparison")
        
    Returns:
        Dict[str, Any]: 다운로드용 데이터 딕셔너리
    """
    download_data = {
        "메타 정보": {
            "계산 일시": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "페이지 타입": page_type,
            "버전": "1.0"
        },
        "입력 데이터": {
            "현재 나이": inputs.get('current_age', 0),
            "은퇴 예정 나이": inputs.get('retirement_age', 0),
            "연봉 (만원)": inputs.get('salary', 0),
            "연봉 증가율 (%)": inputs.get('salary_growth_rate', 0),
            "보너스 (만원)": inputs.get('bonus', 0),
            "월 지출 (만원)": inputs.get('monthly_expense', 0),
            "연간 고정 지출 (만원)": inputs.get('annual_fixed_expense', 0),
            "총 자산 (만원)": inputs.get('total_assets', 0),
            "총 부채 (만원)": inputs.get('total_debt', 0)
        }
    }
    
    # 계산 결과 추가
    if results:
        download_data["계산 결과"] = results
    
    # 데이터 출처 정보 추가
    download_data["데이터 출처"] = {
        "인플레이션": "한국은행 경제통계시스템 (ECOS) 기준 (연 2.5% 가정)",
        "연봉 인상률": "통계청 근로형태별 근로실태조사 기준",
        "재정 건전성 등급": "일반적인 재정 관리 기준",
        "비상금 기준": "6개월 생활비 권장 기준"
    }
    
    return download_data


def create_json_download(
    inputs: Dict[str, Any],
    results: Optional[Dict[str, Any]] = None,
    page_type: str = "income"
) -> str:
    """
    JSON 형식 다운로드 데이터 생성
    
    Args:
        inputs: 입력 데이터 딕셔너리
        results: 계산 결과 딕셔너리 (선택)
        page_type: 페이지 타입
        
    Returns:
        str: JSON 문자열
    """
    download_data = create_download_data(inputs, results, page_type)
    return json.dumps(download_data, ensure_ascii=False, indent=2)


def create_csv_download(
    data: list,
    columns: Optional[list] = None
) -> str:
    """
    CSV 형식 다운로드 데이터 생성
    
    Args:
        data: 데이터 리스트 (딕셔너리 리스트 또는 리스트의 리스트)
        columns: 컬럼명 리스트 (선택)
        
    Returns:
        str: CSV 문자열
    """
    if not data:
        return ""
    
    if pd is None:
        # pandas가 없을 경우 간단한 CSV 생성
        if isinstance(data[0], dict):
            # 딕셔너리 리스트인 경우
            if not data:
                return ""
            keys = list(data[0].keys())
            lines = [','.join(keys)]
            for row in data:
                values = [str(row.get(k, '')) for k in keys]
                lines.append(','.join(values))
            return '\n'.join(lines)
        else:
            # 리스트의 리스트인 경우
            if columns:
                lines = [','.join(columns)]
            else:
                lines = []
            for row in data:
                lines.append(','.join(str(v) for v in row))
            return '\n'.join(lines)
    
    # pandas를 사용하는 경우
    # 딕셔너리 리스트인 경우
    if isinstance(data[0], dict):
        df = pd.DataFrame(data)
    else:
        # 리스트의 리스트인 경우
        if columns:
            df = pd.DataFrame(data, columns=columns)
        else:
            df = pd.DataFrame(data)
    
    return df.to_csv(index=False, encoding='utf-8-sig')


def get_download_filename(prefix: str, extension: str = "json") -> str:
    """
    다운로드 파일명 생성
    
    Args:
        prefix: 파일명 접두사
        extension: 파일 확장자
        
    Returns:
        str: 파일명
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{prefix}_{timestamp}.{extension}"

