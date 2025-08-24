#!/bin/bash
# Development server startup script
echo "Starting Local LLM API Server..."
uv run python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload