@echo off
echo ========================================
echo     Ollama Scenario 5: Test Higher Parallel
echo ========================================

REM Stop all existing OLLAMA processes
echo Stopping all existing OLLAMA processes...
taskkill /f /im ollama.exe >nul 2>&1

REM Scenario 5: Higher Parallel Test
set OLLAMA_NUM_PARALLEL=4
set OLLAMA_MAX_LOADED_MODELS=1
set OLLAMA_GPU_LAYERS=33
set OLLAMA_BATCH_SIZE=512
set OLLAMA_FLASH_ATTENTION=1
set OLLAMA_KEEP_ALIVE=15m

echo Configuration:
echo - NUM_PARALLEL: 4
echo - BATCH_SIZE: 512
echo - GPU_LAYERS: 33
echo - FLASH_ATTENTION: 1
echo.

echo Starting Ollama server with higher parallel settings...
echo Press Ctrl+C to stop
echo.

ollama serve