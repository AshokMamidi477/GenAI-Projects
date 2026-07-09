# 🤖 GenAI Projects Portfolio

![GenAI](https://img.shields.io/badge/Generative%20AI-Projects-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow)
![LLM](https://img.shields.io/badge/LLM-Applications-green)
![RAG](https://img.shields.io/badge/RAG-Systems-orange)
![AI Agents](https://img.shields.io/badge/AI-Agents-purple)

A collection of hands-on **Generative AI applications** built using Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), AI agents, APIs, and modern AI engineering practices.

These projects demonstrate practical implementations of GenAI concepts including prompt engineering, async LLM calls, document intelligence, knowledge retrieval, and AI-powered automation.

---

# 🚀 Projects

## 01. 🧠 RAG Assistant — Document Question Answering System

### Overview

A Retrieval-Augmented Generation (RAG) application that allows users to upload documents and ask questions using natural language.

The system retrieves relevant information from documents and generates accurate answers using an LLM.

### Key Features

* Document ingestion pipeline
* Text chunking and embedding generation
* Vector database search
* Context-aware LLM responses
* Semantic document retrieval
* Reduced hallucination through grounding

### Tech Stack

* Python
* LangChain
* OpenAI / Gemini LLMs
* Vector Database
* Embeddings
* RAG Architecture

---

## 02. 📄 Invoice Data Extractor

### Overview

An AI-powered invoice processing application that extracts structured information from invoices using Generative AI.

The application converts unstructured invoice documents into structured JSON data.

### Key Features

* Invoice document analysis
* OCR + LLM extraction workflow
* Structured JSON output
* Field validation
* Automated data processing

### Tech Stack

* Python
* Generative AI APIs
* Document Processing
* JSON Extraction
* Streamlit

---

## 03. 🛍 Product Description Generator

### Overview

An AI-powered e-commerce content generation system that creates SEO-friendly product descriptions in multiple writing styles.

Users provide product details and the application generates multiple marketing variants.

### Key Features

* Generate multiple tones:

  * Professional
  * Playful
  * Urgency-driven
* Async parallel LLM requests
* SEO meta description generation
* Save generated content to Notion database

### Architecture

```mermaid
graph TD

A[Product Brief] --> B[Gradio UI]

B --> C[Prompt Engineering Layer]

C --> D[Gemini/OpenAI LLM]

D --> E[Multiple Tone Generation]

E --> F[SEO Validation]

F --> G[Notion Database]
```

### Tech Stack

* Python
* Google Gemini / OpenAI API
* AsyncOpenAI
* Gradio
* Notion API
* Prompt Engineering

---

## 04. 🏥 Medical Symptom Summarizer

### Overview

An AI assistant that summarizes user-provided symptoms into a structured medical summary.

The application helps organize information before consulting healthcare professionals.

### Key Features

* Symptom summarization
* Structured output generation
* Natural language processing
* AI-assisted information organization

### Tech Stack

* Python
* LLM APIs
* Prompt Engineering
* AI Workflows

---

# 🏗 GenAI Architecture Patterns Covered

## Prompt Engineering

* Role-based prompting
* Few-shot prompting
* Structured output prompting
* Persona-based generation

## Retrieval-Augmented Generation (RAG)

```text
Documents
    |
    ↓
Chunking
    |
    ↓
Embeddings
    |
    ↓
Vector Database
    |
    ↓
Retriever
    |
    ↓
LLM Response
```

## AI Agent Concepts

* Tool usage
* Multi-step reasoning workflows
* API integrations
* Autonomous task execution

---

# 🛠 Technologies Used

| Category      | Technologies                       |
| ------------- | ---------------------------------- |
| Languages     | Python                             |
| LLMs          | OpenAI GPT, Google Gemini          |
| Frameworks    | LangChain, Gradio                  |
| Vector Search | Embeddings, Vector Databases       |
| APIs          | OpenAI API, Gemini API, Notion API |
| Testing       | Pytest                             |
| Environment   | Python Virtual Environments        |

---

# 📂 Repository Structure

```
GenAI-Projects/

├── README.md

├── 01-RAG-Assistant/
│
├── 02-Invoice-Data-Extractor/
│
├── 03-Product-Description-Generator/
│
└── 04-Medical-Symptom-Summarizer/
```

---

# ⚙️ Running Projects Locally

Clone repository:

```bash
git clone <repository-url>

cd GenAI-Projects
```

Navigate into any project:

```bash
cd project-folder
```

Create virtual environment:

```bash
python -m venv venv

source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables:

```bash
cp .env.example .env
```

Run the application:

```bash
python app.py
```

---

# 🎯 Skills Demonstrated

✅ Generative AI Application Development
✅ LLM API Integration
✅ Prompt Engineering
✅ Retrieval-Augmented Generation (RAG)
✅ AI Workflow Automation
✅ Async API Processing
✅ Document Intelligence
✅ Vector Search Concepts
✅ AI Product Development

---

# 📈 Future Enhancements

* Deploy applications on cloud platforms
* Add LangGraph-based AI agents
* Add multimodal AI capabilities
* Add evaluation pipelines
* Add LLM observability and monitoring
* Add CI/CD pipelines

---

# 👨‍💻 About

Built as part of continuous learning and experimentation with modern Generative AI technologies.

Focused on building practical AI applications that solve real-world business problems.
