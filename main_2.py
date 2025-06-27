from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

import json
import requests
import threading
from github_search_agent import GitHubSearchAgent
from google_adk.framework.message import Message
from concurrent.futures import ThreadPoolExecutor, TimeoutError

from openai import OpenAI

# --- Embeddings & Chroma Setup ---
embedding = HuggingFaceEmbeddings(model_name="thenlper/gte-small")
datasets_db = Chroma(persist_directory="embeddings/resources", embedding_function=embedding)
ideas_db = Chroma(persist_directory="embeddings/ideas", embedding_function=embedding)


# --- GitHub Repo Search ---
# --- GitHub repo search agent ---
def fetch_github_repos(query):
    # Generic inputs that shouldn't trigger GitHub repo search
    GENERIC_INPUTS = {"heyy", "hey", "hi", "hello", "yo", "sup", "help", "pls", "ok", "hii", "new project"}

    if query.strip().lower() in GENERIC_INPUTS:
        print(" ", query)
        return ""

    try:
        github_agent = GitHubSearchAgent()
        github_output = github_agent.run(Message(content=query)).content
        repos = json.loads(github_output)
        if isinstance(repos, list) and repos:
            repo_links = "\n".join(
                [f"- [{r['name']}]({r['url']}) ⭐ {r['stars']}" for r in repos]
            )
            return f"\n\n🔗 **Top GitHub Projects:**\n{repo_links}"
    except Exception as e:
        return f"\n\n⚠️ GitHub Search Error: {e}"
    return ""

# --- Together API Call ---
def call_together_ai(prompt):
    client = OpenAI(
        api_key="YOUR-API-KEY",
        base_url="https://api.together.xyz/v1"
    )
    try:
        response = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for hackathons and dataset projects."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return {"content": response.choices[0].message.content.strip()}
    except Exception as e:
        return {"content": f"❌ Together API error: {e}"}

# --- RAG Answer Generator ---
def generate_answer(query):
    print("Generating answer for query:", query)
    all_contexts = []

    def fetch_docs(db, tag):
        print(f"🔍 Searching {tag} DB...")
        try:
            docs = db.similarity_search(query, k=3)
            print(f"✅ Found {len(docs)} docs in {tag}")
            return [f"[{tag.upper()}] {doc.page_content.strip()}" for doc in docs if doc.page_content.strip()]
        except Exception as e:
            print(f"❌ Error in {tag} search:", e)
            return []

    with ThreadPoolExecutor() as executor:
        dataset_future = executor.submit(fetch_docs, datasets_db, "datasets")
        ideas_future = executor.submit(fetch_docs, ideas_db, "ideas")
        github_future = executor.submit(fetch_github_repos, query)

        all_contexts.extend(dataset_future.result())
        all_contexts.extend(ideas_future.result())

    all_contexts = list(dict.fromkeys(all_contexts))  # dedupe

    if not all_contexts:
        print("⚠️ No docs found. Using fallback context.")
        all_contexts = [
            "[IDEAS] YOLO-based helmet detection system for factory workers.",
            "[DATASETS] WHO Brain MRI dataset helps in brain tumor detection."
        ]

    context = "\n---\n".join(all_contexts)[:1200]
    print("📎 Final context to send:\n", context)

    prompt = f"""
You are a helpful assistant for hackathons and dataset projects.

Based on the context provided below, answer the question clearly and concisely. 
If relevant project ideas or datasets are present in the context, use them. 
If not, say you couldn't find anything directly relevant and suggest good alternatives.

Context:
{context}

Question:
{query}

Answer:
""".strip()

    try:
        with ThreadPoolExecutor() as executor:
            future = executor.submit(call_together_ai, prompt)
            response = future.result(timeout=180)
            llm_answer = response['content']
    except TimeoutError:
        llm_answer = "❌ Together API timed out. Try a simpler query."
    except Exception as e:
        llm_answer = f"❌ Together API error: {e}"
        print(llm_answer)

    github_response = github_future.result()

    GENERIC_REPOS = [
        "project-based-learning", "bootstrap", "HelloGitHub", "awesome-for-beginners", "moby"
    ]

    def is_useful_github_response(response: str) -> bool:
        if not response.strip():
            return False
        if "❌" in response or "GitHub Search Error" in response:
            return False
        if any(repo in response for repo in GENERIC_REPOS):
            return False
        return True

    if is_useful_github_response(github_response):
        return f"\n\n{llm_answer}{github_response}"
    else:
        return f"\n\n{llm_answer}"

# --- CLI Entry ---
if __name__ == "__main__":
    print(" Hello! I'm your hackathon assistant. Ask me anything.")
    while True:
        query = input("Ask your chatbot: ")
        if query.lower() in ["exit", "quit"]:
            print(" Goodbye!")
            break
        print(generate_answer(query))
