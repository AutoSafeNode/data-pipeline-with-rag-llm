# Data Scooper (Python Version)

데이터 파이프라인 프로젝트 - 엑셀/PDF 파일에서 RAG(Retrieval-Augmented Generation) 데이터 생성 및 LLM 통합

## 🔄 Python 버전으로 완전히 재작성되었습니다!

이 프로젝트는 이제 Python으로 작성되었으며, 비동기 처리와 최신 데이터 처리 라이브러리를 활용합니다.

## 프로젝트 개요

Data Scooper는 엑셀 및 PDF 파일에서 데이터를 추출하여 RAG 시스템을 위한 벡터 임베딩을 생성하고, 이를 활용하여 LLM과 통합하는 종합 데이터 파이프라인입니다. Python 비동기 처리를 통해 빠르고 효율적인 데이터 처리를 제공합니다.

## 주요 기능

### 1. 엑셀 → RAG 파이프라인
- 엑셀 파일(.xlsx, .xls, .xlsm) 읽기
- 데이터 추출 및 텍스트 변환
- 청킹(Chunking) 및 임베딩 생성
- 벡터 저장소 저장

### 2. PDF → RAG 파이프라인
- PDF 파일 읽기 및 텍스트 추출
- 페이지별 데이터 처리
- 구조화된 데이터 추출
- 청킹 및 임베딩 생성
- 벡터 저장소 저장

### 3. RAG 시스템
- 텍스트 청킹 및 전처리
- 임베딩 생성 (현재는 해시 기반, 프로덕션에서는 API 사용)
- 벡터 저장소 관리
- 유사도 검색

### 4. LLM 통합
- Google Gemini API 연동
- RAG 컨텍스트를 활용한 질의응답
- 재무 데이터 분석 템플릿

### 5. RAG 평가 및 모니터링 🆕
- **RAGAS 프레임워크**: RAG 시스템 성능 평가
  - Faithfulness (충실도)
  - Answer Relevancy (답변 관련성)
  - Context Precision (컨텍스트 정확도)
  - Context Recall (컨텍스트 재현율)
- **LangSmith 통합**: RAG 파이프라인 추적 및 모니터링
  - 실시간 성능 추적
  - 디버깅 및 최적화 도구
  - 피드백 수집 및 분석

## 프로젝트 구조

```
data-scooper/
├── main.py                   # 메인 진입점
├── setup.py                  # 패키지 설정
├── requirements.txt          # Python 의존성
├── src_python/              # Python 소스 디렉토리
│   ├── __init__.py
│   ├── pipelines/           # 데이터 파이프라인 모듈
│   │   ├── __init__.py
│   │   ├── excel_pipeline.py  # 엑셀 → RAG 파이프라인
│   │   └── pdf_pipeline.py    # PDF → RAG 파이프라인
│   ├── processors/          # 데이터 처리 모듈
│   │   ├── __init__.py
│   │   ├── excel_processor.py # 엑셀 데이터 처리
│   │   ├── pdf_processor.py   # PDF 데이터 처리
│   │   └── text_processor.py  # 텍스트 전처리
│   ├── rag/                 # RAG 생성 모듈
│   │   ├── __init__.py
│   │   ├── embeddings.py      # 임베딩 생성
│   │   └── vector_store.py    # 벡터 저장소
│   ├── llm/                 # LLM 통합 모듈
│   │   ├── __init__.py
│   │   └── gemini_client.py   # Gemini API 클라이언트
│   ├── evaluation/          # RAG 평가 및 모니터링 🆕
│   │   ├── __init__.py
│   │   ├── ragas_evaluator.py    # RAGAS 평가 모듈
│   │   └── langsmith_integration.py # LangSmith 통합
│   └── utils/               # 유틸리티
│       ├── __init__.py
│       ├── logger.py          # 로깅 유틸리티
│       └── config.py          # 설정 관리
├── data/                    # 데이터 디렉토리
│   ├── input/              # 입력 데이터
│   │   ├── excel/          # 엑셀 파일
│   │   └── pdf/            # PDF 파일
│   ├── output/             # 출력 데이터
│   └── vectorstore/        # 벡터 저장소
│       ├── vectors/        # 임베딩 데이터
│       ├── cache/          # 임베딩 캐시
│       └── index.json      # 저장소 인덱스
├── config/                 # 설정 파일
│   └── config.json        # 환경 설정
├── .env.example           # 환경 변수 예시
├── .gitignore            # Git 무시 파일
└── README.md             # 프로젝트 문서

```

