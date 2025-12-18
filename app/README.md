# E-commerce Product Search (Streamlit)

Azure AI Search와 OpenAI를 활용한 이커머스 상품 검색 및 RAG 기반 챗봇 애플리케이션

## 🚀 실행 방법

### 1. 환경 변수 설정

`.env` 파일을 생성하고 다음 정보를 입력하세요:

```bash
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Model Deployments
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=text-embedding-3-large

# Azure AI Search
AZURE_SEARCH_SERVICE_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_INDEX_NAME=products-index

# Embedding Configuration
EMBEDDING_DIMENSION=3072
```

### 2. 필요한 패키지 설치

```bash
pip install streamlit python-dotenv azure-identity azure-search-documents openai
```

### 3. 애플리케이션 실행

```bash
cd app
streamlit run app.py
```

또는 전체 경로로 실행:

```bash
streamlit run /Users/kichul/Documents/project/aoai-workshop/aoai-workshop/app/app.py
```

브라우저가 자동으로 열리며 `http://localhost:8501`에서 앱이 실행됩니다.

## 📋 주요 기능

### 🎯 두 가지 모드

#### 📦 상품 목록
상품 검색 및 브라우징 기능을 제공합니다.

- **검색 방식 선택**
  - Keyword: 전문 검색 (BM25)
  - Vector: 의미 기반 검색 (임베딩)
  - Hybrid: 키워드 + 벡터 결합 (권장)

- **검색 범위 선택**
  - name (상품명)
  - brand (브랜드)
  - description (설명)
  - imageCaption (이미지 캡션)
  - imageDescription (이미지 설명)
  - imageTags (이미지 태그)

- **상품 표시**
  - 페이지당 9개 상품 (3줄 × 3개)
  - 고정 높이 카드 디자인 (690px)
  - 이미지, 상품명, 브랜드, 가격, 설명, 캡션, 태그 표시
  - 검색 시 관련도 점수 표시
  - 페이지네이션 (이전/다음 버튼)

#### 💬 AI 챗봇 (RAG 기반)
자연어로 상품을 추천받을 수 있는 대화형 챗봇입니다.

- **작동 방식**
  1. 사용자가 질문 입력 (예: "여름에 시원하게 입을 티셔츠 추천해줘")
  2. 하이브리드 검색으로 가장 관련성 높은 상품 검색
  3. 검색된 상품 정보를 컨텍스트로 LLM 호출
  4. 자연스러운 대화체로 상품 추천 및 설명 생성

- **챗봇 기능**
  - 자연어 상품 추천
  - 대화 히스토리 유지 (최근 7개 메시지)
  - 추천 상품 정보 표시
    - 상품명 헤더
    - AI 추천 설명
    - 상품 상세 정보 (펼치기/접기)
      - 상품 이미지
      - 브랜드, 가격
      - 상품 설명
      - 이미지 캡션/설명
      - 태그
      - 검색 관련도 점수

- **로딩 인디케이터**
  - "상품 검색 중..." 스피너 표시
  - 응답 생성 시간 동안 피드백 제공

### 🎨 UI 특징

- **Wide Layout**: 넓은 화면 활용
- **라디오 버튼**: 상품 목록 ↔ 챗봇 간 쉬운 전환
- **사이드바**: 검색 설정 및 옵션
- **반응형 디자인**: 고정 높이 카드로 일관된 레이아웃
- **자연스러운 스크롤**: 채팅 히스토리 자동 스크롤

## 🔧 기술 스택

- **Frontend**: Streamlit 1.28.0
- **Backend**: Python
- **Search**: Azure AI Search (Hybrid Search)
- **AI**: Azure OpenAI
  - Chat Completion: GPT-4o
  - Embeddings: text-embedding-3-large
- **Authentication**: Azure DefaultAzureCredential

## 📁 프로젝트 구조

