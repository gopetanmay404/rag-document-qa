#  Production Agentic RAG System

> A self-correcting, hybrid-retrieval, document Q&A chatbot built with LangGraph, FAISS, BM25, and Groq LLM.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?logo=streamlit)
![LangGraph](https://img.shields.io/badge/LangGraph-0.1+-green)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📌 What Is This?

This is a **production-grade Agentic RAG (Retrieval-Augmented Generation)** application.

## Live Demo

 Try the RAG Document App — Live!
<a href="https://rag-document-app-tannu.streamlit.app/">
  <img src="https://img.shields.io/badge/RAG%20DOCUMENT%20APP-LIVE%20DEMO-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white&labelColor=000000" height="50" alt="RAG Document App Live Demo" />
</a>

</div>

You upload PDF documents. You ask questions. The system answers using **only** the content from your documents — with citations, confidence scores, and source tracing.

What makes it **agentic**: if the first retrieval attempt fails to find relevant content, the system **automatically rewrites your query** and retries — without you doing anything.

---

## 🎯 Key Features at a Glance

| Feature | Description |
|---|---|
| 🔀 **Hybrid Retrieval** | BM25 (keywords) + FAISS (semantics) merged for best coverage |
| 🧠 **Agentic Pipeline** | LangGraph state machine self-corrects on bad retrieval |
| ⚡ **Batch Grading** | Grades all docs in 1 LLM call instead of N (5× faster) |
| 🧾 **Progressive Memory** | Never loses long conversation history — compresses cumulatively |
| 📊 **Live Evaluation** | Self-evaluates every answer (no external APIs needed) |
| ⭐ **Optional Reranker** | CrossEncoder reranks 15 candidates → keeps top 5 |
| 📁 **Persistent Indexes** | FAISS + BM25 survive restarts — no re-embedding on reload |
| 🔍 **Confidence Scores** | Retrieval confidence + grounding score per answer |
| 📎 **Source Tracing** | Every answer cites source filename, page number, and section |
| 🔧 **Debug Tab** | Per-query analytics: latency, method, rewrites, grade |
| 📝 **Structured Logging** | All pipeline events logged via Python `logging` module |

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│                   LangGraph State Machine                │
│                                                         │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐  │
│  │ RETRIEVE │───▶│  GRADE   │───▶│    GENERATE      │  │
│  │          │    │(1 LLM    │    │ (Groq LLM)       │  │
│  │ BM25 +   │    │  call)   │    │ + Confidence     │  │
│  │ FAISS    │◀───│          │    │   Scoring        │  │
│  └──────────┘    └──────────┘    └──────────────────┘  │
│       ▲               │ Not relevant?                   │
│       │          ┌────▼─────┐                           │
│       └──────────│  REWRITE │  (semantic guard)         │
│                  │  QUERY   │                           │
│                  └──────────┘                           │
└─────────────────────────────────────────────────────────┘
    │
    ▼
Answer + Sources + Confidence + Section Citations
```

### Pipeline Flow

1. **User asks a question** → adaptive k is computed based on query complexity
2. **RETRIEVE node** → runs hybrid BM25+FAISS search; optionally reranks with CrossEncoder
3. **GRADE node** → 1 batch LLM call grades all retrieved docs at once
4. **Decision:**
   - If `relevant` → go to **GENERATE**
   - If `not_relevant` and attempts < 2 → go to **REWRITE** → retry from RETRIEVE
   - If attempts exhausted → generate with what's available
5. **GENERATE node** → builds context, calls Groq, computes confidence scores
6. **Answer returned** with: citations, confidence %, retrieval method badge

---

## 🛠️ Full Technology Stack

### Core Frameworks

| Library | Version | Role |
|---|---|---|
| `langgraph` | ≥ 0.1.0 | Agentic state machine orchestration |
| `langchain-core` | ≥ 0.2.0 | Document, prompt, chain abstractions |
| `langchain-groq` | ≥ 0.1.6 | Groq LLM API integration |
| `langchain-huggingface` | ≥ 0.0.3 | HuggingFace embedding models |
| `langchain-community` | ≥ 0.2.0 | FAISS vector store wrapper |
| `streamlit` | ≥ 1.35.0 | Web UI (chat, evaluation, debug tabs) |

### Retrieval

| Library | Version | Role |
|---|---|---|
| `faiss-cpu` | ≥ 1.7.4 | Dense vector similarity search |
| `rank-bm25` | ≥ 0.2.2 | Sparse keyword retrieval (BM25Okapi) |
| `sentence-transformers` | ≥ 2.7.0 | Embedding models + CrossEncoder reranker |
| `torch` | ≥ 2.0.0 | Backend for sentence-transformers |

### Document Processing

| Library | Version | Role |
|---|---|---|
| `pymupdf` (fitz) | ≥ 1.24.0 | Fast PDF text extraction, page-by-page |
| `langchain-text-splitters` | ≥ 0.2.0 | RecursiveCharacterTextSplitter |

### Utilities

| Library | Role |
|---|---|
| `python-dotenv` | Load `GROQ_API_KEY` from `.env` |
| `typing_extensions` | `TypedDict` for LangGraph state |
| `pickle` (stdlib) | BM25 index persistence |
| `logging` (stdlib) | Structured event logging |

### Models Used

| Model | Provider | Purpose |
|---|---|---|
| `llama-3.1-8b-instant` | Groq | Fast inference (default) |
| `llama-3.3-70b-versatile` | Groq | Higher quality (optional) |
| `BAAI/bge-base-en-v1.5` | HuggingFace | Dense embeddings (recommended) |
| `all-MiniLM-L6-v2` | HuggingFace | Fastest embeddings |
| `all-mpnet-base-v2` | HuggingFace | Highest quality embeddings |
| `BAAI/bge-reranker-base` | HuggingFace | CrossEncoder reranker (optional) |

---

## 📁 Project Structure

```
check_it/
│
├── app.py                        # Main application (all logic + UI)
├── rag_evaluation_framework.py   # Standalone evaluation module
├── requirements.txt              # Python dependencies
├── report.tex                    # LaTeX project report
├── README.md                     # This file
├── .env                          # API keys (create this yourself)
│
└── faiss_index/                  # Auto-created on first upload
    ├── index.faiss               # FAISS vector index
    ├── index.pkl                 # FAISS metadata
    ├── embedding_model.txt       # Tracks which embedding model built the index
    └── bm25.pkl                  # BM25 sparse index + corpus
```

---

## 🚀 Setup & Installation

### Step 1 — Clone / Copy Files

Make sure you have both files in your project folder:
- `app.py`
- `rag_evaluation_framework.py`

### Step 2 — Create Virtual Environment

```bash
# In VS Code terminal (or any terminal)
python -m venv myenv

# Activate it
# Windows:
myenv\Scripts\activate
# Mac/Linux:
source myenv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install streamlit pymupdf python-dotenv
pip install langchain-core langchain-community langchain-text-splitters
pip install langchain-groq langchain-huggingface
pip install langgraph faiss-cpu rank-bm25
pip install sentence-transformers torch typing_extensions
```

### Step 4 — Get Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (free tier available)
3. Create an API key

### Step 5 — Create `.env` File

```
GROQ_API_KEY=your_groq_api_key_here
```

### Step 6 — Run the App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 💡 How to Use

### 1. Upload PDFs
- Click **"Upload PDF"** in the Chat tab
- Multiple PDFs supported
- System extracts text, chunks it, embeds it, builds FAISS + BM25 indexes
- Indexes are **saved to disk** — reload the app and they persist

### 2. Ask Questions
- Type any question in the chat input
- System runs the LangGraph pipeline automatically
- Each answer shows:
  - 📎 Source filename + page + section
  - 🟢 Relevance grade
  - 🔀 Retrieval method (hybrid / faiss-only / hybrid+reranked)
  - ⏱️ Response time
  - 📊 Retrieval confidence %
  - 📌 Grounding confidence %

### 3. Check the Tabs

| Tab | What You'll Find |
|---|---|
| 💬 Chat | Main Q&A interface |
| 📚 Documents | Chunk stats + ingestion timing per file |
| 📜 History | Full conversation history |
| 📊 Evaluation | Live RAG quality metrics (run from here) |
| 🔧 Debug | Per-query analytics, method distribution, system info |

### 4. Sidebar Controls

| Control | Default | Effect |
|---|---|---|
| LLM Model | 8b-instant | Switch to 70b for harder questions |
| Embedding Model | BGE Base | Change embedding strategy |
| Chunk Size | 1000 | Larger = more context per chunk |
| Overlap % | 20% | Prevents cutting sentences at boundaries |
| Chunks to Retrieve | 6 | How many chunks to retrieve per query |
| BM25 Weight | 0.30 | 0 = pure FAISS, 1 = pure BM25 |
| Reranker Toggle | Off | Enable CrossEncoder (adds ~0.5–1s latency) |
| Memory Window | 5 | Last N exchanges kept in sliding window |

---

## 📊 Evaluation Dashboard

The **Evaluation tab** runs automatic quality checks on recent conversations:

### Metrics Explained

| Metric | Scale | What it means |
|---|---|---|
| **Retrieval Quality** | 0–10 | Are retrieved chunks relevant to the question? |
| **Context Coverage** | 0–10 | Does context fully cover what's needed to answer? |
| **Source Grounding** | 0–10 | Is the answer grounded in retrieved sources? |
| **Hallucination Risk** | 0–10 | Does the answer add facts not in the documents? |
| **Keyword Faithfulness** | 0–100 | Non-LLM lexical overlap between answer and context |
| **Faithfulness Score** | 0–100 | Blended: 60% LLM + 40% keyword overlap |
| **Overall Health** | 0–100 | Weighted average of all dimensions |

### Health Score Formula
```
Health = (Retrieval×0.25 + Coverage×0.25 + Faithfulness×0.30 + (10-Hallucination)×0.20) × 10
```

### Why Blended Faithfulness?
Pure LLM self-scoring is biased — the LLM tends to think its own answers are well-grounded.
Adding keyword overlap (40% weight) provides an independent, bias-free check.

---

## 🔍 Retrieval System Deep Dive

### Hybrid BM25 + FAISS

```
Query
  │
  ├─── FAISS (Dense)  ──▶  Semantic similarity (embeddings)
  │         k_faiss = k × (1 - BM25_weight)
  │
  └─── BM25 (Sparse)  ──▶  Keyword / exact-match
            k_bm25  = k × BM25_weight

              │
              ▼
         Merge + Deduplicate
              │
              ▼
     [Optional] CrossEncoder Rerank
     (retrieve 15 → score → keep top 5)
              │
              ▼
         Final k chunks
```

**When to prefer BM25 weight = 0.5+:**
- Documents with many IDs, codes, version numbers
- Technical specifications
- Named entities (person names, product names)

**When to prefer BM25 weight = 0.1:**
- Conceptual / explanatory questions
- Summarization tasks
- Paraphrase-heavy documents

### Header-Aware Chunking

Chunks are annotated with detected section headers:

```python
# Detects:
## Introduction          ← Markdown headings
CHAPTER OVERVIEW         ← ALL CAPS headings  
3.1 Routing Architecture ← Numbered sections
Chapter 4               ← Chapter markers
```

Each chunk carries `{source, page, section}` metadata for richer citations.

---

## 💾 Memory System

### Dual Memory Architecture

```
Current session
      │
      ├── Sliding Window Buffer (last N exchanges)
      │   └─ Verbatim recent Q&A pairs
      │
      └── Progressive Summary
          └─ LLM compresses: old_summary + new_exchanges → new_summary
```

### Progressive vs Window-Only

| Approach | What gets lost |
|---|---|
| Window-only (old) | Everything before the last N exchanges |
| Progressive (current) | Nothing — history is compressed, not dropped |

---

## 📝 Logs

All events are logged to your terminal (where you ran `streamlit run`):

```
2026-06-13 11:32:01 | INFO | rag_app | PDF extracted | file=doc.pdf pages_ok=12 pages_failed=0
2026-06-13 11:32:05 | INFO | rag_app | upload | files=1 faiss_save=0.43s bm25_build=0.12s
2026-06-13 11:32:10 | INFO | rag_app | retrieval | query='what is...' attempt=1 method=hybrid docs=6
2026-06-13 11:32:11 | INFO | rag_app | grading | query='what is...' result=relevant
2026-06-13 11:32:13 | INFO | rag_app | generation | grounding=0.78
```

**Save logs to file:**
```bash
streamlit run app.py 2>&1 | tee rag_logs.txt
```

---

## ⚠️ Troubleshooting

| Problem | Solution |
|---|---|
| `GROQ_API_KEY not found` | Create `.env` file with your key |
| `ModuleNotFoundError: rank_bm25` | Run `pip install rank-bm25` |
| Embedding model mismatch warning | Click "Clear Docs" and re-upload PDFs |
| Reranker download slow | First use downloads model (~500MB) — wait once |
| PDF shows 0 chunks | PDF is scanned image — no text layer. Use OCR first |
| App crashes on startup | Check Python version ≥ 3.10 |
| BM25 not loaded on restart | Upload a PDF first to rebuild indexes |

---

## 🧪 Interview Talking Points

If asked to explain this project in an interview:

1. **"It's an Agentic RAG system"** — not just retrieve-then-generate. The LangGraph pipeline self-corrects when retrieval fails.

2. **"Hybrid retrieval"** — combining FAISS (semantic) and BM25 (lexical) gives better coverage than either alone. FAISS finds meaning, BM25 finds exact terms.

3. **"Batch grading"** — instead of calling the LLM N times (once per document), I send one prompt with all documents and parse a JSON array. 5× faster for 6 documents.

4. **"Progressive summarization"** — the memory never forgets. It compresses `old_summary + new_exchanges → new_summary` cumulatively. This is better than a sliding window.

5. **"Self-contained evaluation"** — no RAGAS, no external APIs. The evaluation framework uses the same Groq LLM + a keyword overlap bias correction.

6. **"Observability"** — structured Python logging, per-query analytics tab, ingestion timing per file. Production systems need to be debuggable.

---

## 📐 System Requirements

| Requirement | Minimum |
|---|---|
| Python | 3.10+ |
| RAM | 4 GB (8 GB recommended for 70B model) |
| Disk | 2 GB (for embedding models cache) |
| Internet | Required (Groq API + first-time model download) |
| GPU | Not required (CPU mode works fine) |

---


## 📜 License

MIT License — free to use, modify, and distribute.

---

<div align="center">

**Built with:** LangGraph • FAISS • BM25 • Groq LLM • HuggingFace • Streamlit

*Production Agentic RAG System — 2026*

</div>
