@echo off
echo ========================================
echo     Ollama Scenario 3: High Performance
echo ========================================

REM Stop all existing OLLAMA processes
echo Stopping all existing OLLAMA processes...
taskkill /f /im ollama.exe >nul 2>&1

REM Scenario 3: High Performance Configuration
set OLLAMA_NUM_PARALLEL=3
set OLLAMA_MAX_LOADED_MODELS=1
set OLLAMA_GPU_LAYERS=33
set OLLAMA_BATCH_SIZE=512
set OLLAMA_FLASH_ATTENTION=1
set OLLAMA_KEEP_ALIVE=15m
set OLLAMA_MAX_QUEUE=1024
REM Low VRAM mode cannot be disabled via environment variables
REM Try memory optimization instead
set OLLAMA_KV_CACHE_TYPE=q8_0
set OLLAMA_MAX_VRAM=14GiB

echo Configuration:
echo - NUM_PARALLEL: 3
echo - BATCH_SIZE: 512
echo - GPU_LAYERS: 33
echo - FLASH_ATTENTION: 1
echo - MAX_QUEUE: 1024
echo - KV_CACHE_TYPE: q8_0 (memory optimization)
echo - MAX_VRAM: 14GiB
echo.

echo Starting Ollama server with Scenario 3 settings...
echo Press Ctrl+C to stop
echo.

ollama serve