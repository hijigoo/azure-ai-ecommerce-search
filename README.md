# Azure OpenAI 이커머스 워크샵

Azure OpenAI와 AI Search를 활용한 이커머스 검색 및 RAG 기반 챗봇 워크샵 자료입니다.

## 👩🏻‍💻 데모 스크린샷

### 상품 검색 (키워드/벡터/하이브리드 검색)
![상품 검색 화면](https://github.com/user-attachments/assets/6e748d01-2720-442e-b851-8ba6183b2e2b)

### AI 챗봇 (RAG 기반 검색 및 추천)
![AI 챗봇 화면](https://github.com/user-attachments/assets/8c2ddec1-8d53-43a2-a365-e68328099650)

## 🗒️ 프로젝트 개요

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

## 📚 프로젝트 구조 및 학습 순서

### Tutorial (단계별 학습)
1. **[01_introduction.ipynb](tutorial/01_introduction.ipynb)**: Azure OpenAI 기본 설정 및 연동
2. **[02_aisearch_setup.ipynb](tutorial/02_aisearch_setup.ipynb)**: AI Search 인덱스 생성
3. **[03_upload_sample_data.ipynb](tutorial/03_upload_sample_data.ipynb)**: 샘플 데이터 업로드
4. **[04_search_data.ipynb](tutorial/04_search_data.ipynb)**: 키워드/벡터/하이브리드 검색 실습
5. **[05_synonym_search_data.ipynb](tutorial/05_synonym_search_data.ipynb)**: 동의어 검색 구현
6. **[06_image_to_product_info.ipynb](tutorial/06_image_to_product_info.ipynb)**: 이미지 분석 및 정보 추출
7. **[07_upload_augmented_data.ipynb](tutorial/07_upload_augmented_data.ipynb)**: 증강된 데이터 업로드
8. **[08_search_augmented_data.ipynb](tutorial/08_search_augmented_data.ipynb)**: 증강 데이터로 검색 품질 향상

### Application (실전 애플리케이션)
9. **[app/](app/)**: Streamlit 웹 애플리케이션
   - 상품 검색 (키워드/벡터/하이브리드)
   - RAG 기반 AI 챗봇

> ⚠️ **중요**: Application은 Tutorial 1-8에서 생성한 인덱스를 사용합니다. Tutorial을 먼저 완료하세요.

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
cd azure-ai-ecommerce-search

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

---

**Happy Learning! 🚀**
