# Ollama + LangSmith - AI Assistant Application

## 📋 Project Overview

This is a Streamlit-based web application that integrates **Ollama** (a local LLM framework) with **LangSmith** (LangChain's monitoring and debugging platform). The application creates an intelligent chatbot assistant that processes user questions and provides responses using the Gemma 2B model running locally.

### GUI

<img width="1710" height="966" alt="image" src="https://github.com/user-attachments/assets/cd24eb02-917f-4dd3-bf1b-f93cf42f4418" />

## 🎯 Key Features

- **Local LLM Processing**: Uses Ollama with the Gemma 2B model for on-device AI inference
- **LangSmith Integration**: Full tracing and monitoring of LLM calls for debugging and optimization
- **User-Friendly Interface**: Built with Streamlit for an intuitive web-based UI
- **LangChain Pipeline**: Leverages LangChain's robust prompt engineering and output parsing
- **Privacy-First Approach**: All processing happens locally on your machine
- **Real-time Monitoring**: Track all LLM interactions and performance metrics

## 🏗️ Architecture & Components

### 1. **Dependencies Overview**

| Package | Purpose |
|---------|---------|
| `langchain_ollama` | Integration bridge between Ollama and LangChain |
| `streamlit` | Web UI framework for interactive applications |
| `python-dotenv` | Environment variable management for sensitive data |
| `langchain_core` | Core LangChain utilities (prompts, parsers, output handlers) |
| `ollama` | Local LLM runtime and model management |

### 2. **LangSmith Configuration Details** (Lines 12-15)

```python
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
```

**Detailed Breakdown:**
- **LANGCHAIN_API_KEY**: 
  - Authentication token for accessing LangSmith API
  - Obtained from LangSmith dashboard at https://smith.langchain.com
  - Enables secure communication with monitoring service

- **LANGCHAIN_TRACING_V2**: 
  - Flag to enable tracing infrastructure
  - Set to "true" to activate automatic logging
  - Records all LLM calls, inputs, outputs, and metadata

- **LANGCHAIN_PROJECT**: 
  - Organizes traces into logical project groups
  - Helps categorize and filter interactions in LangSmith dashboard
  - Custom project names can be created as needed

### 3. **Prompt Template Architecture** (Lines 17-22)

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant Please respond to the questions asked."),
    ("user", "Question: {question}")
])
```

**Component Explanation:**
- **System Message (Role: "system")**:
  - Sets the model's behavior and personality
  - Provides context and instructions for the assistant
  - Affects all subsequent responses in the conversation
  
- **User Message (Role: "user")**:
  - Contains the actual user query
  - `{question}` is a placeholder replaced with user input at runtime
  - Supports dynamic variable injection

**Template Flow:**
```
User Input → Placeholder Substitution → Formatted Messages → LLM
```

### 4. **LLM Processing Chain** (Lines 26-28)

```python
llm = OllamaLLM(model="gemma:2b")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser
```

**Chain Architecture:**

```
┌─────────────────────┐
│  User Question      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  ChatPromptTemplate                 │
│  - Formats with system instructions │
│  - Injects question variable        │
└──────────┬────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  OllamaLLM (Gemma 2B)               │
│  - Processes formatted prompt       │
│  - Generates text response          │
│  - Runs locally on device           │
└──────────┬────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  StrOutputParser                    │
│  - Extracts string from response    │
│  - Handles formatting & cleanup     │
│  - Returns final text output        │
└──────────┬────────────────────────┘
           │
           ▼
┌─────────────────────┐
│  Final Response     │
└─────────────────────┘
```

**Component Details:**

- **prompt**: 
  - Converts raw user input into structured format
  - Ensures consistency in model interactions
  - Handles variable substitution dynamically

- **llm** (OllamaLLM):
  - Local inference engine using Gemma 2B model
  - No API calls needed (fully private)
  - Executes on your hardware (CPU/GPU)
  - Model name can be customized

- **output_parser** (StrOutputParser):
  - Extracts clean string output from model response
  - Removes formatting artifacts
  - Ensures usable text output

### 5. **Streamlit User Interface** (Lines 24-33)

```python
st.title("Ollama + LangSmith")
input_text = st.text_input("Ask a question to the assistant:")
llm = OllamaLLM(model="gemma:2b")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if input_text:
    with st.spinner("Thinking..."):
        response = chain.invoke({"question": input_text})
        st.write(response)
