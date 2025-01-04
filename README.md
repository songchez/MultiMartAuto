# MultiMartAuto

## 프로젝트 소개

MultiMartAuto는 네이버 커머스를 포함한 다양한 이커머스 플랫폼에 상품을 자동으로 등록하고 관리할 수 있는 자동화 도구입니다.

## 주요 기능

- 상품 정보 일괄 등록
- 플랫폼별 상품 유효성 검증
- OAuth 2.0 기반 인증 관리
- 상품 데이터 CSV 관리
- API 기반 상품 등록/수정

## 시작하기

### 설치 방법

1. 저장소 클론

   ```bash
   git clone https://github.com/yourusername/MultiMartAuto.git
   ```

2. 의존성 패키지 설치

   ```bash
   bash
   pip install -r requirements.txt
   ```

3. 환경 설정
   - `config.json` 파일에 플랫폼별 API 인증 정보 입력
   - 필요한 디렉토리 생성 (data/, logs/ 등)

### 실행 방법

```bash
streamlit run home.py
```

## 프로젝트 구조

MultiMartAuto/
├── api/
│ ├── api_handler.py # API 요청 처리
│ └── api_endpoints.py # API 엔드포인트 정의
├── auth/
│ └── auth_manager.py # 인증 처리
├── product/
│ ├── product_manager.py # 상품 관리
│ └── validator.py # 상품 유효성 검증
├── data/ # 데이터 저장소
├── home.py # 메인 대시보드
├── product_registration.py # 상품 등록 페이지
├── product_listing.py # 상품 목록 페이지
└── requirements.txt # 의존성 패키지

## 사용 방법

### 1. 인증 설정

- 플랫폼별 API 키 및 시크릿 설정
- OAuth 인증 토큰 발급

### 2. 상품 등록

- CSV 파일을 통한 대량 상품 등록
- 웹 인터페이스를 통한 개별 상품 등록
- 이미지 업로드 및 관리

### 3. 상품 관리

- 등록된 상품 조회 및 수정
- 재고 관리
- 판매 현황 모니터링

## API 문서

각 플랫폼별 API 엔드포인트와 사용 방법은 다음과 같습니다:

### 네이버 커머스

[네이버 커머스 공식 문서 참고](https://apicenter.commerce.naver.com/ko/basic/commerce-api)

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 문의사항

- Issue 트래커를 통해 버그를 보고해주세요
- 기능 개선 제안도 환영합니다

## 업데이트 내역

- v1.0.0 (2024-03)
  - 최초 릴리즈
  - 네이버 커머스 연동 지원
