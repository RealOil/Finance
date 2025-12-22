# 데이터 출처 검증 방법 (API 및 뉴스 활용)

## 개요

데이터 출처를 API나 뉴스를 통해 검증하는 방법을 정리합니다.

---

## 1. 한국은행 ECOS API

### 1.1 ECOS Open API

**URL**: https://ecos.bok.or.kr/api/

**인증**: API 키 필요 (무료 회원가입)

**주요 데이터**:

- 소비자물가상승률 (인플레이션)
- 금리
- 환율
- GDP 등

### 1.2 인플레이션 데이터 조회 예시

**API 엔드포인트**:

```
https://ecos.bok.or.kr/api/StatisticSearch/{API_KEY}/json/kr/1/10/010Y001/MM/202101/202312/10101
```

**파라미터 설명**:

- `{API_KEY}`: ECOS에서 발급받은 인증키
- `010Y001`: 소비자물가상승률 통계 코드
- `202101`: 시작 기간 (2021년 1월)
- `202312`: 종료 기간 (2023년 12월)
- `10101`: 통계 항목 코드

**참고 링크**:

- ECOS API 가이드: https://ecos.bok.or.kr/api/
- Python 예제: https://wooiljeong.github.io/python/pdr-ecos/

**Python 예시 코드**:

```python
import requests
import json

def get_inflation_data():
    """한국은행 ECOS API를 통한 인플레이션 데이터 조회"""
    api_key = "YOUR_API_KEY"  # ECOS에서 발급받은 API 키
    url = f"https://ecos.bok.or.kr/api/StatisticSearch/{api_key}/json/kr/1/10/010Y001/MM/202101/202312/10101"

    response = requests.get(url)
    data = response.json()

    # 2021, 2022, 2023년 연평균 계산
    # 데이터 파싱 후 평균 계산
    return data

# 사용 예시
inflation_data = get_inflation_data()
```

**참고 링크**:

- ECOS Open API 가이드: https://ecos.bok.or.kr/api/
- API 신청: https://ecos.bok.or.kr/api/ (회원가입 필요)
- Python 라이브러리: `pandas-datareader` 또는 직접 API 호출

---

## 2. 통계청 KOSIS API

### 2.1 KOSIS Open API

**URL**: https://kosis.kr/openapi/

**인증**: API 키 필요 (무료 회원가입)

**주요 데이터**:

- 임금근로시간조사
- 생명표
- 인구 통계
- 물가 통계 등

### 2.2 임금 상승률 데이터 조회

**API 사용 예시**:

```python
import requests

def get_wage_growth_data():
    """통계청 KOSIS API를 통한 임금 상승률 조회"""
    api_key = "YOUR_API_KEY"

    # 임금근로시간조사 통계 코드 필요
    # KOSIS 사이트에서 통계 코드 확인 후 사용
    url = f"https://kosis.kr/openapi/statisticsData.do?method=getList&apiKey={api_key}&format=json&jsonVD=Y&userStatsId=..."

    response = requests.get(url)
    data = response.json()

    return data
```

**참고 링크**:

- KOSIS Open API: https://kosis.kr/openapi/
- KOSIS 공유서비스: https://mgmk.kosis.kr/serviceInfo/openAPIGuide.do
- 통계 코드 검색: https://kosis.kr/statHtml/statHtml.do
- Python 라이브러리: `kosis` 패키지 (https://github.com/seokhoonj/kosis)
- 공공데이터포털: https://www.data.go.kr/data/15127755/openapi.do

### 2.3 생명표 데이터 조회

**통계 코드**: 생명표 관련 통계 코드 확인 필요

**웹 검색 키워드**:

- "통계청 생명표 API"
- "KOSIS 생명표 통계 코드"

---

## 3. 금융감독원 공개 데이터

### 3.1 가계금융조사 보고서

**URL**: https://www.fss.or.kr/

**검색 방법**:

1. 금융감독원 사이트 접속
2. "통계/조사" 또는 "연구/조사" 메뉴
3. "가계금융조사" 검색
4. 최신 보고서 다운로드

**Python으로 웹 스크래핑 (참고)**:

```python
import requests
from bs4 import BeautifulSoup

def search_fss_report(keyword="가계금융조사"):
    """금융감독원 사이트에서 보고서 검색"""
    url = "https://www.fss.or.kr/fss/bbs/B0000001/list.do?menuNo=200010"
    # 검색 파라미터 추가

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 보고서 링크 찾기
    # 실제 구현 시 사이트 구조 확인 필요
    return soup
```

**주의사항**:

- 웹 스크래핑은 사이트 이용약관 확인 필요
- 가능하면 공식 API나 다운로드 링크 사용 권장

---

## 4. 뉴스 검색을 통한 검증

### 4.1 Google News API

**무료 방법**: Google News RSS 또는 웹 검색

**Python 예시**:

```python
import feedparser
import requests
from bs4 import BeautifulSoup

def search_news(query, num_results=10):
    """Google News 검색"""
    # Google News RSS 사용
    url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"

    feed = feedparser.parse(url)

    results = []
    for entry in feed.entries[:num_results]:
        results.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.published
        })

    return results

# 사용 예시
news = search_news("한국은행 인플레이션 2023", 5)
```

### 4.2 네이버 뉴스 API

**URL**: https://developers.naver.com/docs/serviceapi/search/news/news.md

**인증**: Client ID, Client Secret 필요

**Python 예시**:

```python
import requests

def search_naver_news(query):
    """네이버 뉴스 검색 API"""
    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"

    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    params = {
        "query": query,
        "display": 10,
        "sort": "date"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    return data['items']

# 사용 예시
news = search_naver_news("한국은행 소비자물가상승률 2023")
```

### 4.3 검증에 유용한 뉴스 검색어

**인플레이션 검증**:

- "한국은행 소비자물가상승률 2023"
- "인플레이션 2021 2022 2023 평균"
- "물가상승률 연평균"

**임금 상승률 검증**:

- "통계청 임금 상승률 2024"
- "평균임금 증가율"
- "임금근로시간조사"

**생명표 검증**:

- "통계청 생명표 60세 기대여명"
- "평균 기대여명 2024"

**비상금 검증**:

- "비상금 6개월 생활비 권장"
- "금융감독원 비상금 기준"

---

## 5. 실시간 검증 스크립트

### 5.1 통합 검증 스크립트 예시

```python
import requests
import json
from datetime import datetime

class DataVerifier:
    def __init__(self):
        self.ecos_api_key = None  # ECOS API 키 설정
        self.kosis_api_key = None  # KOSIS API 키 설정
        self.naver_client_id = None  # 네이버 API 키 설정
        self.naver_client_secret = None

    def verify_inflation(self):
        """인플레이션 데이터 검증"""
        # 방법 1: ECOS API
        if self.ecos_api_key:
            try:
                data = self.get_ecos_inflation()
                print(f"ECOS API 결과: {data}")
            except Exception as e:
                print(f"ECOS API 오류: {e}")

        # 방법 2: 뉴스 검색
        news = self.search_news("한국은행 소비자물가상승률 2023")
        print(f"뉴스 검색 결과: {len(news)}개 기사 발견")

        return {
            'api_data': data if self.ecos_api_key else None,
            'news_count': len(news),
            'verified': False  # 수동 확인 필요
        }

    def verify_wage_growth(self):
        """임금 상승률 검증"""
        news = self.search_news("통계청 임금 상승률 2024")
        return {
            'news_count': len(news),
            'verified': False
        }

    def verify_life_expectancy(self):
        """기대여명 검증"""
        news = self.search_news("통계청 생명표 60세 기대여명")
        return {
            'news_count': len(news),
            'verified': False
        }

    def search_news(self, query):
        """뉴스 검색 (네이버 API 사용)"""
        if not self.naver_client_id:
            return []

        url = "https://openapi.naver.com/v1/search/news.json"
        headers = {
            "X-Naver-Client-Id": self.naver_client_id,
            "X-Naver-Client-Secret": self.naver_client_secret
        }
        params = {"query": query, "display": 10}

        try:
            response = requests.get(url, headers=headers, params=params)
            return response.json().get('items', [])
        except:
            return []

# 사용 예시
verifier = DataVerifier()
results = verifier.verify_inflation()
```

---

## 6. 검증 워크플로우

### 6.1 단계별 검증 프로세스

1. **API 키 발급**

   - ECOS: https://ecos.bok.or.kr/api/ (회원가입)
   - KOSIS: https://kosis.kr/openapi/ (회원가입)
   - 네이버: https://developers.naver.com/ (개발자 등록)

2. **데이터 조회**

   - API를 통한 직접 조회
   - 뉴스 검색을 통한 간접 확인

3. **데이터 검증**

   - API 데이터와 문서의 수치 비교
   - 뉴스 기사에서 언급된 수치 확인

4. **문서 업데이트**
   - 검증된 수치로 문서 업데이트
   - 출처에 API 또는 뉴스 링크 추가

---

## 7. 검증 체크리스트

### 7.1 인플레이션 2.5% 검증

- [ ] ECOS API로 2021-2023년 데이터 조회
- [ ] 연평균 계산 후 2.5% 확인
- [ ] 뉴스에서 최근 인플레이션 관련 기사 확인
- [ ] 문서에 정확한 수치 및 출처 업데이트

### 7.2 재정 건전성 등급 기준 검증

- [ ] 금융감독원 사이트에서 가계금융조사 보고서 검색
- [ ] 보고서에서 저축률 기준 확인
- [ ] 뉴스에서 관련 기준 언급 확인
- [ ] 공식 기준이 없으면 "금융권 일반 권장"으로 변경

### 7.3 비상금 6개월치 검증

- [ ] 금융감독원 공식 문서 검색
- [ ] 뉴스에서 비상금 권장 기준 확인
- [ ] 금융권 일반 조언인지 확인
- [ ] 문서에 정확한 출처 명시

### 7.4 생명표 기대여명 검증

- [ ] KOSIS API로 생명표 데이터 조회
- [ ] 통계청 사이트에서 최신 생명표 확인
- [ ] 뉴스에서 최근 기대여명 관련 기사 확인
- [ ] 문서에 정확한 수치 업데이트

---

## 8. API 키 발급 가이드

### 8.1 한국은행 ECOS API

1. https://ecos.bok.or.kr/ 접속
2. 회원가입
3. "Open API" 메뉴에서 API 키 발급
4. API 사용 가이드 확인

### 8.2 통계청 KOSIS API

1. https://kosis.kr/ 접속
2. 회원가입
3. "Open API" 메뉴에서 API 키 발급
4. 통계 코드 검색 및 확인

### 8.3 네이버 검색 API

1. https://developers.naver.com/ 접속
2. 개발자 등록
3. "Application" 등록
4. Client ID, Client Secret 발급

---

## 9. 검증 결과 기록 템플릿

```markdown
## 검증 결과: [항목명]

**검증 일자**: 2025-12-21

**검증 방법**:

- [ ] ECOS API
- [ ] KOSIS API
- [ ] 뉴스 검색
- [ ] 공식 사이트 확인

**검증 결과**:

- 문서 수치: [수치]
- 실제 수치: [수치]
- 차이: [차이]

**출처**:

- API: [링크]
- 뉴스: [링크]
- 공식 문서: [링크]

**업데이트 필요**: [예/아니오]
```

---

## 10. 자동화 검증 스크립트 (향후 개발)

Phase 2에서 자동화 검증 시스템 구축 고려:

```python
# modules/data_verification.py

def auto_verify_all_sources():
    """모든 데이터 출처 자동 검증"""
    verifier = DataVerifier()

    results = {
        'inflation': verifier.verify_inflation(),
        'wage_growth': verifier.verify_wage_growth(),
        'life_expectancy': verifier.verify_life_expectancy(),
        # ... 기타 항목
    }

    # 검증 결과 리포트 생성
    generate_verification_report(results)

    return results
```

---

이 문서를 참고하여 실제 데이터를 검증하고, `data_sources.md`와 `phase1_design.md`를 업데이트하세요.