```
app/
├── app.py                      # 메인 Streamlit 애플리케이션
├── config.py                   # 설정 관리 (환경 변수 로드)
├── README.md                   # 프로젝트 문서
├── concept.md                  # 컨셉 및 설계 문서
├── .env                        # 환경 변수 (생성 필요)
├── data/
│   └── products.json           # 샘플 상품 데이터
├── scripts/
│   ├── init_search_index.py   # AI Search 인덱스 초기화
│   └── upload_products.py     # 상품 데이터 업로드
└── services/
    ├── azure_search_service.py # Azure AI Search 연동 (검색 기능)
    ├── openai_service.py       # Azure OpenAI 연동 (LLM, 임베딩)
    ├── product_service.py      # 상품 관리 서비스
    └── vision_service.py       # 이미지 분석 (Vision API)
```

## 💡 사용 예시

### 상품 목록 모드
1. 사이드바에서 검색 방식 선택 (Hybrid 권장)
2. 검색 범위 선택 (기본: 모든 필드)
3. 검색어 입력 후 "검색" 버튼 클릭
4. 또는 "전체보기" 버튼으로 모든 상품 보기
5. 상품 카드에서 상세 정보 확인
6. 페이지 버튼으로 다른 상품 탐색

### 챗봇 모드
1. "💬 챗봇" 라디오 버튼 선택
2. 자연어로 질문 입력
   - "여름에 입을 시원한 티셔츠 추천해줘"
   - "운동할 때 신을 편한 신발 있어?"
   - "세련된 검은색 가방 찾고 있어"
3. AI가 상품을 검색하고 자연스럽게 추천
4. 추천 상품명 클릭하여 상세 정보 확인
5. 대화 계속하거나 "🗑️ 대화 초기화"로 새 대화 시작

## 🐛 문제 해결

### Azure 인증 오류
- Azure CLI 로그인 확인: `az login`
- DefaultAzureCredential이 올바르게 설정되었는지 확인
- 적절한 RBAC 권한 확인 (Search Index Data Reader, Cognitive Services OpenAI User)

### 검색 결과 없음
- Azure AI Search 인덱스가 생성되었는지 확인
- 인덱스에 데이터가 업로드되었는지 확인
- 검색 필드가 올바르게 설정되었는지 확인
- `scripts/init_search_index.py`와 `scripts/upload_products.py` 실행 확인

### 챗봇 응답 오류
- Azure OpenAI 배포가 활성화되어 있는지 확인
- `.env` 파일의 DEPLOYMENT_NAME이 올바른지 확인
- OpenAI API 할당량 및 요금 제한 확인

### 포트 충돌
다른 포트로 실행:
```bash
streamlit run app.py --server.port 8502
```

## 📝 참고사항

### 필수 사전 준비
1. Azure AI Search 인덱스 생성 및 데이터 업로드
   - Tutorial 폴더의 노트북 참조
   - `02_aisearch_setup.ipynb`: 인덱스 생성
   - `03_upload_sample_data.ipynb`: 데이터 업로드

2. 필요한 인덱스 필드
   - `id`, `name`, `brand`, `price` (기본 정보)
   - `description`, `descriptionVector` (설명 및 벡터)
   - `imageUrl` (이미지)
   - `imageCaption`, `imageDescription` (이미지 정보)
   - `imageTags` (태그 배열)

3. Azure OpenAI 리소스
   - GPT-4o 배포 (chat completion)
   - text-embedding-3-large 배포 (벡터 검색)

### RAG 챗봇 동작 원리
1. 사용자 입력 → Hybrid Search 실행
2. 최상위 상품 선택 (highest score)
3. 상품 정보로 컨텍스트 생성
4. System Prompt + Context + 대화 히스토리 → LLM
5. 자연스러운 추천 응답 생성
6. 응답과 함께 상품 정보 저장 및 표시

### 성능 최적화
- `@st.cache_resource`: 서비스 객체 캐싱
- Session State: 상품 목록 및 대화 히스토리 유지
- Hybrid Search: 키워드와 의미 검색 결합으로 정확도 향상
