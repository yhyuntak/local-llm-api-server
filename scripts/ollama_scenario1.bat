@echo off
echo ========================================
echo     Ollama Scenario 1: Safe Start
echo ========================================

REM Stop all existing OLLAMA processes
echo Stopping all existing OLLAMA processes...
taskkill /f /im ollama.exe >nul 2>&1

REM Scenario 1: Safe Start Configuration
set OLLAMA_NUM_PARALLEL=1
set OLLAMA_MAX_LOADED_MODELS=1
set OLLAMA_GPU_LAYERS=25
set OLLAMA_BATCH_SIZE=128
set OLLAMA_FLASH_ATTENTION=1
set OLLAMA_KEEP_ALIVE=5m

echo Configuration:
echo - NUM_PARALLEL: 1
echo - BATCH_SIZE: 128
echo - GPU_LAYERS: 25 (some layers on CPU)
echo - FLASH_ATTENTION: 1
echo.

echo Starting Ollama server with Scenario 1 settings...
echo Press Ctrl+C to stop
echo.

ollama serve