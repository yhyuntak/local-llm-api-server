# Local LLM API Server

A local LLM server providing OpenAI-compatible API. Uses Ollama as backend and runs stably on Windows environment.

## 🎯 Key Features

- **Full OpenAI Chat Completions API compatibility**
- **Ollama backend** integration supporting various LLM models
- **FastAPI-based** high-performance REST API server
- **Internal network support** (accessible from NAS servers, etc.)
- **Structured logging** system
- **Performance testing** tools included

## 📋 Prerequisites

### 1. Python Environment
- **Python 3.10 or higher** required
- **uv** package manager ([Installation Guide](https://docs.astral.sh/uv/))

### 2. Ollama Installation
- **Ollama** installation ([Official Site](https://ollama.com))
- **qwen3:14b** model download required

```bash
# Download model after Ollama installation
ollama pull qwen3:14b
```

## 🚀 Installation & Execution

### Method 1: Automated Setup Scripts (Recommended)

```bash
# 1. Install dependencies
scripts\setup.bat

# 2. Start Ollama server (separate terminal)
scripts\start_ollama.bat

# 3. Start API server
scripts\run_dev.bat
```

### Method 2: Manual Installation

```bash
# 1. Install dependencies
uv sync

# 2. Start Ollama server (separate terminal)
ollama serve

# 3. Check models
ollama list

# 4. Start API server
uv run python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload --workers 4
```

## 🌐 Access URLs

Once the server starts successfully, you can access it via:

- **Local**: http://localhost:8000
- **Internal Network**: http://192.168.219.114:8000
- **API Documentation**: http://localhost:8000/docs
- **Server Status**: http://localhost:8000/

## 📝 API Usage

### OpenAI-compatible Chat Completions API

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3:14b",
    "messages": [
      {"role": "user", "content": "Hello! Please write a simple Python code."}
    ],
    "temperature": 0.7,
    "num_predict": 150,
    "thinking": false
  }'
```

### Supported Parameters

- `model`: Model name (currently supports "qwen3:14b")
- `messages`: Message array (OpenAI format)
- `temperature`: Generation temperature (0.0-2.0)
- `num_predict`: Maximum number of tokens
- `top_k`: Top-K sampling (default: 20)
- `top_p`: Top-P sampling (default: 1.0)
- `repeat_penalty`: Repetition penalty (default: 0.0)
- `thinking`: Show reasoning process (default: false)

## 🏗️ Project Structure

```
├── main.py                    # FastAPI application entry point
├── chat/                      # OpenAI-compatible chat API
│   ├── models.py             # Pydantic data models
│   ├── router.py             # FastAPI router
│   └── service.py            # Business logic
├── model/                     # Model management
│   └── model_manager.py      # Ollama model manager
├── templates/                 # Prompt template system
│   ├── base.py              # Abstract template class
│   ├── qwen.py              # Qwen model template
│   └── service.py           # Factory Pattern implementation
├── core/                      # Common functionality
│   ├── logging.py           # Logging system
│   └── middleware.py        # Middleware
├── scripts/                   # Execution scripts
│   ├── setup.bat            # Dependency installation
│   ├── start_ollama.bat     # Ollama server startup
│   ├── run_dev.bat          # Development server execution
│   └── run_performance_test.bat # Performance testing
└── logs/                      # Log files
    └── app.log               # Application logs
```

## 🧪 Performance Testing

The project includes performance testing tools:

```bash
# Run performance test
scripts\run_performance_test.bat

# Or run directly
uv run python performance_test.py
```

## 🔧 Configuration & Tuning

### Ollama Performance Optimization

```bash
# Optimize parallel processing with environment variables
set OLLAMA_NUM_PARALLEL=16
set OLLAMA_MAX_LOADED_MODELS=3
set OLLAMA_MAX_QUEUE=512
```

### Log Level Adjustment

Logs are saved to `logs/app.log` and retained for 30 days.

## 🌍 Network Environment

### Internal Network Access

- **Windows Desktop**: `192.168.219.114:8000`
- **NAS Server**: `192.168.219.102`
- **Router**: `192.168.219.1`

### Firewall Configuration

Port 8000 must be allowed in Windows Defender Firewall.

## 🔍 Troubleshooting

### Common Issues

1. **Ollama server won't start**
   ```bash
   # Check Ollama installation
   ollama --version
   
   # Start server manually
   ollama serve
   ```

2. **Model not found**
   ```bash
   # Check model list
   ollama list
   
   # Download model
   ollama pull qwen3:14b
   ```

3. **Port conflict**
   ```bash
   # Run on different port
   uv run python -m uvicorn main:app --host 0.0.0.0 --port 8080
   ```

4. **Out of memory**
   - Use smaller model: `ollama pull qwen2.5:7b`
   - Reduce `OLLAMA_NUM_PARALLEL` value

### Log Monitoring

```bash
# Real-time log monitoring
tail -f logs\app.log
```

## 📈 Development Log

For detailed development process and performance analysis, see [DEVELOPMENT_LOG.md](DEVELOPMENT_LOG.md).

## 🤝 Contributing

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is provided under the MIT License.