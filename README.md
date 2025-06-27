
# Basic RAG Chatbot for Hackathon/Project Ideas & Datasets

This is a simple Retrieval-Augmented Generation (RAG) chatbot built using:

- **LangChain** for chaining components
- **ChromaDB** for semantic search
- **HuggingFace Embeddings** for vectorization
- **Together API (Mistral-7B)** for generating answers
- **GitHub API** to fetch relevant repositories
- **Streamlit** for a lightweight web UI

---

##  Features

- Chat-based interface via Streamlit
- Semantic search using ChromaDB + GTE-small embeddings
- LLM-based answer generation via Together AI (Mistral 7B)
- Searches project ideas and datasets stored in CSVs
- Intelligent GitHub repo search using keyword agent
- Everything is bundled into a simple, interactive [Streamlit](https://streamlit.io/) app.

---

---

## Tech Stack

| Purpose             | Tool/Library                        |
|---------------------|-------------------------------------|
| LLM                 | [Mistral-7B](https://www.together.ai/) via Together API |
| Embeddings          | `thenlper/gte-small` from HuggingFace |
| Vector Database     | [ChromaDB](https://www.trychroma.com/) |
| Backend Logic       | [LangChain](https://www.langchain.com/) |
| GitHub Integration  | Custom search using GitHub REST API |
| UI                  | [Streamlit](https://streamlit.io/)  |

---
