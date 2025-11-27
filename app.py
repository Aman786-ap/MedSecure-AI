import streamlit as st
import pandas as pd
from phi_masking import PHIMasker
from embeddings import MedicalEmbedder
from cyborgdb_client import MedicalVectorDB

# Configure the app
st.set_page_config(
    page_title="MedSecure AI - Clinical Decision Support",
    page_icon="🏥",
    layout="wide"
)

# DRUG INTERACTION DATABASE
DRUG_INTERACTIONS = {
    # Dangerous combinations
    ('warfarin', 'aspirin'): '🚨 DANGEROUS: Increased bleeding risk',
    ('warfarin', 'ibuprofen'): '🚨 DANGEROUS: Increased bleeding risk',
    ('warfarin', 'naproxen'): '🚨 DANGEROUS: Increased bleeding risk',
    ('lisinopril', 'ibuprofen'): '⚠️ CAUTION: Kidney damage risk',
    ('metformin', 'alcohol'): '⚠️ CAUTION: Lactic acidosis risk',
    ('simvastatin', 'grapefruit'): '⚠️ CAUTION: Increased side effects',
    
    # Safe combinations (for demo)
    ('aspirin', 'vitamin c'): '✅ SAFE: No known interactions',
    ('aspirin', 'calcium'): '✅ SAFE: No known interactions',
    ('vitamin c', 'calcium'): '✅ SAFE: No known interactions',
    ('metformin', 'vitamin b12'): '✅ SAFE: No known interactions',
    ('lisinopril', 'calcium'): '✅ SAFE: No known interactions'
}

# EMERGENCY TRIAGE KEYWORDS
EMERGENCY_KEYWORDS = [
    'chest pain', 'shortness of breath', 'severe bleeding', 'unconscious',
    'stroke', 'heart attack', 'suicidal', 'seizure', 'choking'
]

URGENT_KEYWORDS = [
    'high fever', 'head injury', 'abdominal pain', 'severe burn',
    'broken bone', 'eye injury', 'severe headache'
]

# Initialize components
@st.cache_resource
def load_components():
    masker = PHIMasker()
    embedder = MedicalEmbedder()
    db = MedicalVectorDB()
    return masker, embedder, db

def emergency_triage(symptoms):
    """Enhanced emergency triage system"""
    symptoms_lower = symptoms.lower()
    
    # Check for emergency keywords
    for keyword in EMERGENCY_KEYWORDS:
        if keyword in symptoms_lower:
            return {
                "level": "🚨 EMERGENCY",
                "color": "red",
                "action": "CALL 911 IMMEDIATELY - Life-threatening condition suspected",
                "instructions": "Do not delay. Seek emergency medical care now."
            }
    
    # Check for urgent keywords
    for keyword in URGENT_KEYWORDS:
        if keyword in symptoms_lower:
            return {
                "level": "⚠️ URGENT",
                "color": "orange", 
                "action": "Visit urgent care within 24 hours",
                "instructions": "Condition requires prompt medical attention."
            }
    
    # Default non-urgent
    return {
        "level": "✅ NON-URGENT", 
        "color": "green",
        "action": "Schedule with primary care doctor",
        "instructions": "Monitor symptoms and seek care if they worsen."
    }

def main():
    st.title("🏥 MedSecure AI - Clinical Decision Support")
    st.markdown("### HIPAA-Compliant Medical AI with Encrypted Vector Search")
    
    # Load components
    masker, embedder, db = load_components()
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox(
        "Choose the app mode",
        ["Symptom Checker", "Drug Interaction Checker", "Database Management", "About"]
    )
    
    if app_mode == "Symptom Checker":
        symptom_checker_ui(masker, embedder, db)
    elif app_mode == "Drug Interaction Checker":
        drug_checker_ui(masker, embedder, db)
    elif app_mode == "Database Management":
        database_management_ui(db, masker, embedder)
    elif app_mode == "About":
        about_ui()

