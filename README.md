
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

## Project Structure

├── app.py # Streamlit app

├── main_2.py # Core RAG logic (retrieval + generation)

├── github_search_agent.py# GitHub keyword-based search

├── ideas.csv # Project ideas

├── sih.csv # Additional ideas (optional)

├── setup.py # embed your project ideas into ChromaDB

├── README.md # You are here!

---

---

## Core Logic

The chatbot follows a simple **RAG (Retrieval-Augmented Generation)** pattern using HuggingFace embeddings, ChromaDB, and an LLM. Here's how it works:

### 1. Embedding and Retrieval

User queries are embedded using `thenlper/gte-small`, and documents are retrieved from two ChromaDB collections:
- `ideas_db`: project ideas from `ideas.csv`
- `datasets_db`: datasets from `datasets.csv`

```python
embedding = HuggingFaceEmbeddings(model_name="thenlper/gte-small")
ideas_db = Chroma(persist_directory="embeddings/ideas", embedding_function=embedding)
datasets_db = Chroma(persist_directory="embeddings/resources", embedding_function=embedding)

docs = db.similarity_search(query, k=3)
```


### 2. LLM Response Generation
Using the retrieved docs, a prompt is crafted and passed to Together API (Mistral-7B-Instruct) to generate a contextual response.

```
prompt = f"""
You are a helpful assistant for hackathons and dataset projects.

Context:
{context}

Question:
{query}

Answer:
"""

response = client.chat.completions.create(
    model="mistralai/Mistral-7B-Instruct-v0.1",
    messages=[
        {"role": "system", "content": "You are a helpful assistant for hackathons and dataset projects."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=500,
    temperature=0.7
)
```

### 3. GitHub Repository Search
Parallel to the LLM call, a lightweight GitHubSearchAgent extracts keywords from the query and fetches top repositories using GitHub's REST API.
```
url = f"https://api.github.com/search/repositories?q={keywords}&sort=stars&order=desc&per_page=5"
response = requests.get(url, headers=headers)
repos = response.json().get("items", [])
```
###  4. Final Response Composition
The final response combines:

✅ LLM answer (based on context)

🔗 GitHub repo suggestions (if relevant)

🛑 Fallback examples if no documents are found