## 설치 방법

### 1. Python 요구사항

- Python 3.8 이상
- pip (Python 패키지 매니저)

### 2. 의존성 설치

```bash
# pip를 사용한 설치
pip install -r requirements.txt

# 또는 setup.py를 사용한 설치
pip install -e .
```

### 3. 설정 파일 구성

`config/config.json` 파일에서 API 키 및 설정을 구성하세요:

```json
{
  "gemini": {
    "apiKey": "YOUR_GEMINI_API_KEY",
    "model": "gemini-pro",
    "temperature": 0.3,
    "topK": 40,
    "topP": 0.95,
    "maxOutputTokens": 2048
  },
  "pipelines": {
    "excel": {
      "inputDir": "./data/input/excel",
      "outputDir": "./data/output/rag",
      "chunkSize": 1000,
      "chunkOverlap": 200
    },
    "pdf": {
      "inputDir": "./data/input/pdf",
      "outputDir": "./data/output/rag",
      "chunkSize": 1500,
      "chunkOverlap": 300
    }
  },
  "rag": {
    "embeddingModel": "text-embedding-004",
    "vectorStorePath": "./data/vectorstore",
    "maxDocuments": 1000
  }
}
```

## 사용 방법

### 1. 엑셀 → RAG 파이프라인 실행

```bash
# 단일 파일 처리
python main.py excel path/to/file.xlsx

# 디렉토리 전체 처리
python main.py excel ./data/input/excel
```

### 2. PDF → RAG 파이프라인 실행

```bash
# 단일 파일 처리
python main.py pdf path/to/file.pdf

# 디렉토리 전체 처리
python main.py pdf ./data/input/pdf
```

### 3. 전체 파이프라인 실행

```bash
python main.py all ./data/input/excel ./data/input/pdf
```

### 4. 파이프라인 모듈 직접 사용

```python
import asyncio
from src_python.pipelines.excel_pipeline import ExcelToRAGPipeline
from src_python.utils.config import load_config

async def process_excel():
    config = load_config()
    pipeline = ExcelToRAGPipeline(config.pipelines["excel"])
    result = await pipeline.run("./data/input/excel")
    print(result)

asyncio.run(process_excel())
```

## 파이프라인 처리 과정

### 엑셀 → RAG 파이프라인

1. **엑셀 파일 읽기**: `.xlsx`, `.xls`, `.xlsm` 파일을 읽고 모든 시트 데이터 추출
2. **텍스트 변환**: 엑셀 데이터를 읽기 쉬운 텍스트 형식으로 변환
3. **청킹**: 텍스트를 적절한 크기의 청크로 분할 (기본 1000자, 오버랩 200자)
4. **전처리**: 텍스트 정규화 및 검증
5. **임베딩 생성**: 각 청크에 대한 벡터 임베딩 생성
6. **벡터 저장소 저장**: 임베딩을 벡터 저장소에 저장 및 인덱싱
7. **결과 저장**: 처리 결과를 JSON 파일로 저장

### PDF → RAG 파이프라인

1. **PDF 파일 읽기**: PDF 파일에서 텍스트 및 메타데이터 추출
2. **페이지 분할**: 페이지별로 텍스트 분할
3. **구조화된 데이터 추출**: 제목, 키 포인트 등 추출
4. **청킹**: 텍스트를 청크로 분할 (기본 1500자, 오버랩 300자)
5. **전처리**: 텍스트 정규화 및 검증
6. **임베딩 생성**: 각 청크에 대한 벡터 임베딩 생성
7. **벡터 저장소 저장**: 임베딩을 벡터 저장소에 저장 및 인덱싱
8. **결과 저장**: 처리 결과를 JSON 파일로 저장