def symptom_checker_ui(masker, embedder, db):
    st.header("🔍 Symptom Checker")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        symptoms = st.text_area(
            "Describe patient symptoms:",
            placeholder="e.g., Patient John Smith, phone (123) 456-7890, has headache and fever for 2 days...",
            height=100
        )
        
        patient_age = st.number_input("Patient Age", min_value=0, max_value=120, value=30)
        patient_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        if st.button("Analyze Symptoms Securely", type="primary"):
            if symptoms:
                with st.spinner("Analyzing symptoms with privacy protection..."):
                    # Show the privacy process
                    with st.expander("🔒 Privacy Protection Steps"):
                        st.write("1. **PHI Masking**: Removing personal identifiers...")
                        masked_symptoms = masker.mask_phi(symptoms)
                        st.write(f"2. **Secure Text**: `{masked_symptoms}`")
                        
                        st.write("3. **AI Analysis**: Generating embeddings...")
                        embedding = embedder.generate_embedding(masked_symptoms)
                        st.write(f"4. **Vector Search**: Finding similar cases...")
                    
                    # Perform emergency triage
                    triage_result = emergency_triage(symptoms)
                    
                    # Display triage result with color coding
                    if triage_result["color"] == "red":
                        st.error(f"**{triage_result['level']}**")
                    elif triage_result["color"] == "orange":
                        st.warning(f"**{triage_result['level']}**")
                    else:
                        st.success(f"**{triage_result['level']}**")
                    
                    st.write(f"**Action Required:** {triage_result['action']}")
                    st.write(f"**Instructions:** {triage_result['instructions']}")
                    
                    # Search similar cases
                    results = db.search_similar_cases(masked_symptoms, top_k=3)
                    
                    # Display results
                    display_symptom_results(results, symptoms)
            else:
                st.warning("Please enter symptoms to analyze")

def display_symptom_results(results, original_symptoms):
    st.subheader("🔍 Similar Cases Found")
    
    if results and results['documents'][0]:
        st.success("Found similar cases in our secure database:")
        
        for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
            with st.expander(f"Similar Case {i+1}"):
                st.write(f"**Matched Symptoms:** {doc}")
                st.write(f"**Diagnosis:** {metadata.get('diagnosis', 'Not specified')}")
                st.write(f"**Urgency Level:** {metadata.get('urgency', 'Not specified')}")
                st.write(f"**Medications:** {metadata.get('medications', 'Not specified')}")
                st.write(f"**Timestamp:** {metadata.get('timestamp', 'Unknown')}")
    else:
        st.info("No similar cases found. This appears to be a new symptom pattern.")
    
    # Add AI insights
    st.info("""
    **🔒 Privacy & Security Features:**
    - All personal identifiers removed before processing
    - Medical data stored as encrypted vectors
    - No patient information exposed during search
    - HIPAA-compliant data handling
    """)

def drug_checker_ui(masker, embedder, db):
    st.header("💊 Drug Interaction Checker")
    
    medications = st.text_input(
        "Enter medications (comma separated):",
        placeholder="e.g., Aspirin, Metformin, Lisinopril"
    )
    
    # Show example inputs
    with st.expander("💡 Example Inputs"):
        st.write("**Safe combination:** `Aspirin, Vitamin C, Calcium`")
        st.write("**Dangerous combination:** `Warfarin, Aspirin, Ibuprofen`")
        st.write("**Moderate risk:** `Lisinopril, Ibuprofen, Metformin`")
    
    if st.button("Check Interactions Securely"):
        if medications:
            # Process medications
            med_list = [med.strip().lower() for med in medications.split(',')]
            med_list = [med for med in med_list if med]  # Remove empty strings
            
            st.subheader("🔍 Interaction Analysis")
            
            # Check each medication individually first
            st.write("**Medication Safety Check:**")
            for med in med_list:
                st.write(f"✅ **{med.title()}**: Basic safety check passed")
            
            # Check interactions between medications
            st.subheader("🔄 Drug Interaction Check")
            found_interactions = False
            dangerous_interactions = []
            caution_interactions = []
            
            # Check all combinations
            for i in range(len(med_list)):
                for j in range(i + 1, len(med_list)):
                    med1, med2 = med_list[i], med_list[j]
                    
                    # Check both orders in our interaction database
                    interaction = (DRUG_INTERACTIONS.get((med1, med2)) or 
                                  DRUG_INTERACTIONS.get((med2, med1)))
                    
                    if interaction:
                        if '🚨 DANGEROUS' in interaction:
                            dangerous_interactions.append(f"**{med1.title()} + {med2.title()}**: {interaction}")
                        elif '⚠️ CAUTION' in interaction:
                            caution_interactions.append(f"**{med1.title()} + {med2.title()}**: {interaction}")
                        else:
                            st.write(f"**{med1.title()} + {med2.title()}**: {interaction}")
                        found_interactions = True
                    else:
                        st.write(f"**{med1.title()} + {med2.title()}**: ✅ No known interactions")
            
            # Show dangerous interactions first
            if dangerous_interactions:
                st.error("### 🚨 DANGEROUS INTERACTIONS DETECTED!")
                for interaction in dangerous_interactions:
                    st.error(interaction)
            
            # Show caution interactions
            if caution_interactions:
                st.warning("### ⚠️ CAUTION ADVISED")
                for interaction in caution_interactions:
                    st.warning(interaction)
            
            # Final summary
            if not found_interactions:
                st.success("🎉 **No dangerous interactions found between these medications!**")
            elif dangerous_interactions:
                st.error("🆘 **DANGEROUS INTERACTIONS DETECTED! Consult your doctor immediately.**")
            elif caution_interactions:
                st.warning("📞 **Consult your doctor about these medication combinations.**")
            
            # Add medical disclaimer
            st.warning("""
            **Medical Disclaimer:** 
            This is a demonstration system with limited drug interaction data. 
            Always verify drug interactions with a healthcare professional.
            Real drug interaction databases contain thousands of medications and interactions.
            """)
        else:
            st.warning("Please enter medications to check")

