# 🏥 MedSecure AI - Secure Medical AI with Encrypted Vector Search

## 🚀 Hackathon Project for CyborgDB

A HIPAA-compliant medical AI system that provides clinical decision support while maintaining complete patient privacy through encrypted vector search.

### 🔒 Key Features
- **PHI Masking**: Automatic removal of personal health information
- **Drug Interaction Checking**: Secure medication safety analysis
- **Emergency Triage**: AI-powered symptom urgency assessment
- **Encrypted Vector Search**: Privacy-preserving medical case retrieval
- **Mock CyborgDB Integration**: Demonstrates encrypted vector database concept

### 🛠️ Technology Stack
- **Frontend**: Streamlit
- **AI/ML**: Sentence Transformers, spaCy
- **Vector Database**: Mock CyborgDB (easily replaceable with real CyborgDB)
- **Security**: PHI detection, encryption simulation
- **Deployment**: Python, Virtual Environment

### 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/Aman786-ap/medsecure-ai.git
cd medsecure-ai

2. **Set up virtual environment**
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
Install dependencies
pip install -r requirements.txt

# Download spaCy model (if needed)
python -m spacy download en_core_web_sm
Run the application
streamlit run app.py

🎯 Usage Examples

Symptom Checker:
Input: "Patient John Smith, phone (123) 456-7890, has headache and fever"
Output: "Patient [REDACTED], phone [REDACTED], has headache and fever"

Drug Interaction Checker:
Input: "Warfarin, Aspirin, Ibuprofen"
Output: "🚨 DANGEROUS: Increased bleeding risk"

Emergency Triage:
Input: "Chest pain and shortness of breath"
Output: "🚨 EMERGENCY - CALL 911 IMMEDIATELY"

🏗️ Architecture
Patient Input → PHI Masking → AI Embeddings → Encrypted Vector Search → Safe Response

📁 Project Structure
medsecure-ai/
├── app.py                 # Main Streamlit application
├── phi_masking.py         # PHI masking and privacy protection
├── embeddings.py          # AI embedding generation
├── cyborgdb_client.py     # Database interface
├── mock_database.py       # Mock vector database simulation
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── .gitignore            # Git ignore rules

🎪 Demo Features

Real-time PHI Detection: Automatically masks names, phones, emails, medical IDs
Drug Interaction Database: 10+ medication pairs with safety ratings
Emergency Triage System: 3-level urgency assessment (Emergency/Urgent/Routine)
Encrypted Vector Search: Privacy-preserving medical case retrieval
Professional Medical UI: Streamlit-based healthcare interface

🔮 Future Enhancements

Integrate real CyborgDB for encrypted vector storage
Add advanced PHI detection with machine learning
Implement real EHR system integration
Deploy as HIPAA-compliant web service
Add multi-language support for global healthcare
Integrate wearable device data for real-time monitoring

👥 Contributor
Aman Unus Pathan

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments

CyborgDB for the hackathon opportunity and encrypted vector database concept
Sentence Transformers for medical text embeddings
Streamlit for the interactive web framework
spaCy for natural language processing capabilities

🚨 Quick Start for Hackathon Judges

# 1. Clone and setup
git clone https://github.com/Aman786-ap/medsecure-ai.git
cd medsecure-ai

# 2. Install and run (Windows)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py

# 3. Test these demo inputs:
# Symptom Checker: "Patient John Smith, (123) 456-7890, chest pain and sweating"
# Drug Checker: "Warfarin, Aspirin, Ibuprofen"
# Database: Add sample records and view them
The application will open at: http://localhost:8501

<div align="center">
Built with ❤️ for the CyborgDB Hackathon

Making Healthcare AI Safe and Private

</div>
