import pandas as pd
from langchain.docstore.document import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Load ideas.csv
df = pd.read_csv("chatbot/data/ideas.csv")

docs = []

# Loop over each row
for i, row in df.iterrows():
    title = f"Title: {row['Title']}"
    category = f"Category: {row['Category']}"
    tech_stack = f"Tech Stack: {row['Tech Stack']}"
    difficulty = f"Difficulty: {row['Difficulty']}"
    description = f"Description: {row['Description']}"

    full_text = f"{title}\n{category}\n{tech_stack}\n{difficulty}\n{description}"
    docs.append(Document(page_content=full_text))

# Embed using HuggingFace
embedding = HuggingFaceEmbeddings(model_name="thenlper/gte-small")

# Store in Chroma vector DB
db = Chroma.from_documents(
    docs,
    embedding=embedding,
    persist_directory="embeddings/ideas"
)

db.persist()
print("✅ Your project ideas are now stored in ChromaDB!")
