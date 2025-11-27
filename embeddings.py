from sentence_transformers import SentenceTransformer
import numpy as np

class MedicalEmbedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        print("🔄 Loading AI model for medical embeddings...")
        self.model = SentenceTransformer(model_name)
        self.vector_dimension = 384  # For all-MiniLM-L6-v2
        print(f"✅ Medical Embedder initialized with model: {model_name}")
        print(f"📊 Vector dimension: {self.vector_dimension}")
    
    def generate_embedding(self, text):
        """Generate embedding for medical text"""
        if not text:
            print("⚠️  Warning: Empty text provided")
            return np.zeros(self.vector_dimension).tolist()
        
        # Generate embedding
        embedding = self.model.encode(text)
        print(f"📈 Generated embedding of length: {len(embedding)}")
        return embedding.tolist()
    
    def batch_generate_embeddings(self, texts):
        """Generate embeddings for multiple texts efficiently"""
        if not texts:
            return []
        
        print(f"🔄 Generating embeddings for {len(texts)} texts...")
        embeddings = self.model.encode(texts)
        print(f"✅ Batch embedding generation complete")
        return embeddings.tolist()

def test_embedder():
    """Test the embedding system"""
    print("🧪 Testing Medical Embedding System...")
    
    embedder = MedicalEmbedder()
    
    # Test medical texts
    test_texts = [
        "Patient presents with headache and fever",
        "Cough and sore throat for 3 days",
        "High blood pressure and dizziness",
        "Abdominal pain with nausea and vomiting"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n--- Test {i} ---")
        print(f"📝 Medical text: {text}")
        embedding = embedder.generate_embedding(text)
        print(f"🔢 Embedding length: {len(embedding)}")
        print(f"📊 First 5 values: {[round(x, 4) for x in embedding[:5]]}...")
        
        # Verify it's working
        if len(embedding) == 384 and all(isinstance(x, float) for x in embedding[:5]):
            print("✅ Embedding test PASSED")
        else:
            print("❌ Embedding test FAILED")

if __name__ == "__main__":
    test_embedder()