```

**UI Components:**

| Component | Purpose | Function |
|-----------|---------|----------|
| `st.title()` | Main heading | Displays "Ollama + LangSmith" at top |
| `st.text_input()` | User input field | Captures question from user |
| `st.spinner()` | Loading indicator | Shows "Thinking..." during processing |
| `st.write()` | Output display | Shows assistant response |

**Interaction Flow:**
```
1. Display title and input box
2. Wait for user to type question
3. Check if input_text has content
4. Show spinner
5. Process question through chain
6. Display response
7. Return to input state
```

## 🚀 How It Works - Step by Step

### Complete Interaction Flow

```
START
  ↓
[User Types Question]
  ↓
[Streamlit Captures Input]
  ↓
[Check if Input Not Empty]
  ├─→ YES → Continue
  └─→ NO  → Wait for Input
  ↓
[Show "Thinking..." Spinner]
  ↓
[ChatPromptTemplate Formats]
  ├─ System Instruction: "You are a helpful assistant..."
  ├─ User Input: {question}
  └─ Result: Structured message
  ↓
[Send to Ollama/Gemma 2B]
  ├─ Model processes locally
  ├─ Generates response
  └─ Returns raw output
  ↓
[StrOutputParser Cleans Output]
  ├─ Extracts string
  ├─ Removes artifacts
  └─ Returns clean text
  ↓
[LangSmith Captures Trace]
  ├─ Records prompt used
  ├─ Logs response
  ├─ Tracks latency
  └─ Stores metadata
  ↓
[Streamlit Displays Response]
  ├─ Remove spinner
  ├─ Show answer
  └─ Return to input
  ↓
[User Can Ask Another Question]
  ↓
END
```

### Data Flow Visualization

```
┌─────────────────────┐
│   Streamlit UI      │
│  (Web Interface)    │
└────────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ LangChain Core  │
    │ - Prompting     │
    │ - Chain Logic   │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────────┐
    │ Ollama + Gemma 2B   │
    │ (Local LLM Engine)  │
    └────────┬────────────┘
             │
             ▼
    ┌──────────────────┐
    │  LangSmith       │
    │  (Monitoring &   │
    │   Debugging)     │
    └──────────────────┘
```

## ⚙️ Setup & Installation

### Prerequisites

**System Requirements:**
- OS: Windows, macOS, or Linux
- Python: 3.8 or higher
- RAM: Minimum 8GB (16GB recommended for smooth operation)
- Storage: 5GB for Ollama + models

**Software Requirements:**
- Ollama (downloaded from https://ollama.ai)
- Git (for cloning repository)
- pip (Python package manager)

**Accounts Required:**
- LangSmith account (free tier available at https://smith.langchain.com)

### Installation Steps

#### Step 1: Clone the Repository
```bash
git clone https://github.com/pratikdesai189/ollama_langsmith.git
cd ollama_langsmith
```

**What this does:**
- Downloads project files to your local machine
- Creates `ollama_langsmith` directory
- Changes into project directory

#### Step 2: Create a Virtual Environment

**On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Why virtual environment?**
- Isolates project dependencies
- Prevents conflicts with other Python projects
- Ensures reproducibility

#### Step 3: Upgrade pip and Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected packages to install:**
- langchain
- langchain-ollama
- streamlit
- python-dotenv
- Additional dependencies as per requirements.txt

#### Step 4: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# On macOS/Linux
touch .env

# On Windows
type nul > .env
```

Add the following content to `.env`:

```env
# LangSmith Configuration
LANGCHAIN_API_KEY=your_api_key_from_langsmith_here
LANGCHAIN_PROJECT=My_Ollama_Project
LANGCHAIN_TRACING_V2=true

# Ollama Configuration (optional)
OLLAMA_HOST=http://localhost:11434
```

**To get your LANGCHAIN_API_KEY:**
1. Visit https://smith.langchain.com
2. Sign up or log in
3. Go to Settings/API Keys
4. Create new API key
5. Copy and paste into `.env`

#### Step 5: Download and Run Ollama

**Install Ollama:**
1. Visit https://ollama.ai
2. Download for your operating system
3. Install following on-screen instructions

**Pull the Gemma Model:**

In a terminal/command prompt:
```bash
ollama pull gemma:2b
```

**Verify installation:**
```bash
ollama list
```

You should see output like:
```
NAME          	ID              	SIZE   	MODIFIED
gemma:2b      	ce4f60297665	   	5.2GB  	2 seconds ago
```

**Run Ollama service (keep terminal open):**
```bash
ollama serve
```

