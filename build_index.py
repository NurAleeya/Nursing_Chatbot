# build_index.py

import os
import pdfplumber
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# === SETTINGS ===
pdf_path = "documents/Section 01 - Medical Emergencies.pdf"
output_folder = "vectorstore"
os.makedirs(output_folder, exist_ok=True)

# === STEP 1: Extract text and tables ===
chunks = []
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        # Extract page text
        text = page.extract_text()
        if text:
            chunks.append(text)

        # Extract tables and clean None values
        tables = page.extract_tables()
        for table in tables:
            table_str = "\n".join([
                "\t".join(cell if cell is not None else "" for cell in row)
                for row in table if any(row)
            ])
            chunks.append("TABLE DATA:\n" + table_str)

print(f"✅ Extracted {len(chunks)} text/table chunks from PDF.")

# === STEP 2: Generate embeddings ===
print("🔄 Embedding chunks using intfloat/e5-small-v2...")
embedder = SentenceTransformer("intfloat/e5-small-v2")
embeddings = embedder.encode(chunks)

# === STEP 3: Save chunks.txt ===
chunks_file = os.path.join(output_folder, "chunks.txt")
with open(chunks_file, "w", encoding="utf-8") as f:
    for chunk in chunks:
        f.write(chunk.replace("\n", " ") + "\n")

print(f"✅ Saved chunks to {chunks_file}")

# === STEP 4: Save FAISS index ===
dim = embeddings[0].shape[0]
index = faiss.IndexFlatL2(dim)
index.add(np.array(embeddings))
faiss.write_index(index, os.path.join(output_folder, "index.faiss"))

print("✅ FAISS index saved to vectorstore/index.faiss")
print("\n🎉 Done! You can now run your Streamlit app with: streamlit run app.py")
