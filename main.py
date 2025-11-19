import subprocess
from typing import Literal, Optional, Tuple
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Local LLM API Server")


class PromptRequest(BaseModel):
    prompt: str
    model: Literal["claude", "gemini", "copilot"]


class LLMResponse(BaseModel):
    model: str
    output: str
    error: Optional[str] = None


def execute_claude(prompt: str) -> Tuple[str, Optional[str]]:
    """Execute claude CLI command"""
    try:
        result = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            timeout=60
        )
        if result.returncode == 0:
            return result.stdout.strip(), None
        else:
            return "", result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "", "Command timed out after 60 seconds"
    except FileNotFoundError:
        return "", "claude command not found. Please ensure it's installed and in PATH"
    except Exception as e:
        return "", f"Error executing claude: {str(e)}"


def execute_gemini(prompt: str) -> Tuple[str, Optional[str]]:
    """Execute gemini CLI command"""
    try:
        result = subprocess.run(
            ["gemini", "-p", prompt],
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            timeout=60
        )
        if result.returncode == 0:
            return result.stdout.strip(), None
        else:
            return "", result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "", "Command timed out after 60 seconds"
    except FileNotFoundError:
        return "", "gemini command not found. Please ensure it's installed and in PATH"
    except Exception as e:
        return "", f"Error executing gemini: {str(e)}"


def execute_copilot(prompt: str) -> Tuple[str, Optional[str]]:
    """Execute copilot CLI command"""
    try:
        result = subprocess.run(
            ["copilot", "-p", prompt],
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            timeout=60
        )
        if result.returncode == 0:
            return result.stdout.strip(), None
        else:
            return "", result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "", "Command timed out after 60 seconds"
    except FileNotFoundError:
        return "", "copilot command not found. Please ensure it's installed and in PATH"
    except Exception as e:
        return "", f"Error executing copilot: {str(e)}"


@app.get("/")
def root():
    return {
        "message": "Local LLM API Server",
        "available_models": ["claude", "gemini", "copilot"],
        "endpoints": {
            "/generate": "POST - Generate text from a prompt",
            "/health": "GET - Check server health"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/generate", response_model=LLMResponse)
def generate(request: PromptRequest):
    """Generate text using the specified LLM model"""

    executors = {
        "claude": execute_claude,
        "gemini": execute_gemini,
        "copilot": execute_copilot
    }

    executor = executors.get(request.model)
    if not executor:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model: {request.model}"
        )

    output, error = executor(request.prompt)

    if error and not output:
        raise HTTPException(status_code=500, detail=error)

    return LLMResponse(
        model=request.model,
        output=output,
        error=error
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=12341)