Expected output:
```
time=2024-03-22T10:30:45.123Z level=INFO msg="Listening on 127.0.0.1:11434"
```

#### Step 6: Run the Streamlit Application

**In a new terminal (with venv activated):**

```bash
streamlit run app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
  Network URL: http://192.168.1.x:8501
```

**Verify everything works:**
1. Open browser to http://localhost:8501
2. See "Ollama + LangSmith" title
3. Type a test question
4. Receive response

### Installation Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'streamlit'` | Run `pip install -r requirements.txt` |
| `Connection refused` when running app | Ensure Ollama is running with `ollama serve` |
| `Model not found` error | Run `ollama pull gemma:2b` |
| Port 8501 already in use | Use `streamlit run app.py --server.port 8502` |

## 📊 LangSmith Monitoring & Debugging

### Accessing LangSmith Dashboard

**Step 1: Start Your Application**
```bash
# Terminal 1: Ollama
ollama serve

# Terminal 2: Streamlit
streamlit run app.py
```

**Step 2: Make Requests**
- Open http://localhost:8501
- Ask several questions to generate traces

**Step 3: View Traces**
1. Go to https://smith.langchain.com
2. Click on your project name
3. You'll see all traces recorded

### Understanding Trace Information

Each trace shows:

```
┌─────────────────────────────────────────┐
│ TRACE DETAILS                           │
├─────────────────────────────────────────┤
│ Input: "What is Python?"                │
│ Output: "Python is a programming..."    │
│ Duration: 2.34 seconds                  │
│ Tokens: 45 input, 120 output            │
│ Model: gemma:2b                         │
│ Status: Success ✓                       │
└─────────────────────────────────────────┘
```

### Monitoring Metrics

**Available in LangSmith Dashboard:**
- **Latency**: Time taken for response
- **Token Count**: Input and output tokens used
- **Error Tracking**: Failed requests with details
- **Usage Analytics**: Total requests over time
- **Performance Graphs**: Visual latency trends

### Debug Features

```python
# View detailed logs
streamlit run app.py --logger.level=debug

# Enable verbose LangSmith logging
export LANGSMITH_DEBUG=true
streamlit run app.py
```

## 🔧 Configuration & Customization

### Model Selection

**Current Setup:**
```python
llm = OllamaLLM(model="gemma:2b")
```

**Available Models:**

| Model | Size | Speed | Memory | Quality |
|-------|------|-------|--------|---------|
| gemma:2b | 2B | Fast | 4GB | Good |
| mistral | 7B | Slower | 8GB | Better |
| neural-chat | 7B | Medium | 8GB | Good |
| orca-mini | 3B | Fast | 4GB | Fair |
| phi | 2.7B | Fast | 4GB | Fair |

**To Change Model:**

1. **Pull new model:**
```bash
ollama pull mistral
```

2. **Update app.py line 26:**
```python
llm = OllamaLLM(model="mistral")
```

3. **Restart application**

### System Prompt Customization

**Current Prompt (Line 19):**
```python
("system", "You are a helpful assistant Please respond to the questions asked.")
```

**Customization Examples:**

**Example 1: Code Assistant**
```python
("system", "You are an expert Python programmer. Provide concise, well-documented code examples.")
```

**Example 2: Creative Writer**
```python
("system", "You are a creative storyteller. Write engaging, imaginative responses with rich details.")
```

**Example 3: Technical Educator**
```python
("system", "You are a technical educator. Explain complex concepts simply with real-world examples.")
```

### Temperature & Other Parameters

**Add to app.py (after line 26):**
```python
llm = OllamaLLM(
    model="gemma:2b",
    temperature=0.7,      # 0.0-1.0: 0=deterministic, 1=creative
    top_p=0.9,           # Nucleus sampling parameter
    top_k=40,            # Top-k sampling parameter
    num_predict=256,     # Max tokens to generate
)
```

### UI Customization

**Change app title:**
```python
st.set_page_config(page_title="My AI Assistant", layout="wide")
st.title("🤖 My Custom Assistant")
```

**Add sidebar:**
```python
with st.sidebar:
    st.write("### Settings")
    model = st.selectbox("Choose Model", ["gemma:2b", "mistral"])
```

**Style input:**
```python
st.markdown("### 🎯 Ask Me Anything")
input_text = st.text_area("Your question:", height=100)
```

## 📦 Project Structure & Files

