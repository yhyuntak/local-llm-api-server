@echo off
echo ========================================
echo     Ollama Scenario Performance Test
echo ========================================
echo.

echo Available scenarios:
echo 1. Scenario 1: Safe Start (PARALLEL=1, BATCH=128)
echo 2. Scenario 2: Balanced Performance (PARALLEL=2, BATCH=256)
echo 3. Scenario 3: High Performance (PARALLEL=3, BATCH=512)
echo 4. Scenario 4: Maximum Performance (PARALLEL=4, BATCH=768)
echo 5. Performance test only (current Ollama settings)
echo.

set /p choice="Select scenario to test (1-5): "

if "%choice%"=="1" (
    echo.
    echo ========================================
    echo Testing Scenario 1: Safe Start
    echo ========================================
    echo.
    echo 1. Start Ollama with Scenario 1 settings in another terminal:
    echo    scripts\ollama_scenario1.bat
    echo.
    echo 2. Start your FastAPI server in another terminal:
    echo    scripts\run_dev.bat
    echo.
    echo 3. Press any key when both servers are running...
    pause >nul
    echo.
    echo Starting performance test for Scenario 1...
    uv run python performance_test.py -r 30 -c 10
) else if "%choice%"=="2" (
    echo.
    echo ========================================
    echo Testing Scenario 2: Balanced Performance
    echo ========================================
    echo.
    echo 1. Start Ollama with Scenario 2 settings in another terminal:
    echo    scripts\ollama_scenario2.bat
    echo.
    echo 2. Start your FastAPI server in another terminal:
    echo    scripts\run_dev.bat
    echo.
    echo 3. Press any key when both servers are running...
    pause >nul
    echo.
    echo Starting performance test for Scenario 2...
    uv run python performance_test.py -r 30 -c 10
) else if "%choice%"=="3" (
    echo.
    echo ========================================
    echo Testing Scenario 3: High Performance
    echo ========================================
    echo.
    echo 1. Start Ollama with Scenario 3 settings in another terminal:
    echo    scripts\ollama_scenario3.bat
    echo.
    echo 2. Start your FastAPI server in another terminal:
    echo    scripts\run_dev.bat
    echo.
    echo 3. Press any key when both servers are running...
    pause >nul
    echo.
    echo Starting performance test for Scenario 3...
    uv run python performance_test.py -r 30 -c 10
) else if "%choice%"=="4" (
    echo.
    echo ========================================
    echo Testing Scenario 4: Maximum Performance
    echo ========================================
    echo.
    echo WARNING: This scenario uses high memory!
    echo Monitor VRAM usage closely.
    echo.
    echo 1. Start Ollama with Scenario 4 settings in another terminal:
    echo    scripts\ollama_scenario4.bat
    echo.
    echo 2. Start your FastAPI server in another terminal:
    echo    scripts\run_dev.bat
    echo.
    echo 3. Press any key when both servers are running...
    pause >nul
    echo.
    echo Starting performance test for Scenario 4...
    uv run python performance_test.py -r 30 -c 10
) else if "%choice%"=="5" (
    echo.
    echo Running performance test with current Ollama settings...
    uv run python performance_test.py -r 100 -c 10
) else (
    echo Invalid choice. Exiting...
    pause
    exit /b 1
)

echo.
echo ========================================
echo Test completed!
echo ========================================
echo.
echo Check the generated JSON file for detailed results.
echo Compare results across different scenarios to find the optimal configuration.
echo.
pause