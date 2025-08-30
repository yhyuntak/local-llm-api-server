@echo off
echo ========================================
echo     Ollama Scenario 2: Balanced Performance
echo ========================================

REM Stop all existing OLLAMA processes
echo Stopping all existing OLLAMA processes...
taskkill /f /im ollama.exe >nul 2>&1

REM Scenario 2: Balanced Performance Configuration
set OLLAMA_NUM_PARALLEL=2
set OLLAMA_MAX_LOADED_MODELS=1
set OLLAMA_GPU_LAYERS=33
set OLLAMA_BATCH_SIZE=256
set OLLAMA_FLASH_ATTENTION=1
set OLLAMA_KEEP_ALIVE=10m

echo Configuration:
echo - NUM_PARALLEL: 2
echo - BATCH_SIZE: 256
echo - GPU_LAYERS: 33
echo - FLASH_ATTENTION: 1
echo.

echo Starting Ollama server with Scenario 2 settings...
echo Press Ctrl+C to stop
echo.

ollama serve