## RAG 시스템 활용

### 벡터 검색

```python
import asyncio
from src_python.rag.vector_store import VectorStore
from src_python.rag.embeddings import EmbeddingGenerator
from src_python.utils.config import load_config

async def search_vectors():
    config = load_config()
    vector_store = VectorStore(config.rag)
    embedding_generator = EmbeddingGenerator(config.rag)
    
    # 쿼리 임베딩 생성
    query = "찾고 싶은 내용"
    query_embedding = await embedding_generator.generate_embedding(query)
    
    # 유사한 문서 검색
    results = await vector_store.search(query_embedding, top_k=5)
    print(results)

asyncio.run(search_vectors())
```

### LLM 질의응답

```python
import asyncio
from main import DataScooper
from src_python.utils.config import load_config

async def query_llm():
    config = load_config()
    scooper = DataScooper(config)
    
    # RAG 컨텍스트와 함께 LLM 질의
    query = "데이터에 대한 질문"
    rag_data = {"context": "검색된 RAG 데이터"}
    response = await scooper.query_with_rag(query, rag_data)
    print(response)

asyncio.run(query_llm())
```

## 🆕 RAG 평가 및 모니터링

### RAGAS로 RAG 시스템 평가하기

RAGAS 프레임워크를 사용하여 RAG 시스템의 성능을 정량적으로 평가할 수 있습니다.

```bash
# RAGAS 평가 실행
python evaluate_rag.py ragas --sample-size 20

# 전체 평가 실행
python evaluate_rag.py all
```

### 프로그래매틱하게 RAGAS 사용하기

```python
import asyncio
from src_python.evaluation.ragas_evaluator import create_ragas_evaluator

async def evaluate_rag():
    evaluator = create_ragas_evaluator()

    # 평가 데이터 준비
    questions = ["What is the purpose of this document?"]
    answers = ["This document provides comprehensive analysis..."]
    contexts = [["Key information from the document..."]]

    # 평가 실행
    result = await evaluator.evaluate_rag_system(
        questions=questions,
        answers=answers,
        contexts=contexts
    )

    print(f"Faithfulness: {result.metrics['faithfulness']:.4f}")
    print(f"Answer Relevancy: {result.metrics['answer_relevancy']:.4f}")

asyncio.run(evaluate_rag())
```

### LangSmith로 파이프라인 모니터링하기

LangSmith를 사용하여 RAG 파이프라인의 실행을 추적하고 모니터링할 수 있습니다.

```bash
# LangSmith 테스트
python evaluate_rag.py langsmith
```

### LangSmith 프로그래매틱 통합

```python
import asyncio
from src_python.evaluation.langsmith_integration import create_langsmith_integration

async def trace_pipeline():
    integration = create_langsmith_integration()

    # RAG 쿼리 추적
    await integration.trace_rag_query(
        question="What is Data Scooper?",
        context=["Data Scooper is a RAG pipeline system."],
        answer="Data Scooper converts documents to RAG format.",
        metadata={"version": "1.0", "test": True}
    )

    # 통계 확인
    stats = await integration.get_run_statistics()
    print(f"Total runs: {stats['total_runs']}")
    print(f"Success rate: {stats['success_rate']:.2%}")

asyncio.run(trace_pipeline())
```

### 평가 메트릭 이해하기

**RAGAS 메트릭**:
- **Faithfulness**: 생성된 답변이 검색된 컨텍스트에 얼마나 충실한가
- **Answer Relevancy**: 답변이 질문에 얼마나 관련성이 있는가
- **Context Precision**: 검색된 컨텍스트가 얼마나 정확한가
- **Context Recall**: 관련 컨텍스트를 얼마나 잘 찾아내는가

### 🆕 에이스(A's) 야구 데이터셋으로 RAG 평가하기

