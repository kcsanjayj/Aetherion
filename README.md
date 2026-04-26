# 🚀 Aetherion — Agentic Multi-LLM RAG System

A production-style agentic RAG system that improves LLM outputs using retrieval + evaluation + controlled retry loops

🧠 **What is this?**

Aetherion is a self-correcting RAG pipeline where every answer is:

**Generate → Evaluate → Refine → Finalize**

Instead of trusting a single LLM response, the system acts like an exam system with a built-in examiner (critic agent).

---

## ⚙️ Core Pipeline

### 🧩 Architecture
```
backend/agents/
├── planner_agent      → understands query intent
├── reasoning_agent    → generates response
├── critic_agent       → evaluates quality
├── retry_agent        → triggers refinement loop
└── orchestrator       → controls full pipeline
```

---

## ✨ Key Features

- 🧠 **Evaluation-driven generation** — Every response is scored before being returned
- 🔁 **Self-correction loop** — Automatically retries low-quality outputs (bounded iterations)
- 🔌 **Multi-LLM routing** — OpenAI / Anthropic / Groq / HuggingFace fallback support
- 📊 **Execution trace** — Full visibility into retrieval → generation → evaluation steps
- ⚡ **Async FastAPI backend** — Handles concurrent requests efficiently

---

## 📊 Results (Controlled Eval)

| Metric | Improvement |
|--------|-------------|
| **Relevance** | +21% vs baseline RAG |
| **Hallucinations** | ~25% reduction |
| **Avg latency** | ~1.2s (with evaluation loop) |
| **Retry depth** | max 3 iterations |

Evaluation done on 50 QA pairs (research-paper dataset) using structured GPT-based rubric.

---

## ⚖️ Design Tradeoffs

| Tradeoff | Choice |
|----------|--------|
| ⏱️ **Higher latency** | due to evaluation + retry loop |
| 🎯 **Higher accuracy** | critic filters weak responses before final output |
| 💰 **Higher cost** | multiple LLM calls per query |
| 🧩 **Better reliability** | fallback routing + failure recovery |

---

## 🛡️ Production Features

- Rate limiting middleware
- Structured JSON logging
- Timeout handling + graceful fallback
- Multi-provider resilience layer
- Health check endpoint

---

## 🧪 Failure Handling

| Failure Mode | Response |
|--------------|----------|
| LLM timeout | → fallback provider |
| Low-quality output | → retry loop |
| Retrieval noise | → filtered context selection |
| Persistent failure | → safe degraded response |

---

## 🧠 Why this matters

This project demonstrates:

- **Agentic orchestration** (planner + critic + retry loop)
- **Evaluation-as-a-stage** (not post-processing)
- **Real-world tradeoffs** (latency vs quality)
- **Production-ready FastAPI architecture**
- **Multi-LLM routing systems**

---

## 🧪 Tech Stack

FastAPI · ChromaDB · OpenAI / Anthropic / Groq · sentence-transformers · Tailwind · Vercel · Railway · Docker

---

## 🚀 Summary

Aetherion turns a standard RAG pipeline into a **self-evaluating AI system** that improves its own answers before responding.
