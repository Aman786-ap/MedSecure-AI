import re
from datetime import datetime

class PHIMasker:
    def __init__(self):
        print("✅ PHI Masker initialized - Simple Version")
    
    def mask_phi(self, text):
        """Remove personally identifiable information from medical text"""
        if not text:
            return text
            
        print(f"🔍 Original text: {text}")
        
        # Enhanced rule-based patterns for common PHI
        patterns = {
            'patient_name': r'Patient:\s*[A-Z][a-z]+ [A-Z][a-z]+',
            'doctor_name': r'Dr\.\s*[A-Z][a-z]+',
            'ssn': r'\d{3}-\d{2}-\d{4}',
            'phone': r'\(\d{3}\) \d{3}-\d{4}',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'date': r'\d{1,2}/\d{1,2}/\d{4}',
            'medical_record': r'MRN:\s*\d+',
            'address': r'\d+\s+[A-Za-z\s]+,?\s*[A-Za-z\s]+,?\s*[A-Z]{2}\s*\d{5}',
            'name_standalone': r'\b(?:Mr|Ms|Mrs|Dr)\.?\s+[A-Z][a-z]+ [A-Z][a-z]+\b'
        }
        
        masked_text = text
        for entity_type, pattern in patterns.items():
            masked_text = re.sub(pattern, f'[{entity_type}_REDACTED]', masked_text)
        
        print(f"🔒 Masked text: {masked_text}")
        return masked_text

def test_phi_masking():
    """Test the PHI masking system"""
    print("🧪 Testing PHI Masking System...")
    
    masker = PHIMasker()
    
    # Test cases with sensitive information
    test_cases = [
        "Patient John Smith, phone (123) 456-7890, visited Dr. Johnson on 12/25/2023.",
        "Medical record MRN: 123456 for patient email john.doe@hospital.com",
        "Address: 123 Main Street, New York, NY 10001. Patient complains of headache.",
        "Simple medical note without PHI: patient has fever and cough."
    ]
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        result = masker.mask_phi(test_text)
        print(f"✅ PHI removed successfully")

if __name__ == "__main__":
    test_phi_masking()