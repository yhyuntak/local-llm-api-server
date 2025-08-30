@echo off
echo ========================================
echo     Local LLM API Server (Windows)
echo ========================================
echo.

REM Check if uv is installed
uv --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: uv is not installed or not in PATH
    echo Please install uv first: https://docs.astral.sh/uv/
    pause
    exit /b 1
)

REM Check if Ollama is running
echo Checking Ollama server...
curl -s http://localhost:11434 >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Ollama server is not running on localhost:11434
    echo Please start Ollama server first: 'ollama serve'
    echo.
    set /p continue="Continue anyway? (y/n): "
    if /i not "%continue%"=="y" (
        pause
        exit /b 1
    )
)

echo Starting Local LLM API Server...
echo Server will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.

REM Start the FastAPI server
uv run python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload --workers 1

echo.
echo Server stopped.
pause