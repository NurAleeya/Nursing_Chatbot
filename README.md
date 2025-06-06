# KKH Nursing Chatbot

A Streamlit-based chatbot for paediatric medical emergency guidelines with built-in fluid calculator for KKH (KK Women's and Children's Hospital).

## Features

- 💬 **Medical Q&A**: Ask questions based on paediatric medical emergency protocols
- 🧮 **Fluid Calculator**: Calculate paediatric fluid requirements based on weight
- 🩺 **Clinical Support**: Evidence-based responses from hospital guidelines
- 🤖 **AI-Powered**: Uses Mistral AI for intelligent responses

## Project Structure

```
Nursing_Chatbot/
├── app.py              # Main Streamlit application
├── backend.py          # Backend functions for AI processing
├── utils.py            # Utility functions (fluid calculator)
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/NurAleeya/Nursing_Chatbot.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up API keys (create a `.env` file):
```
MISTRAL_API_KEY=your_mistral_api_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage

### Medical Chatbot
1. Enter your paediatric medical question in the text input
2. Click "Ask" to get evidence-based responses
3. The system retrieves relevant information from medical protocols

### Fluid Calculator
1. Enter the child's weight in kilograms
2. Click "Calculate Fluid Requirement"
3. Get the recommended fluid requirement based on paediatric guidelines

## Dependencies

- Streamlit (web interface)
- Backend AI processing modules
- Utility functions for medical calculations

## Contributing

This is a medical application. Please ensure any contributions follow:
- Medical accuracy standards
- Hospital protocol compliance
- Code review processes

## License

[Add appropriate license for medical software]

## Disclaimer

This tool is for educational and clinical support purposes. Always consult with qualified medical professionals for patient care decisions.