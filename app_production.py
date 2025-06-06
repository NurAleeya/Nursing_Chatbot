import streamlit as st
from backend import load_index_and_chunks, get_relevant_chunks, query_mistral
from utils import calc_fluid_requirement

# Configure Streamlit page
st.set_page_config(page_title="KKH Nursing Chatbot", layout="wide")
st.title("🩺 KKH Nursing Chatbot")
st.markdown("Ask clinical questions based on paediatric medical emergency guidelines. You can also use the built-in fluid calculator.")

# Check if running locally or in production
if st.secrets.get("ENVIRONMENT") == "production":
    st.info("🚀 This app is running in production mode. Some features may be limited.")

try:
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

except Exception as e:
    st.error(f"⚠️ Error loading AI components: {e}")
    st.info("The chatbot functionality is currently unavailable, but you can still use the fluid calculator below.")

# --- Fluid Calculator Interface ---
st.divider()
st.header("🧮 Paediatric Fluid Calculator")
st.markdown("This calculator works offline and provides fluid requirements based on standard paediatric guidelines.")

weight = st.number_input("Enter child's weight (kg):", min_value=0.0, step=0.1)

if st.button("Calculate Fluid Requirement"):
    if weight <= 0:
        st.warning("Please enter a valid weight.")
    else:
        result = calc_fluid_requirement(weight)
        st.success(result)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
    <p>⚠️ <strong>Medical Disclaimer:</strong> This tool is for educational purposes only. 
    Always consult with qualified medical professionals for patient care decisions.</p>
    <p>📧 For technical issues, contact your IT administrator.</p>
</div>
""", unsafe_allow_html=True)
