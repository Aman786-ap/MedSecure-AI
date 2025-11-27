from mock_database import MockMedicalVectorDB

# Use our mock database instead of ChromaDB
MedicalVectorDB = MockMedicalVectorDB

def test_database():
    """Test the database system"""
    print("🧪 Testing Database System...")
    
    # Initialize database
    db = MedicalVectorDB()
    
    # Test data
    test_records = [
        {
            "text": "Patient presents with headache and fever",
            "metadata": {"diagnosis": "migraine", "urgency": "low"}
        },
        {
            "text": "Cough and sore throat for 3 days",
            "metadata": {"diagnosis": "common cold", "urgency": "low"}
        },
        {
            "text": "Severe chest pain and shortness of breath",
            "metadata": {"diagnosis": "cardiac issue", "urgency": "high"}
        }
    ]
    
    # Store test records
    for record in test_records:
        db.store_medical_record(
            medical_text=record["text"],
            metadata=record["metadata"]
        )
    
    # Test search
    print("\n--- Testing Search ---")
    results = db.search_similar_cases("headache and high temperature", top_k=2)
    
    # Display results
    for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
        print(f"Result {i+1}:")
        print(f"  Text: {doc}")
        print(f"  Metadata: {metadata}")
        print()
    
    # Show collection info
    info = db.get_collection_info()
    print(f"📊 Database info: {info}")
    
    # Test new methods
    print("\n📁 Testing get_all_records:")
    all_records = db.get_all_records()
    print(f"Total records: {len(all_records)}")
    for record_id in all_records:
        print(f"  - {record_id}")

if __name__ == "__main__":
    test_database()