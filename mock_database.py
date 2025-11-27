import uuid
from datetime import datetime

class MockMedicalVectorDB:
    """Mock database that simulates vector search without external dependencies"""
    
    def __init__(self, persist_directory=None):
        print("🔄 Initializing Mock Medical Database...")
        self.records = {}
        self.collection_name = "medical_records"
        print("✅ Mock database initialized (no external dependencies required)")
    
    def store_medical_record(self, medical_text, metadata=None):
        """Store medical record in mock database"""
        if metadata is None:
            metadata = {}
        
        record_id = str(uuid.uuid4())
        
        full_metadata = {
            **metadata,
            'timestamp': datetime.now().isoformat(),
            'phi_removed': True,
            'text': medical_text
        }
        
        self.records[record_id] = full_metadata
        print(f"✅ Mock stored record with ID: {record_id}")
        print(f"   Text: {medical_text}")
        return record_id
    
    def search_similar_cases(self, query_text, top_k=5, filters=None):
        """Mock similarity search based on keyword matching"""
        print(f"🔍 Mock searching for: '{query_text}'")
        
        # Simple keyword-based "similarity" search
        query_words = query_text.lower().split()
        matches = []
        
        for record_id, metadata in self.records.items():
            text = metadata.get('text', '').lower()
            score = sum(1 for word in query_words if word in text)
            
            if score > 0:
                matches.append((score, metadata))
        
        # Sort by match score and take top_k
        matches.sort(key=lambda x: x[0], reverse=True)
        top_matches = matches[:top_k]
        
        # Format results to match ChromaDB format
        documents = [match[1]['text'] for match in top_matches]
        metadatas = [{k: v for k, v in match[1].items() if k != 'text'} for match in top_matches]
        
        print(f"✅ Mock found {len(documents)} similar cases")
        return {'documents': [documents], 'metadatas': [metadatas]}
    
    def get_collection_info(self):
        """Get mock collection info"""
        return {
            'total_records': len(self.records),
            'collection_name': self.collection_name,
            'status': 'mock_database_active'
        }
    
    def reset_database(self):
        """Reset the database (for testing)"""
        self.records = {}
        print("✅ Mock database reset complete")
    
    def get_all_records(self):
        """Get all records from the database for viewing"""
        print(f"📊 Retrieving all {len(self.records)} records...")
        return self.records
    
    def get_records_list(self):
        """Get records in a format suitable for display"""
        records_list = []
        for record_id, metadata in self.records.items():
            records_list.append({
                'id': record_id,
                'text': metadata.get('text', ''),
                'diagnosis': metadata.get('diagnosis', 'N/A'),
                'urgency': metadata.get('urgency', 'N/A'),
                'category': metadata.get('category', 'N/A'),
                'timestamp': metadata.get('timestamp', 'N/A'),
                'phi_removed': metadata.get('phi_removed', True)
            })
        return records_list
    
    def show_database_contents(self):
        """Simple method to display database contents"""
        if not self.records:
            return "Database is empty"
        
        result = f"Database has {len(self.records)} records:\n"
        for record_id, metadata in self.records.items():
            result += f"\n🔹 {record_id[:8]}...: {metadata.get('text', 'No text')}\n"
        return result

def test_mock_database():
    """Test the mock database"""
    print("🧪 Testing Mock Database...")
    
    db = MockMedicalVectorDB()
    
    # Store test records
    test_records = [
        "Patient with headache and fever",
        "Cough and sore throat for 3 days",
        "Chest pain and breathing difficulty"
    ]
    
    for text in test_records:
        db.store_medical_record(text, metadata={"urgency": "low"})
    
    # Test search
    results = db.search_similar_cases("headache fever", top_k=2)
    
    print("📋 Search results:")
    for i, doc in enumerate(results['documents'][0]):
        print(f"  {i+1}. {doc}")
    
    print(f"📊 Database info: {db.get_collection_info()}")
    
    # Test new methods
    print("\n📁 All records:")
    all_records = db.get_all_records()
    for record_id, metadata in all_records.items():
        print(f"  {record_id}: {metadata.get('text')}")
    
    print("✅ Mock database test completed!")

if __name__ == "__main__":
    test_mock_database()