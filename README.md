# ai-agent-vs-agentic-ai
AI Agents vs Agentic AI: From Chatbots to Autonomous Systems

This project demonstrates the evolution of AI agents through three distinct implementations, showcasing the progression from basic conversational AI to true agentic behavior.

## Quick Start

### 1. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment
Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

### 4. Run Different AI Agent Types

**Basic AI Agent (Traditional Chat)**
```bash
python3 ai-agent.py
```

**AI Agent with Tools**
```bash
python3 ai-agent_tool_calling.py
```

**Agentic AI (LangChain)**
```bash
python3 ai-agent_Agentic.py
```
