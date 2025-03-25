import sys
sys.path.append("/opt/anaconda3/lib/python3.12/site-packages")  # Ensure correct package path

from langchain_groq import ChatGroq  # Now import should work
from langchain.prompts import PromptTemplate
from langchain.document_loaders import WebBaseLoader
from dotenv import load_dotenv
from models.data_clean import initialize_chromadb
from bs4 import BeautifulSoup
import requests
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
    cleaned_answers = [answer.split(") ", 1)[1] if ") " in answer else answer for answer in user_answers]  # Removes 'A)', 'B)' etc.
    # cleaned_answers = "I love coding"
    query_text = " ".join(cleaned_answers)  # Combine cleaned responses
    results = collection.query(query_texts=[query_text], n_results=3)
    if not results:
        return ["No match found"]
    else:
        job_id = extract_job_ids(results["documents"])
        jobs = fetch_web_results(job_id)
        print(jobs)
        return jobs
    # return results["documents"] if results["documents"] else ["No match found"]

def fetch_web_results(ids):
    final = []
    for i in ids:
        id = i[0]

        """Fetches the header and first <p> content from a given career page and returns as a string."""
        url = f"https://www.onetonline.org/link/details/{id}"
        
        try:
            response = requests.get(url, timeout=10)  # Fetch the page with a timeout
            response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        except requests.RequestException as e:
            return f"Error: Failed to fetch data ({str(e)})"

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract job title (assuming it's inside an <h1> tag)
        header = soup.find("h1").get_text(strip=True) if soup.find("h1") else "No header found"

        # Extract the first meaningful paragraph
        first_paragraph = None
        for p in soup.find_all("p"):
            text = p.get_text(strip=True)
            if len(text) > 30:  # Ensure it's a meaningful paragraph
                first_paragraph = text
                break

        if not first_paragraph:
            first_paragraph = "No description available"

        # Remove job codes, "Bright Outlook", and "Updated YYYY"
        header = re.sub(r'\d{2}-\d{4}\.\d{2}', '', header)  # Remove job codes like 11-1021.00
        header = re.sub(r'(Bright Outlook|Updated \d{4})', '', header).strip()  # Remove "Bright Outlook" and "Updated YYYY"

        final.append(f"{header} : {first_paragraph}")  # Return as a single formatted string
    return final

def extract_job_ids(texts):
    """Extracts only job role IDs from the given text."""
    matches = []
    for element in texts:
        for text in element:
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