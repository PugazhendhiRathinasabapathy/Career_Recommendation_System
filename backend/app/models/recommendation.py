import sys
sys.path.append("/opt/anaconda3/lib/python3.12/site-packages")  # Ensure correct package path

from langchain_groq import ChatGroq  # Now import should work
from langchain.prompts import PromptTemplate
from langchain.document_loaders import WebBaseLoader
from dotenv import load_dotenv
from data_clean import initialize_chromadb
import os
import re # Regular Expression

# Load environment variables
load_dotenv()

def setup_llm():
    """Initializes the LLM model."""
    return ChatGroq(
        model='llama3-8b-8192',
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.5
    )

llm = setup_llm()
_, collection = initialize_chromadb()
user_memory = []

def generate_question(previous_answers):
    """Generates a career-related question dynamically based on previous answers."""
    prompt = PromptTemplate.from_template("""
    You are an intelligent career advisor AI that helps users find the most suitable career based on their responses. 
    Your job is to **ask one question at a time**, with four multiple-choice options.

    ### **Instructions:**
    1. The next question should be relevant based on the user's previous answers.
    2. Keep the question concise but informative.
    3. Make sure the four answer choices represent **distinct career-related preferences**.
    4. The answers should be **diverse** (e.g., different skills, interests, or work preferences).

    ### **User Responses So Far:**
    {previous_answers}

    ### **Output Format:**
    No Preamble, just the question and options.
    Question: <your generated question>
    A) <Option 1>
    B) <Option 2>
    C) <Option 3>
    D) <Option 4>
    """)
    
    full_prompt = prompt.format(previous_answers=", ".join(previous_answers))
    return llm.invoke(full_prompt)

def get_career_recommendations(user_answers):
    """Queries ChromaDB for career matches based on user answers."""
    query_text = " ".join(user_answers)  # Combine responses
    results = collection.query(query_texts=[query_text], n_results=3)  # Get top 3 matches
    
    return results["documents"][0] if results["documents"] else ["No match found"]

def fetch_web_results(id):
    """Fetches web-based information for a given career."""
    url = "https://www.google.com/"
    loader = WebBaseLoader(url)
    return loader.load()

def extract_job_ids(texts):
    """Extracts only job role IDs from the given text."""
    matches = []
    for text in texts:
        pattern = r'(\d{2}-\d{4}\.\d{2})'
        matches.append(re.findall(pattern, text))
    return matches

def run_career_advisor():
    """Runs the interactive career recommendation process."""
    global user_memory
    for _ in range(5):  # Change to 20 for full experience
        question = generate_question(user_memory)
        print("\n", question)
        
        # Simulate user selecting an answer (in real use case, get input from user)
        user_response = input("Choose an option (A, B, C, D): ")
        user_memory.append(user_response)  # Store answer

    # Get Career Recommendations
    career_matches = get_career_recommendations(user_memory)
    print("\n🎯 Recommended Careers:", extract_job_ids(career_matches))

# Run the program if executed directly
if __name__ == "__main__":
    run_career_advisor()