# rag-chatbot-using-llm-chromadb
A Retrieval-Augmented Generation (RAG) chatbot that uses HuggingFace embeddings, ChromaDB for vector search, and LLMs (via Together AI) to assist with hackathon ideas and dataset exploration.

# Basic RAG Chatbot for Hackathon Ideas & Datasets

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

---