프로젝트에 오클랜드 애슬레틱스(A's) 야구 팀 데이터셋이 포함되어 있어 바로 RAG 평가를 테스트할 수 있습니다!

**데이터셋 특징**:
- 100개의 평가 샘플
- 7개 카테고리 (팀 정보, 역사, 선수, 구장, 라이벌, 머니볼, 최근 성적)
- 질문, 컨텍스트, 답변, 정답 포함
- RAGAS/Hugging Face 형식 지원

```bash
# 데이터셋 분석
python3 analyze_dataset.py

# RAGAS 평가 테스트 (샘플 10개)
python3 test_ragas_with_as_dataset.py --samples 10

# 데이터셋 업로드 준비
python3 upload_to_ragas.py --dataset data/evaluation_datasets/as_evaluation_dataset_*.json
```

**데이터셋 카테고리**:
- `team_info` (30개): 팀 기본 정보
- `players` (20개): 전설적인 선수들
- `history` (10개): 역사적 성과
- `stadium` (10개): 구장 정보
- `rivalries` (10개): 라이벌 관계
- `moneyball` (10개): 머니볼 전략
- `recent` (10개): 최근 성적

## 데이터 포맷

### 입력 데이터

**엑셀 파일**:
- 지원 형식: `.xlsx`, `.xls`, `.xlsm`
- 다중 시트 지원
- 헤더 행 자동 감지

**PDF 파일**:
- 지원 형식: `.pdf`
- 텍스트 기반 PDF 권장
- 멀티페이지 지원

### 출력 데이터

파이프라인 실행 결과로 다음과 같은 JSON 파일이 생성됩니다:

```json
{
  "processed": 5,
  "successful": 4,
  "failed": 1,
  "results": [
    {
      "success": true,
      "fileName": "data.xlsx",
      "chunks": 150,
      "embeddings": 150,
      "vectorStoreId": "doc-1234567890-abc123"
    }
  ]
}
```

## 모듈 상세 설명

### ExcelProcessor
- 엑셀 파일 읽기 및 파싱
- 시트별 데이터 추출
- 텍스트 형식 변환
- 청킹 및 메타데이터 생성

### PDFProcessor
- PDF 파일 읽기 및 텍스트 추출
- 페이지별 처리
- 구조화된 데이터 추출 (제목, 키 포인트)
- 청킹 및 메타데이터 생성

### TextProcessor
- 텍스트 정규화
- 품질 검증
- 메타데이터 강화
- 작은 청크 병합

### EmbeddingGenerator
- 텍스트 임베딩 생성
- 배치 처리
- 캐싱 지원
- 유사도 계산

### VectorStore
- 문서 저장 및 관리
- 벡터 검색
- 인덱싱
- 통계 및 내보내기

## 확장 가능성

### 프로덕션 환경에서의 임베딩

현재 구현은 해시 기반의 간단한 임베딩을 사용합니다. 프로덕션 환경에서는 다음 서비스 중 하나를 사용하도록 `EmbeddingGenerator`를 수정하세요:

- OpenAI Embeddings API
- Google Vertex AI Embeddings
- HuggingFace Transformers
- Cohere Embeddings

### 벡터 데이터베이스

대규모 데이터 처리를 위해 다음 벡터 데이터베이스를 통합할 수 있습니다:

- Pinecone
- Weaviate
- Qdrant
- Milvus
- Chroma

### 추가 파이프라인

다른 파일 형식을 위한 파이프라인을 쉽게 추가할 수 있습니다:

- Word 문서 (.docx)
- PowerPoint (.pptx)
- 이미지 (OCR)
- 웹페이지 (HTML)

## 환경 변수 선택 사항

`.env` 파일을 생성하여 환경 변수를 설정할 수 있습니다:

```env
GEMINI_API_KEY=your_api_key
EMBEDDING_MODEL=text-embedding-004
VECTOR_STORE_PATH=./data/vectorstore

# RAGAS 평가를 위한 설정 🆕
OPENAI_API_KEY=your_openai_api_key_for_ragas_evaluation
RAGAS_EVALUATION_MODEL=gpt-4o-mini
RAGAS_EMBEDDING_MODEL=text-embedding-004

# LangSmith 모니터링을 위한 설정 🆕
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=data-scooper
```

## Python 버전의 주요 특징

### 🚀 비동기 처리
- `asyncio`를 사용한 비동기 I/O 처리
- 병렬 파일 처리로 빠른 속도
- 효율적인 리소스 활용

### 📊 강력한 데이터 처리
- `pandas`를 활용한 엑셀 데이터 처리
- `pdfplumber`를 통한 정확한 PDF 텍스트 추출
- `numpy`를 사용한 빠른 벡터 연산

### 🔧 타입 안전성
- 타입 힌트를 사용한 코드 안정성
- IDE 자동완성 지원
- 런타임 오류 감소

### 🎈 모듈화
- 재사용 가능한 컴포넌트 구조
- 플러그인 방식의 확장성
- 명확한 의존성 관리

### 🧪 테스트 친화적
- `pytest`를 사용한 단위 테스트
- 비동기 테스트 지원
- 모의 객체(Mock) 사용 용이

## 트러블슈팅

### 일반적인 문제

1. **API 키 오류**: `config/config.json`에서 Gemini API 키 확인
2. **파일을 찾을 수 없음**: 입력 파일 경로가 올바른지 확인
3. **메모리 부족**: 대용량 파일 처리 시 `chunkSize` 조정
4. **임베딩 오류**: 임베딩 API 설정 확인
5. **비동기 함수 오류**: `async/await` 패턴이 올바른지 확인

### Python 개발자를 위한 팁

1. **가상 환경 사용**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows
```

2. **패키지 업그레이드**:
```bash
pip install --upgrade -r requirements.txt
```

3. **디버깅**:
```python
# 로거 설정을 DEBUG 레벨로 변경
from src_python.utils.logger import get_logger
logger = get_logger()
logger.logger.setLevel(logging.DEBUG)
```

4. **성능 최적화**:
```python
# 병렬 처리를 활용한 대용량 파일 처리
import asyncio
from pathlib import Path

async def process_multiple_files(file_paths):
    tasks = [pipeline.run(file_path) for file_path in file_paths]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

5. **테스트 실행**:
```bash
pytest tests/ -v
# 또는 특정 테스트만 실행
pytest tests/test_excel_processor.py -v
```

1. **API 키 오류**: `config/config.json`에서 Gemini API 키 확인
2. **파일을 찾을 수 없음**: 입력 파일 경로가 올바른지 확인
3. **메모리 부족**: 대용량 파일 처리 시 `chunkSize` 조정
4. **임베딩 오류**: 임베딩 API 설정 확인

### 로그 확인

모든 작업은 콘솔에 로그가 출력됩니다. 문제 발생 시 로그를 확인하세요.

## 라이선스

MIT

## 기여

이 프로젝트에 기여하고 싶다면 Pull Request를 제출해 주세요.

### Python 코드 스타일 가이드

- PEP 8 스타일 가이드 준수
- 타입 힌트 사용 권장
- 독스트링(Docstring) 작성 권장
- `black` 포매터 사용 권장
- `flake8` 린터 사용 권장

### 개발 환경 설정

```bash
# 개발 의존성 설치
pip install -e ".[dev]"

# 코드 포맷팅
black src_python/ tests/

# 린팅
flake8 src_python/ tests/

# 테스트 실행
pytest tests/ -v

# 커버리지 확인
pytest --cov=src_python tests/
```

## 📞 연락처

질문이나 문의사항이 있으면 이슈를 생성해 주세요.

---

## 🐍 Python 버전 변경사항

### v1.0.0 (Python Version)
- ✅ Node.js에서 Python으로 완전 재작성
- ✅ 비동기 처리(`asyncio`) 도입으로 성능 향상
- ✅ 타입 힌트 추가로 코드 안정성 강화
- ✅ 현대적인 Python 패키지 구조 적용
- ✅ 테스트 프레임워크(`pytest`) 통합
- ✅ 강력한 데이터 처리 라이브러리 활용 (pandas, numpy)
- ✅ 개선된 로깅 및 오류 처리
- ✅ 더 나은 문서화 및 타입 안전성

## 연락처

질문이나 문의사항이 있으면 이슈를 생성해 주세요.
