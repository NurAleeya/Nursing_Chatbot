import streamlit as st

# Embedded fluid calculator function (no external dependencies)
def calc_fluid_requirement(weight_kg: float) -> str:
    """
    Calculates daily maintenance fluid requirement using the Holliday-Segar formula.
    
    - 100 ml/kg for first 10 kg
    - 50 ml/kg for next 10 kg
    - 20 ml/kg for every kg above 20 kg
    """
    if weight_kg <= 0:
        return "Invalid weight."
    
    if weight_kg <= 10:
        total = weight_kg * 100
    elif weight_kg <= 20:
        total = 1000 + (weight_kg - 10) * 50
    else:
        total = 1500 + (weight_kg - 20) * 20

    return f"Estimated Daily Fluid Requirement: {total:.0f} ml/day"

# Embedded backend functions for production (no external dependencies)
import os
import pickle

def load_simple_chunks():
    """Load pre-built text chunks from file"""
    try:
        chunks_path = "vectorstore/chunks.txt"
        if os.path.exists(chunks_path):
            with open(chunks_path, 'r', encoding='utf-8') as f:
                chunks = [line.strip() for line in f.readlines() if line.strip()]
            return chunks
        return []
    except Exception:
        return []

def simple_search(query, chunks, max_results=3):
    """Simple keyword-based search as fallback"""
    query_words = query.lower().split()
    scored_chunks = []
    
    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = sum(1 for word in query_words if word in chunk_lower)
        if score > 0:
            scored_chunks.append((score, chunk))
    
    # Sort by score and return top results
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return [chunk for score, chunk in scored_chunks[:max_results]]

# Try to load chunks
try:
    chunks = load_simple_chunks()
    BACKEND_AVAILABLE = len(chunks) > 0
    if not BACKEND_AVAILABLE:
        st.warning("📚 Medical knowledge base not found. Only fluid calculator is available.")
except Exception as e:
    BACKEND_AVAILABLE = False
    chunks = []
    st.warning(f"⚠️ Could not load medical knowledge base: {e}")

# Utils is now embedded, so always available
UTILS_AVAILABLE = True

# Configure Streamlit page
st.set_page_config(page_title="KKH Nursing Chatbot", layout="wide")
st.title("🩺 KKH Nursing Chatbot")
st.markdown("Ask clinical questions based on paediatric medical emergency guidelines. You can also use the built-in fluid calculator.")

# Check if running locally or in production (safe check)
try:
    if st.secrets.get("ENVIRONMENT") == "production":
        st.info("🚀 This app is running in production mode. Some features may be limited.")
except Exception:
    # Running locally without secrets file - this is normal
    pass

# --- Chatbot Interface ---
st.header("💬 Ask a Medical Question")

if BACKEND_AVAILABLE:
    query = st.text_input("Enter your medical or nursing question:")

    if st.button("Ask"):
        if query.strip() == "":
            st.warning("Please enter a question.")
        else:
            with st.spinner("Searching medical knowledge base..."):
                try:
                    # Use simple search instead of AI embeddings
                    relevant_chunks = simple_search(query, chunks, max_results=3)
                    
                    if relevant_chunks:
                        st.subheader("📋 Relevant Medical Information")
                        for i, chunk in enumerate(relevant_chunks, 1):
                            with st.expander(f"Reference {i}"):
                                st.markdown(chunk)
                    else:
                        st.info("No specific information found in the medical knowledge base for your query.")
                        
                    st.info("💡 **Note:** This is a simplified search. For more accurate results, consult medical professionals or detailed clinical guidelines.")
                    
                except Exception as e:
                    st.error(f"Search error: {e}")
                    st.info("Please try a different search term or consult medical professionals.")
else:
    st.warning("⚠️ The medical knowledge base is currently unavailable. Only the fluid calculator is accessible.")
    st.info("💊 You can still use the pediatric fluid calculator below for basic calculations.")

# --- Fluid Calculator Interface ---
st.divider()
st.header("🧮 Paediatric Fluid Calculator")

if UTILS_AVAILABLE:
    st.markdown("This calculator works offline and provides fluid requirements based on standard paediatric guidelines.")

    weight = st.number_input("Enter child's weight (kg):", min_value=0.0, step=0.1)

    if st.button("Calculate Fluid Requirement"):
        if weight <= 0:
            st.warning("Please enter a valid weight.")
        else:
            result = calc_fluid_requirement(weight)
            st.success(result)
else:
    st.warning("⚠️ Fluid calculator is unavailable due to missing dependencies.")
    st.markdown("**Manual Calculation Guide:**")
    st.markdown("""
    - **First 10 kg:** 100 mL/kg/day
    - **Next 10 kg (11-20 kg):** 50 mL/kg/day  
    - **Each kg above 20 kg:** 20 mL/kg/day
    
    **Example:** 25 kg child = (10×100) + (10×50) + (5×20) = 1000 + 500 + 100 = 1600 mL/day
    """)
    st.info("Always consult medical professionals for accurate fluid management.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
    <p>⚠️ <strong>Medical Disclaimer:</strong> This tool is for educational purposes only. 
    Always consult with qualified medical professionals for patient care decisions.</p>
    <p>📧 For technical issues, contact your IT administrator.</p>
</div>
""", unsafe_allow_html=True)
