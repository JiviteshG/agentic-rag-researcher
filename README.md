# Agentic RAG Research Assistant 🤖🔬

An autonomous intelligence pipeline designed to ingest, index, and query academic literature from Arxiv. This project leverages **Agentic Orchestration** to transform raw research papers into a queryable knowledge base using **Weaviate Cloud** and **OpenAI**.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Vector Store: Weaviate](https://img.shields.io/badge/VectorStore-Weaviate-green.svg)](https://weaviate.io/)
[![Package Manager: uv](https://img.shields.io/badge/manager-uv-purple.svg)](https://github.com/astral-sh/uv)

---

## 🚀 Key Features

* **Autonomous Ingestion:** Automated Arxiv scraping and metadata extraction.
* **Agentic Orchestration:** Modular pipeline design for chunking, embedding, and indexing.
* **Hybrid Search Ready:** Integrated with Weaviate for high-performance vector retrieval.
* **Modern DevStack:** Managed via `uv` for lightning-fast dependency resolution and reproducible environments.
* **Scalable Architecture:** Designed with clear separation between `ingestion`, `rag`, and `ui` layers.
---
## 🏗️ System Architecture

The project follows a modular RAG (Retrieval-Augmented Generation) design:

1.  **Ingestion Layer:** Connects to the Arxiv API to fetch domain-specific research papers.
2.  **Processing Layer:** Implements intelligent document chunking and OpenAI embedding generation.
3.  **Vector Store:** Stores high-dimensional embeddings in **Weaviate Cloud** with full schema management.
4.  **Orchestration:** (Future) Multi-agent workflows for cross-paper synthesis and reasoning.
---
## 🛠️ Installation & Setup

This project uses `uv` for dependency management.

### 1. Clone the Repository
  ```bash
  git clone [https://github.com/JiviteshG/agentic-rag-researcher.git](https://github.com/JiviteshG/agentic-rag-researcher.git)
  cd agentic-rag-researcher
  ```
### 2. Environment Setup
  ```bash
  # Install dependencies and create venv
  uv sync
  ```
### 3. Configure Environment Variables
Create a .env file in the root directory:
OPENAI_API_KEY=your_openai_api_key
WEAVIATE_URL=your_weaviate_cluster_url
WEAVIATE_API_KEY=your_weaviate_api_key

### Section 5: Usage

### Indexing Documents
To ingest data from Arxiv and index it into Weaviate:
  ```bash
  uv run python -m app.ingestion.index_weaviate
  ```
Verifying Connection
  Bash```
  uv run python -m app.ingestion.VERIFY_WEAVIATE
  ```

### Section 6: Project Structure
```markdown
## 📁 Project Structure

```text
├── app/
│   ├── ingestion/         # Data scraping and Weaviate indexing logic
│   ├── rag/               # Retrieval and generation orchestration
│   ├── ui/                # Frontend interface (Streamlit)
│   └── config.py          # Centralized configuration management
├── data/                  # Local storage for raw research artifacts
├── pyproject.toml         # Project metadata and dependencies
└── uv.lock                # Deterministic lockfile
```

### Section 7: Future Roadmap & Contact
  ```markdown
  ## 🗺️ Roadmap
  - [ ] Implement multi-agent reasoning for comparative paper analysis.
  - [ ] Add support for local LLMs via Ollama.
  - [ ] Expand ingestion to include PubMed and OpenAlex.
  ```

**Maintained by:** [Jivitesh Gudekar](https://github.com/JiviteshG)
*Data Scientist*
[![Managed by uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
