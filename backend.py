import os
import pdfplumber
import numpy as np
import faiss
import requests
from sentence_transformers import SentenceTransformer

# === Load embedding model ===
embedder = SentenceTransformer("intfloat/e5-small-v2")

# === STEP 1: Extract text + tables from PDF ===
def extract_text_and_tables(pdf_path):
    data_chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                data_chunks.append(text)

            tables = page.extract_tables()
            for table in tables:
                table_str = "\n".join(["\t".join(row) for row in table if any(row)])
                data_chunks.append("TABLE DATA:\n" + table_str)
    return [chunk.strip() for chunk in data_chunks if chunk.strip()]

# === STEP 2: Embed chunks ===
def embed_chunks(chunks):
    return embedder.encode(chunks)

# === STEP 3: Save FAISS index and chunk text ===
def save_index(chunks, embeddings, path="vectorstore/"):
    os.makedirs(path, exist_ok=True)
    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    faiss.write_index(index, os.path.join(path, "index.faiss"))
    with open(os.path.join(path, "chunks.txt"), "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(c.replace("\n", " ") + "\n")

# === STEP 4: Load FAISS index + chunks ===
def load_index_and_chunks(path="vectorstore/"):
    index = faiss.read_index(os.path.join(path, "index.faiss"))
    with open(os.path.join(path, "chunks.txt"), "r", encoding="utf-8") as f:
        chunks = f.readlines()
    return index, chunks

# === STEP 5: Retrieve top-k relevant chunks ===
def get_relevant_chunks(query, index, chunks, top_k=5):
    q_embedding = embedder.encode([query])
    D, I = index.search(np.array(q_embedding), top_k)
    return [chunks[i].strip() for i in I[0]]

# === STEP 6: Query LM Studio (Mistral 7B) ===
def query_mistral(prompt):
    url = "http://10.203.9.201:1234/v1/completions"  # LM Studio custom IP
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.5
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["text"].strip()
    except Exception as e:
        return f"⚠️ Error connecting to LM Studio: {e}"

# === Optional: Check if LM Studio is online ===
def is_lm_studio_online():
    try:
        r = requests.get("http://10.203.9.201:1234")
        return r.status_code == 200
    except:
        return False
