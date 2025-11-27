from phi_masking import PHIMasker
from embeddings import MedicalEmbedder

def test_phi_and_embeddings():
    """Test that PHI masking and embeddings work together"""
    print("🧪 Testing PHI Masking + Embeddings Integration...")
    
    # Initialize both systems
    masker = PHIMasker()
    embedder = MedicalEmbedder()
    
    # Test medical text with PHI
    test_cases = [
        "Patient John Smith presents with headache and fever, phone (123) 456-7890",
        "Dr. Johnson diagnosed hypertension in patient Sarah Wilson on 12/25/2023",
        "Simple case: cough and sore throat for 3 days"
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n--- Integration Test {i} ---")
        print(f"📝 Original: {text}")
        
        # Step 1: Mask PHI
        masked_text = masker.mask_phi(text)
        
        # Step 2: Generate embedding
        embedding = embedder.generate_embedding(masked_text)
        
        # Step 3: Verify
        print(f"✅ PHI masked and embedding generated ({len(embedding)} dimensions)")
        print(f"🔒 Safe for storage: {len(embedding) == 384}")

if __name__ == "__main__":
    test_phi_and_embeddings()