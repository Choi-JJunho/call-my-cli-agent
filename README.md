# Local LLM API Server

Python FastAPI 서버로 로컬에 설치된 LLM CLI 도구들을 API로 호출할 수 있습니다.

## 지원 모델

- **codex** - `codex exec "prompt"`
- **claude** - `claude -p "prompt"`
- **gemini** - `gemini -p "prompt"`
- **copilot** - `copilot -p "prompt"`

## 설치 및 설정

### 1. 가상 환경 생성

```bash
python3 -m venv venv
```

### 2. 가상 환경 활성화

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

## 실행

가상 환경이 활성화된 상태에서:

```bash
python main.py
```

서버는 `http://localhost:12341`에서 실행됩니다.

## API 사용법

### 1. 기본 정보 확인

```bash
curl http://localhost:12341/
```

### 2. 헬스 체크

```bash
curl http://localhost:12341/health
```

### 3. LLM 호출

```bash
curl -X POST http://localhost:12341/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude",
    "prompt": "Hello, how are you?"
  }'
```

**요청 본문:**
```json
{
  "model": "codex" | "claude" | "gemini" | "copilot",
  "prompt": "your prompt here"
}
```

**응답 예시:**
```json
{
  "model": "claude",
  "output": "LLM의 응답 내용",
  "error": null
}
```

## 예시

### Codex 사용

```bash
curl -X POST http://localhost:12341/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "codex",
    "prompt": "Write a Python function to calculate fibonacci"
  }'
```

### Claude 사용

```bash
curl -X POST http://localhost:12341/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude",
    "prompt": "Explain quantum computing"
  }'
```

### Gemini 사용

```bash
curl -X POST http://localhost:12341/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini",
    "prompt": "What is machine learning?"
  }'
```

### Copilot 사용

```bash
curl -X POST http://localhost:12341/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "copilot",
    "prompt": "Suggest code improvements"
  }'
```

## Python에서 사용하기

```python
import requests

response = requests.post(
    "http://localhost:12341/generate",
    json={
        "model": "claude",
        "prompt": "Hello!"
    }
)

result = response.json()
print(result["output"])
```

## 주의사항

- 각 CLI 도구(codex, claude, gemini, copilot)가 시스템 PATH에 설치되어 있어야 합니다
- 명령어 실행 타임아웃은 60초로 설정되어 있습니다
- 에러 발생 시 HTTP 500 상태 코드와 함께 에러 메시지가 반환됩니다

## API 문서

서버 실행 후 다음 URL에서 자동 생성된 API 문서를 확인할 수 있습니다:

- Swagger UI: http://localhost:12341/docs
- ReDoc: http://localhost:12341/redoc
