# Azure OpenAI 이커머스 워크샵

Azure OpenAI와 AI Search를 활용한 이커머스 검색 및 RAG 기반 챗봇 워크샵 자료입니다.

## 📋 프로젝트 개요

- **주제**: Azure OpenAI + AI Search를 활용한 이커머스 솔루션 구현
- **주요 기능**: 
  - 하이브리드 상품 검색 (키워드 + 벡터)
  - RAG 기반 AI 챗봇 상품 추천
  - 이미지 기반 상품 정보 추출 및 증강
- **기술 스택**: Python, Streamlit, Azure AI Search, Azure OpenAI

## 🎯 학습 목표

이 프로젝트를 통해 다음의 실무 활용 가능한 AI 솔루션을 구현하고 이해할 수 있습니다:

1. **Azure AI Search 통합**: 키워드, 벡터, 하이브리드 검색 구현
2. **이미지 기반 상품 속성 추출**: GPT-4o Vision으로 상품 정보 자동 추출
3. **RAG 기반 챗봇**: 검색 결과를 컨텍스트로 활용한 자연스러운 상품 추천
4. **벡터 임베딩**: text-embedding-3-large를 활용한 의미 기반 검색
5. **실시간 웹 애플리케이션**: Streamlit 기반 인터랙티브 UI

## 📚 프로젝트 구조

### 📖 Tutorial (단계별 학습)

#### [01. Introduction](tutorial/01_introduction.ipynb)
- Azure OpenAI 서비스 개요
- 환경 설정 및 API 연동
- 기본 사용법 실습

#### [02. AI Search Setup](tutorial/02_aisearch_setup.ipynb)
- Azure AI Search 인덱스 생성
- 스키마 정의 (벡터 필드 포함)
- 검색 설정 구성

#### [03. Upload Sample Data](tutorial/03_upload_sample_data.ipynb)
- 기본 상품 데이터 업로드
- 임베딩 생성 및 저장
- 인덱스 데이터 확인

#### [04. Search Data](tutorial/04_search_data.ipynb)
- 키워드 검색 구현
- 벡터 검색 구현
- 하이브리드 검색 구현

#### [05. Synonym Search](tutorial/05_synonym_search_data.ipynb)
- 동의어 맵 설정
- 검색 고도화

#### [06. Image to Product Info](tutorial/06_image_to_product_info.ipynb)
- GPT-4o Vision API 활용
- 이미지 분석 및 속성 추출
- 구조화된 데이터로 변환

#### [07. Upload Augmented Data](tutorial/07_upload_augmented_data.ipynb)
- 이미지 분석 결과로 데이터 증강
- 풍부한 상품 정보 업로드

#### [08. Search Augmented Data](tutorial/08_search_augmented_data.ipynb)
- 증강된 데이터로 검색 품질 향상
- 이미지 캡션, 태그 활용 검색

### 🚀 Application (실전 애플리케이션)

#### [Streamlit Web App](app/)
완전한 기능을 갖춘 이커머스 검색 및 챗봇 애플리케이션

**주요 기능:**
- 📦 **상품 목록 모드**
  - 3x3 그리드 레이아웃 (페이지당 9개 상품)
  - 키워드/벡터/하이브리드 검색
  - 검색 범위 선택 (상품명, 브랜드, 설명, 이미지 정보 등)
  - 페이지네이션 및 관련도 점수 표시

- 💬 **AI 챗봇 모드**
  - RAG 기반 자연어 상품 추천
  - 하이브리드 검색으로 관련 상품 찾기
  - GPT-4o로 자연스러운 추천 설명 생성
  - 대화 히스토리 유지 및 컨텍스트 활용
  - 상품 상세 정보 펼치기/접기

**실행 방법:**
```bash
cd app
streamlit run app.py
```

자세한 내용은 [app/README.md](app/README.md)를 참조하세요.

## 🛠 사전 준비사항

### 1. Azure 리소스

#### Azure OpenAI
```bash
# 필요한 모델 배포:
# - gpt-4o (텍스트 생성 + 이미지 분석)
# - text-embedding-3-large (임베딩, 3072 차원)
```

#### Azure AI Search
```bash
# Search Service 생성 (Basic 이상 권장)
# 벡터 검색 지원 (2023-11-01 API 버전 이상)
```

### 2. Python 환경
```bash
# Python 3.8 이상
pip install -r requirements.txt
```

### 3. 환경 변수 설정

프로젝트 루트 및 `app/` 폴더에 각각 `.env` 파일을 생성하세요:

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

**인증 방식:**
- Azure CLI: `az login` (권장)
- 또는 환경 변수에 `AZURE_OPENAI_API_KEY` 추가

## 📦 설치 및 실행

### 1. 환경 설정

```bash
# 1. 리포지토리 이동
cd aoai-workshop

# 2. 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. Azure CLI 로그인
az login

# 5. .env 파일 설정
cp .env.example .env
# .env 파일을 편집하여 실제 Azure 리소스 정보 입력
```

### 2. Tutorial 실습 (순서대로)

```bash
# Jupyter Notebook 실행
jupyter notebook

# 또는 VS Code에서 실행
# tutorial/ 폴더의 노트북을 01번부터 순서대로 실행
```

### 3. 애플리케이션 실행

```bash
# Streamlit 앱 실행
cd app
streamlit run app.py

# 브라우저에서 http://localhost:8501 자동 열림
```

## 📝 학습 순서

### Tutorial (단계별 학습)
1. **01_introduction.ipynb**: Azure OpenAI 기본 설정 및 연동
2. **02_aisearch_setup.ipynb**: AI Search 인덱스 생성
3. **03_upload_sample_data.ipynb**: 샘플 데이터 업로드
4. **04_search_data.ipynb**: 키워드/벡터/하이브리드 검색 실습
5. **05_synonym_search_data.ipynb**: 동의어 검색 구현
6. **06_image_to_product_info.ipynb**: 이미지 분석 및 정보 추출
7. **07_upload_augmented_data.ipynb**: 증강된 데이터 업로드
8. **08_search_augmented_data.ipynb**: 증강 데이터로 검색 품질 향상

### Application (실전 적용)
9. **app/app.py**: 완성된 Streamlit 웹 애플리케이션 실행 및 테스트

## 💡 주요 기능 예시

### 🔍 하이브리드 검색
```python
# 키워드 + 벡터 검색 결합으로 최적의 결과 제공
# 예: "여름에 입을 시원한 티셔츠"
# → 키워드: "티셔츠", "여름"
# → 벡터: 의미 유사도 (시원함, 가벼움, 반팔 등)
```

### 🤖 RAG 기반 챗봇
```python
# 1. 사용자: "운동할 때 신을 편한 신발 추천해줘"
# 2. 시스템: 하이브리드 검색으로 관련 상품 찾기
# 3. GPT-4o: 검색된 상품 정보를 컨텍스트로 활용하여 자연스럽게 추천
# 4. 응답: "고객님께 추천드리는 운동화는..."
```

### 🖼️ 이미지 기반 상품 정보 추출
```python
# GPT-4o Vision으로 상품 이미지 분석
# → 색상, 스타일, 특징 자동 추출
# → 검색 품질 향상을 위한 메타데이터 생성
```

## 🏗️ 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Web App                        │
│  ┌──────────────────┐        ┌──────────────────┐          │
│  │  상품 목록 모드   │        │   챗봇 모드      │          │
│  │  - 그리드 레이아웃│        │  - 자연어 질의   │          │
│  │  - 검색/필터링   │        │  - RAG 추천      │          │
│  └──────────────────┘        └──────────────────┘          │
└─────────────────────────────────────────────────────────────┘
                           ↓
         ┌─────────────────────────────────────┐
         │     Azure AI Search Service         │
         │  ┌──────────────────────────────┐   │
         │  │   Products Index             │   │
         │  │  - Keyword Search (BM25)     │   │
         │  │  - Vector Search (HNSW)      │   │
         │  │  - Hybrid Search (RRF)       │   │
         │  └──────────────────────────────┘   │
         └─────────────────────────────────────┘
                           ↓
         ┌─────────────────────────────────────┐
         │      Azure OpenAI Service           │
         │  ┌──────────────────────────────┐   │
         │  │  gpt-4o                      │   │
         │  │  - Chat Completion           │   │
         │  │  - Vision (Image Analysis)   │   │
         │  ├──────────────────────────────┤   │
         │  │  text-embedding-3-large      │   │
         │  │  - Vector Embeddings (3072)  │   │
         │  └──────────────────────────────┘   │
         └─────────────────────────────────────┘
```

## 📚 참고 자료

### Azure 공식 문서
- [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure AI Search](https://learn.microsoft.com/azure/search/)
- [Vector Search in Azure AI Search](https://learn.microsoft.com/azure/search/vector-search-overview)
- [Hybrid Search (RRF)](https://learn.microsoft.com/azure/search/hybrid-search-ranking)

### API 레퍼런스
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Azure AI Search REST API](https://learn.microsoft.com/rest/api/searchservice/)

### RAG 및 벡터 검색
- [Retrieval Augmented Generation (RAG)](https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview)
- [Vector Embeddings](https://learn.microsoft.com/azure/ai-services/openai/concepts/understand-embeddings)

## 🔒 보안 및 주의사항

- ⚠️ **API 키 보안**: 절대 코드에 하드코딩하지 말고 환경 변수 사용
- ⚠️ **`.env` 파일**: `.gitignore`에 추가하여 버전 관리에서 제외
- ⚠️ **운영 환경**: Azure Key Vault 사용 권장
- ⚠️ **비용 관리**: 
  - Azure OpenAI: 토큰 사용량 모니터링
  - AI Search: 인덱스 크기 및 쿼리 수 관리
  - Cost Management 도구 활용
- ⚠️ **RBAC 권한**: 
  - Search Index Data Reader
  - Cognitive Services OpenAI User

## 💬 문의 및 지원

- **Azure 기술 지원**: [Azure Support](https://azure.microsoft.com/support/)
- **이슈 리포트**: GitHub Issues
- **문서 업데이트**: Pull Requests 환영

## 📄 라이선스

이 프로젝트는 교육 및 학습 목적으로 제공됩니다.

---

**Happy Learning! 🚀**
