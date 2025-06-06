import streamlit as st
from backend import load_index_and_chunks, get_relevant_chunks, query_mistral
from utils import calc_fluid_requirement

# Configure Streamlit page
st.set_page_config(page_title="KKH Nursing Chatbot", layout="wide")
st.title("🩺 KKH Nursing Chatbot")
st.markdown("Ask clinical questions based on paediatric medical emergency guidelines. You can also use the built-in fluid calculator.")

# Load embedding index and text chunks
index, chunks = load_index_and_chunks()

# --- Chatbot Interface ---
st.header("💬 Ask a Medical Question")
query = st.text_input("Enter your medical or nursing question:")

if st.button("Ask"):
    if query.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Retrieving relevant information..."):
            top_chunks = get_relevant_chunks(query, index, chunks, top_k=5)
            context = "\n\n".join(top_chunks)

            prompt = f"""You are a paediatric clinical assistant. Use the following medical context to answer clearly, based on hospital protocols:

Context:
{context}

Question: {query}
Answer:"""

            answer = query_mistral(prompt)

        st.subheader("🧠 Assistant's Response")
        st.markdown(answer)


# --- Fluid Calculator Interface ---
st.divider()
st.header("🧮 Paediatric Fluid Calculator")

weight = st.number_input("Enter child’s weight (kg):", min_value=0.0, step=0.1)

if st.button("Calculate Fluid Requirement"):
    if weight <= 0:
        st.warning("Please enter a valid weight.")
    else:
        result = calc_fluid_requirement(weight)
        st.success(result)