```
ollama_langsmith/
│
├── app.py                          # Main Streamlit application
│   ├── Imports
│   ├── Environment setup
│   ├── LangSmith configuration
│   ├── Prompt template
│   ├── UI components
│   └── Chain execution
│
├── requirements.txt                # Python dependencies
│   ├── langchain==0.x.x
│   ├── langchain-ollama==0.x.x
│   ├── streamlit==1.x.x
│   ├── python-dotenv==0.x.x
│   └── Other packages
│
├── .env                            # Environment variables (create manually)
│   ├── LANGCHAIN_API_KEY
│   ├── LANGCHAIN_PROJECT
│   └── Other configs
│
├── .env.example                    # Template for .env (optional)
│
├── .gitignore                      # Git ignore rules
│   ├── .env (sensitive!)
│   ├── __pycache__
│   ├── venv/
│   └── .DS_Store
│
├── README.md                       # This documentation file
│
└── venv/                           # Virtual environment (auto-created)
    ├── bin/ (macOS/Linux)
    ├── Scripts/ (Windows)
    ├── lib/
    └── pyvenv.cfg
```

## 🐛 Troubleshooting Guide

### Problem: "Connection refused" Error

**Error Message:**
```
ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
```

**Solutions:**
1. **Check if Ollama is running:**
```bash
# Terminal 1
ollama serve
```

2. **Verify Ollama port:**
```bash
# Check if port 11434 is listening
netstat -an | grep 11434  # macOS/Linux
netstat -ano | findstr :11434  # Windows
```

3. **Restart Ollama:**
```bash
# Kill existing process and restart
ollama serve
```

### Problem: "Model not found" Error

**Error Message:**
```
ollama: Error: model 'gemma:2b' not found, try pulling it first
```

**Solutions:**
```bash
# List available models
ollama list

# Pull the required model
ollama pull gemma:2b

# Try alternative model
ollama pull mistral
```

### Problem: LangSmith Traces Not Showing

**Debugging Steps:**

1. **Verify API key:**
```python
import os
from dotenv import load_dotenv
load_dotenv()
print(os.getenv("LANGCHAIN_API_KEY"))  # Should print key, not None
```

2. **Check environment variables in app:**
```python
# Add to app.py temporarily
import os
print(f"API Key: {os.getenv('LANGCHAIN_API_KEY')}")
print(f"Project: {os.getenv('LANGCHAIN_PROJECT')}")
print(f"Tracing: {os.getenv('LANGCHAIN_TRACING_V2')}")
```

3. **Verify internet connection:**
```bash
# Test connectivity to LangSmith
curl https://api.smith.langchain.com/health
```

4. **Check .env file format:**
```
✓ Correct: LANGCHAIN_API_KEY=sk_...
✗ Wrong: LANGCHAIN_API_KEY = sk_...  (spaces!)
✗ Wrong: export LANGCHAIN_API_KEY=sk_...  (use in terminal, not .env)
```

### Problem: Slow Responses

**Performance Issues:**

| Issue | Cause | Solution |
|-------|-------|----------|
| First response takes 30s | Model loading | Normal, happens once per session |
| All responses slow | Large model | Try smaller model (gemma:2b) |
| CPU at 100% | Hardware limitation | Reduce token limit or batch size |
| High memory usage | Model too large | Switch to smaller model |

**Optimization Tips:**
```python
# Reduce token generation
llm = OllamaLLM(
    model="gemma:2b",
    num_predict=128  # Generate fewer tokens
)

# Use quantized model
ollama pull gemma:2b-q4  # 4-bit quantized version
```

### Problem: Port 8501 Already in Use

**Error Message:**
```
Error: Address already in use. Port 8501 is already running
```

**Solutions:**

1. **Use different port:**
```bash
streamlit run app.py --server.port 8502
```

2. **Kill process using port 8501:**
```bash
# macOS/Linux
lsof -ti:8501 | xargs kill -9

# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

3. **Check what's running:**
```bash
# macOS/Linux
ps aux | grep streamlit

# Windows
tasklist | findstr streamlit
```

### Problem: "ModuleNotFoundError"

**Error Message:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solutions:**

1. **Activate virtual environment:**
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

2. **Install requirements:**
```bash
pip install -r requirements.txt
```

3. **Verify installation:**
```bash
pip list | grep streamlit
python -c "import streamlit; print(streamlit.__version__)"
```

### Problem: Ollama Model Download Fails

**Error Message:**
```
Error: Failed to download model
```

**Solutions:**

1. **Check storage space:**
```bash
# Show disk usage
df -h  # macOS/Linux
dir C:\  # Windows

