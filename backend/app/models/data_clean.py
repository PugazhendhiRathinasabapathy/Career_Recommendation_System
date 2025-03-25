import sys
sys.path.append("/opt/anaconda3/lib/python3.12/site-packages")  # Ensure correct package path

# Loading data for using RAG
import pandas as pd
import chromadb

def load_and_clean_data(filepath):
    """Loads, cleans, and preprocesses career data from an Excel file."""
    data = pd.read_excel(filepath)

    # Convert all data to string format to ensure compatibility
    data = data.astype(str).dropna()

    # Create unique IDs for each row
    data["id"] = data.index.astype(str)

    # Combine relevant text columns into one text field for embedding
    data["combined_text"] = data.apply(lambda row: " | ".join(row.values), axis=1)

    # Define column names
    column_names = [
        'O*NET-SOC Code', 'Title', 'Description', 'Interests', 'Knowledge', 
        'Skills', 'Technology Skills', 'Tools Used', 'id', 'combined_text'
    ]
    data.columns = column_names

    return data

def initialize_chromadb(db_path="./processed_data/chroma_db"):
    """Initializes ChromaDB client and returns the collection."""
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_or_create_collection(name="career_recommendation")
    return chroma_client, collection

def store_data_in_chromadb(data, collection):
    """Stores cleaned career data in ChromaDB."""
    collection.add(
        ids=data["id"].astype(str).tolist(),
        documents=data["combined_text"].tolist(),
    )
    print(f"✅ Total records stored: {collection.count()}")

def main():
    """Main function to clean data and store it in ChromaDB."""
    data = load_and_clean_data("/Users/pugazhendhi/MachineLearning/Career_Recommendation_System/backend/app/models/processed_data/Final_Occupation_Data_Cleaned.xlsx")
    chroma_client, collection = initialize_chromadb()
    store_data_in_chromadb(data, collection)

    # Perform a sample similarity search
    query_result = collection.query(
        query_texts=["I am good at art and design, and I enjoy working with my hands."],
        n_results=5  
    )

    # Display results
    for i, doc in enumerate(query_result["documents"][0]):  
        print(f"🔹 Match {i+1}: {doc}\n")

if __name__ == "__main__":
    main()