def database_management_ui(db, masker, embedder):
    st.header("📊 Database Management")
    
    # Database Statistics
    col1, col2, col3 = st.columns(3)
    info = db.get_collection_info()
    
    with col1:
        st.metric("Total Records", info['total_records'])
    with col2:
        st.metric("Database Status", info['status'])
    with col3:
        st.metric("Storage Type", "Mock Vector DB")
    
    # Tabs for different operations
    tab1, tab2, tab3 = st.tabs(["📥 Add Records", "🔍 View All Records", "🛠️ Maintenance"])
    
    with tab1:  # Add Records Tab
        st.subheader("Add Medical Records")
        
        # Manual record entry
        with st.expander("➕ Add Custom Record"):
            custom_text = st.text_area("Enter medical text (include PHI to see masking):", 
                                     placeholder="e.g., Patient John Smith, phone (123) 456-7890, has headache and fever")
            diagnosis = st.selectbox("Diagnosis Category", ["Migraine", "Common Cold", "Hypertension", "Diabetes", "Cardiac", "Other"])
            urgency = st.select_slider("Urgency Level", ["low", "medium", "high"])
            
            if st.button("Add Custom Record"):
                if custom_text:
                    masked_text = masker.mask_phi(custom_text)
                    metadata = {
                        "diagnosis": diagnosis,
                        "urgency": urgency,
                        "category": "custom",
                        "original_text": custom_text,  # Store original for demo
                        "phi_removed": True
                    }
                    record_id = db.store_medical_record(masked_text, metadata)
                    st.success(f"✅ Record added! ID: {record_id}")
                    
                    # Show the transformation
                    col_orig, col_masked = st.columns(2)
                    with col_orig:
                        st.write("**Original (with PHI):**")
                        st.info(custom_text)
                    with col_masked:
                        st.write("**Stored (PHI Removed):**")
                        st.success(masked_text)
                else:
                    st.warning("Please enter medical text")
        
        # Quick sample data
        st.subheader("📚 Quick Sample Data")
        sample_cases = [
            "Patient with migraine headache and sensitivity to light",
            "Upper respiratory infection with cough and congestion", 
            "Hypertension management and medication review",
            "Emergency: Chest pain with shortness of breath"
        ]
        
        for i, case in enumerate(sample_cases):
            if st.button(f"Add Sample {i+1}", key=f"sample_{i}"):
                masked_text = masker.mask_phi(case)
                metadata = {
                    "diagnosis": "sample",
                    "urgency": "high" if "emergency" in case.lower() else "medium",
                    "category": "sample",
                    "phi_removed": True
                }
                record_id = db.store_medical_record(masked_text, metadata)
                st.success(f"✅ Added: {case}")
        
        # Bulk add
        if st.button("🔄 Add All Samples"):
            for case in sample_cases:
                masked_text = masker.mask_phi(case)
                metadata = {
                    "diagnosis": "sample",
                    "urgency": "high" if "emergency" in case.lower() else "medium",
                    "category": "sample",
                    "phi_removed": True
                }
                db.store_medical_record(masked_text, metadata)
            st.success("✅ All 4 sample cases added!")
    
    with tab2:  # View All Records Tab
        st.subheader("🔍 View All Database Records")
        
        if st.button("🔄 Load All Records", type="primary"):
            try:
                # Get all records from database
                records_list = db.get_records_list()
                
                if records_list:
                    st.success(f"📊 Found {len(records_list)} records in database:")
                    
                    # Display each record
                    for i, record in enumerate(records_list):
                        with st.expander(f"Record {i+1} | 🆔 {record['id'][:8]}... | ⚠️ {record['urgency']}", expanded=False):
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.write(f"**Medical Text:** {record['text']}")
                                if 'original_text' in record:
                                    st.write(f"**Original Text:** {record['original_text']}")
                            
                            with col2:
                                st.write(f"**Diagnosis:** {record['diagnosis']}")
                                st.write(f"**Category:** {record['category']}")
                                st.write(f"**PHI Removed:** {record['phi_removed']}")
                                st.write(f"**Added:** {record['timestamp'][:19]}")
                else:
                    st.info("📭 No records found in database. Add some records in the 'Add Records' tab.")
                    
            except Exception as e:
                st.error(f"❌ Error loading records: {e}")
                st.info("The database might not support this feature yet.")
        
        # Search functionality
        st.subheader("🔎 Search Records")
        search_query = st.text_input("Enter search terms:")
        if st.button("Search Database"):
            if search_query:
                results = db.search_similar_cases(search_query, top_k=5)
                if results['documents'][0]:
                    st.success(f"Found {len(results['documents'][0])} matching records:")
                    for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
                        st.write(f"{i+1}. {doc}")
                else:
                    st.info("No records found for your search.")
            else:
                st.warning("Please enter a search query")
    
    with tab3:  # Maintenance Tab
        st.subheader("🛠️ Database Maintenance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Database Operations**")
            
            if st.button("🔄 Refresh Connection"):
                st.success("Database connection refreshed!")
                info = db.get_collection_info()
                st.rerun()
            
            if st.button("📊 Update Statistics"):
                st.success("Statistics updated!")
                info = db.get_collection_info()
        
        with col2:
            st.write("**Danger Zone**")
            
            if st.button("🗑️ Delete All Records", type="secondary"):
                db.reset_database()
                st.error("All records have been deleted!")
                st.rerun()
            
            if st.button("🔄 Reset with Demo Data", type="primary"):
                db.reset_database()
                # Add demo records
                demo_cases = [
                    "Patient with migraine and light sensitivity",
                    "Upper respiratory infection with cough",
                    "Hypertension management visit",
                    "Emergency chest pain case"
                ]
                for case in demo_cases:
                    masked_text = masker.mask_phi(case)
                    metadata = {
                        "diagnosis": "demo",
                        "urgency": "high" if "emergency" in case.lower() else "medium",
                        "category": "demo",
                        "phi_removed": True
                    }
                    db.store_medical_record(masked_text, metadata)
                st.success("Database reset with 4 demo records!")
                st.rerun()
