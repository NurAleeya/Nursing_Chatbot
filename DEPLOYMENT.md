# KKH Nursing Chatbot - Local Development Setup

## Local Development (for testing with LM Studio)

1. **Start LM Studio server:**
   - Make sure LM Studio is running on `http://10.203.9.201:1234`
   - Load a compatible model (e.g., Mistral, Llama)

2. **Run locally:**
   ```bash
   streamlit run app.py
   ```

## Production Deployment on Streamlit Cloud

### Option 1: Direct Deployment to Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Connect your GitHub account**
3. **Deploy from your repository:**
   - Repository: `NurAleeya/Nursing_Chatbot`
   - Branch: `main`
   - Main file path: `app_production.py`

4. **Set up secrets (if needed):**
   - Go to App settings → Secrets
   - Add any API keys:
   ```toml
   ENVIRONMENT = "production"
   # Add other secrets as needed
   ```

### Option 2: Manual Deployment Steps

1. **Create the app on Streamlit Cloud:**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Choose "From existing repo"
   - Repository: `https://github.com/NurAleeya/Nursing_Chatbot`
   - Branch: `main`
   - Main file: `app_production.py`

2. **Your app will be available at:**
   ```
   https://nuraleeya-nursing-chatbot-app-production-xyz123.streamlit.app
   ```

### Features Available in Production:

✅ **Fluid Calculator** - Works offline, no dependencies
✅ **PDF Document Display** - Medical emergency protocols  
✅ **Vector Search** - Pre-built embeddings included
⚠️ **AI Chat** - Limited (requires API setup)

### Troubleshooting:

- If AI chat doesn't work in production, only the fluid calculator will be available
- The vectorstore folder contains pre-built embeddings that work offline
- Check the logs in Streamlit Cloud for any deployment issues

## Local vs Production Differences:

| Feature | Local (app.py) | Production (app_production.py) |
|---------|----------------|--------------------------------|
| LM Studio | ✅ Uses local server | ❌ Not available |
| Fluid Calculator | ✅ Full functionality | ✅ Full functionality |
| Error Handling | Basic | Enhanced with fallbacks |
| UI Messages | Development focused | User-friendly |