# Need at least 5GB free
```

2. **Download with retry:**
```bash
ollama pull gemma:2b
# If fails, try again
ollama pull gemma:2b
```

3. **Use smaller model:**
```bash
ollama pull phi  # Only 2.7B
ollama pull orca-mini  # Only 3B
```

## 📚 Resources & Documentation

### Official Documentation

| Resource | URL | Purpose |
|----------|-----|---------|
| LangChain | https://python.langchain.com | Core library docs |
| Ollama | https://ollama.ai | Model management |
| Streamlit | https://docs.streamlit.io | UI framework |
| LangSmith | https://docs.smith.langchain.com | Monitoring & debugging |

### Model Collections

- **Ollama Models**: https://ollama.ai/library
- **Hugging Face**: https://huggingface.co/models
- **Model Benchmarks**: https://huggingface.co/spaces/lmsys/chatbot-arena

### Learning Resources

- **LangChain Quickstart**: https://python.langchain.com/docs/get_started
- **Streamlit Tutorial**: https://docs.streamlit.io/library/get-started
- **Ollama Getting Started**: https://github.com/ollama/ollama#quickstart

### Community & Support

- **LangChain Discord**: https://discord.gg/langchain
- **Ollama GitHub**: https://github.com/ollama/ollama
- **Streamlit Forum**: https://discuss.streamlit.io

## 🤝 Contributing

### How to Contribute

We welcome contributions! Here's how:

1. **Fork the repository**
```bash
# Click "Fork" on GitHub
```

2. **Create a feature branch**
```bash
git checkout -b feature/amazing-feature
```

3. **Make your changes**
```bash
# Edit files
# Test your changes
```

4. **Commit changes**
```bash
git commit -m "Add amazing feature"
```

5. **Push to branch**
```bash
git push origin feature/amazing-feature
```

6. **Open Pull Request**
```bash
# On GitHub, click "New Pull Request"
```

### Contribution Ideas

- **New Models**: Test with different Ollama models
- **UI Enhancements**: Improve Streamlit interface
- **Features**: Add conversation history, export functionality
- **Documentation**: Improve guides and examples
- **Bug Fixes**: Report and fix issues

### Reporting Issues

When reporting bugs, include:
- Error message (full traceback)
- Steps to reproduce
- Your environment (OS, Python version)
- Expected vs actual behavior

Example:
```
Title: LangSmith traces not appearing

Environment:
- OS: macOS 12.6
- Python: 3.10.5
- Streamlit: 1.28.0

Steps to reproduce:
1. Start Ollama
2. Run streamlit run app.py
3. Ask a question

Error:
[Full traceback here]

Expected: Traces appear in LangSmith dashboard
Actual: Dashboard shows no traces
```

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

For full license text, see LICENSE file in repository.

## 📞 Support & Contact

### Getting Help

**For Issues:**
1. Check troubleshooting section above
2. Search existing GitHub issues
3. Create new issue with details

**For Questions:**
- GitHub Discussions
- Project Issues with "question" label

**For Security Issues:**
- Do NOT open public issue
- Email maintainer directly
- Include detailed reproduction steps

### Links

| Item | Link |
|------|------|
| GitHub Repo | https://github.com/pratikdesai189/ollama_langsmith |
| Issues | https://github.com/pratikdesai189/ollama_langsmith/issues |
| Discussions | https://github.com/pratikdesai189/ollama_langsmith/discussions |
| Author | @pratikdesai189 |

## 🎓 Learning Paths

### Beginner Path
1. Install and run basic setup
2. Ask questions and get responses
3. Explore LangSmith dashboard
4. Read documentation

### Intermediate Path
1. Customize system prompt
2. Try different models
3. Adjust model parameters
4. Monitor performance metrics

### Advanced Path
1. Add conversation history
2. Implement custom chains
3. Build multi-model workflows
4. Deploy to production

## 🔮 Future Enhancements

Planned features:
- ✨ Conversation memory/history
- 📊 Advanced analytics dashboard
- 🔌 API endpoint for external access
- 💾 Session save/load functionality
- 🎨 Dark/Light theme support
- 📱 Mobile responsiveness
- 🔐 User authentication
- ⚡ Streaming response support

## 📋 Changelog

### Version 1.0.0 (Initial Release)
- Basic Streamlit UI
- Ollama integration
- LangChain pipeline
- LangSmith monitoring
- Local model inference

---

**Last Updated**: March 22, 2026  
**Maintained by**: @pratikdesai189  
**License**: MIT  

**Happy coding! 🚀**