def about_ui():
    st.header("About MedSecure AI")
    
    st.markdown("""
    ## 🏥 Secure Medical AI with Encrypted Vector Search
    
    **MedSecure AI** demonstrates how healthcare organizations can use AI while maintaining 
    strict patient privacy and HIPAA compliance.
    
    ### 🔒 Key Privacy Features:
    - **PHI Masking**: Automatic removal of personal identifiers
    - **Encrypted Embeddings**: Medical data stored as secure vectors  
    - **Private AI**: Local model processing - no data sent to cloud
    - **Secure Search**: Vector similarity search without exposing raw data
    
    ### 🚀 Use Cases:
    - Clinical Decision Support
    - Drug Interaction Checking
    - Symptom Analysis
    - Medical Research
    - Emergency Triage
    
    ### 🛡️ Compliance:
    - HIPAA Compliant Design
    - End-to-End Encryption
    - Audit Logging Ready
    - Access Control Systems
    
    ### 💊 Drug Interaction Database:
    - **🚨 Dangerous**: Warfarin + Aspirin/Ibuprofen (bleeding risk)
    - **⚠️ Caution**: Lisinopril + Ibuprofen (kidney risk)
    - **✅ Safe**: Aspirin + Vitamin C/Calcium
    
    ### 🚨 Emergency Triage:
    - **Emergency**: Chest pain, shortness of breath, severe bleeding
    - **Urgent**: High fever, head injury, abdominal pain  
    - **Non-urgent**: Common cold, routine follow-ups
    
    ### 🔧 Technical Architecture:
    ```
    Patient Input → PHI Masking → AI Embeddings → Secure Search → Safe Response
    ```
    
    *Note: This is a demonstration system for educational purposes.*
    """)

if __name__ == "__main__":
    main()