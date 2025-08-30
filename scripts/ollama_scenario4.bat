@echo off
echo ========================================
echo     Ollama Scenario 4: Maximum Performance
echo ========================================

REM Stop all existing OLLAMA processes
echo Stopping all existing OLLAMA processes...
taskkill /f /im ollama.exe >nul 2>&1

REM Scenario 4: Maximum Performance Configuration
set OLLAMA_NUM_PARALLEL=4
set OLLAMA_MAX_LOADED_MODELS=1
set OLLAMA_GPU_LAYERS=33
set OLLAMA_BATCH_SIZE=768
set OLLAMA_FLASH_ATTENTION=1
set OLLAMA_KEEP_ALIVE=20m
set OLLAMA_MAX_QUEUE=2048
set OLLAMA_LOW_VRAM=false

echo Configuration:
echo - NUM_PARALLEL: 4
echo - BATCH_SIZE: 768
echo - GPU_LAYERS: 33
echo - FLASH_ATTENTION: 1
echo - MAX_QUEUE: 2048
echo - LOW_VRAM: false
echo.

echo WARNING: High memory usage scenario!
echo Monitor VRAM usage closely.
echo.

echo Starting Ollama server with Scenario 4 settings...
echo Press Ctrl+C to stop
echo.

ollama serve