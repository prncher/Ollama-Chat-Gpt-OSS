# 🧠 A chat server using FastAPI, Ollama and gpt-oss

This project demonstrates how to build a **ollama gpt-oss based chat server** system using:
 
- 🦙 **Ollama** running `gpt-oss:20b` for reasoning


## 🧰 Getting Started

### 1. Install Ollama
Download and install **Ollama 0.12.3** from the official site:  
👉 [https://ollama.com/download/windows](https://ollama.com/download/windows)

### 2. Pull the Model
After installing Ollama, pull the required model:

```bash
ollama gpt-oss:20b
```

### 3. Install Python Dependencies
Install [**uv**](https://github.com/astral-sh/uv) (a fast Python package installer):

```bash
pip install uv
```

### 4. Create and Activate a Virtual Environment

#### 🪟 **Windows**
```bash
uv venv
.venv\Scripts\activate
```

#### 🍎 **macOS / 🐧 Linux**
```bash
uv venv
source .venv/bin/activate
```

### 5. Install the Project in Editable Mode
This installs dependencies and links the local project for development:

```bash
uv pip install -e .
```

> 📝 **VS Code Tip**: You may need to manually select the `.venv` Python interpreter to resolve imports.

### 6. Run the Chat Server
Start the MCP server to handle tool execution:

```bash
uvicorn src.server:app --host 0.0.0.0 --port 5600
```
