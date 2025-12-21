# Azure OpenAI 이커머스 워크샵 - Tutorial

Azure AI Search와 OpenAI를 활용한 이커머스 검색 및 RAG 기반 챗봇 구현 실습 자료입니다.

## 📋 학습 순서

**⚠️ 순서대로 진행하세요** - 각 노트북은 이전 단계에서 생성된 데이터/인덱스를 사용합니다.

### 1. [01_introduction.ipynb](01_introduction.ipynb)
Azure OpenAI 연동 및 기본 설정
- Azure OpenAI 클라이언트 초기화
- GPT-4o 모델 테스트
- text-embedding-3-large 임베딩 테스트

### 2. [02_aisearch_setup.ipynb](02_aisearch_setup.ipynb)
AI Search 인덱스 생성
- `products-index` 생성
- 벡터 검색 설정 (HNSW 알고리즘)
- 하이브리드 검색을 위한 스키마 정의

### 3. [03_upload_sample_data.ipynb](03_upload_sample_data.ipynb)
샘플 상품 데이터 업로드
- `data/sample_products.json` 데이터 로드
- 상품 설명 벡터 임베딩 생성
- AI Search 인덱스에 데이터 업로드

### 4. [04_search_data.ipynb](04_search_data.ipynb)
검색 기능 실습
- Keyword 검색 (BM25)
- Vector 검색 (의미 기반)
- Hybrid 검색 (Reciprocal Rank Fusion)

### 5. [05_synonym_search_data.ipynb](05_synonym_search_data.ipynb)
동의어 검색 구현
- 동의어 맵 설정
- 검색 품질 향상

### 6. [06_weighted_field_search.ipynb](06_weighted_field_search.ipynb)
점수 매기기 프로필 (Scoring Profile)
- Scoring Profile 생성 및 적용
- 필드별 가중치 설정 (name: 3.0, brand: 2.0, description: 1.0)
- Scoring Profile 효과 비교
- 하이브리드 검색과 Scoring Profile 조합

### 7. [07_image_to_product_info.ipynb](07_image_to_product_info.ipynb)
이미지 기반 상품 정보 추출
- GPT-4o Vision으로 이미지 분석
- 이미지 캡션/설명/태그 자동 생성
- 증강 데이터 생성 (`data/sample_products_augmented.json`)

### 8. [08_upload_augmented_data.ipynb](08_upload_augmented_data.ipynb)
증강된 데이터 업로드
- 이미지 분석 결과 포함된 데이터 업로드
- 이미지 캡션/설명/태그 벡터화

### 9. [09_search_augmented_data.ipynb](09_search_augmented_data.ipynb)
증강 데이터로 검색 품질 향상 확인
- 이미지 정보를 활용한 검색 테스트
- 검색 정확도 비교

## 🚀 실행 방법

### 1. 환경 설정

`.env` 파일이 이미 생성되어 있습니다. Azure 리소스 정보를 확인하세요:

```bash
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=text-embedding-3-large
AZURE_SEARCH_SERVICE_ENDPOINT=https://your-service.search.windows.net
AZURE_SEARCH_INDEX_NAME=products-index
EMBEDDING_DIMENSION=3072
```

### 2. Jupyter Notebook 실행

```bash
# 프로젝트 루트에서 실행
jupyter notebook

# 또는 VS Code에서 .ipynb 파일 직접 실행
```

### 3. 노트북 순서대로 실행

01번부터 09번까지 순서대로 셀을 실행하세요.

## 📦 필요한 패키지

프로젝트 루트의 `requirements.txt` 참조:

```bash
pip install -r ../requirements.txt
```

주요 패키지:
- `openai` - Azure OpenAI API 클라이언트
- `azure-search-documents` - Azure AI Search SDK
- `azure-identity` - Azure 인증

## 🎯 학습 후

Tutorial을 모두 완료한 후 `app/` 폴더의 Streamlit 애플리케이션을 실행하세요:

```bash
cd ../app
streamlit run app.py
```

애플리케이션은 Tutorial에서 생성한 `products-index`를 사용합니다.

## ⚠️ 주의사항

- Azure CLI 로그인 필요: `az login`
- RBAC 권한 확인:
  - **Search Index Data Contributor** (인덱스 생성/데이터 업로드)
  - **Cognitive Services OpenAI User** (OpenAI API 사용)
- 인덱스 이름을 변경하면 `.env` 파일도 함께 수정하세요
