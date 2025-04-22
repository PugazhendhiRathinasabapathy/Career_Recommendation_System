import sys
sys.path.append("/opt/anaconda3/lib/python3.12/site-packages")  # Ensure correct package path

from langchain_groq import ChatGroq  # Now import should work
from langchain_core.output_parsers.string import StrOutputParser 
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
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
history = {}

def gen_questions_langchain(history):
    history = history
    prompt1 = ChatPromptTemplate.from_messages([
        ("system", "You are an AI career advisor. Your ONLY task is to ask one career-related multiple-choice question at a time with exactly four answer options. You must ask questions in order to narrow the user's career path based on their responses. You must always provide 4 options no matter what, never ask a question without 4 options. Do not provide preamble or introduction. Respond strictly in this format:\n\nQuestion: <your question>\nA) <Option A>\nB) <Option B>\nC) <Option C>\nD) <Option D>"),
        ("user", "What is your favorite programming language?")
    ])

    chain1 = prompt1 | llm | StrOutputParser()

    categories = [
        "Interests", 
        "Skills", 
        "Education", 
        "Experience", 
        "Work Environment Preferences", 
        "Industry Preference", 
        "Career Growth Aspirations"
    ]
    current_category = categories[len(history) % len(categories)]

    prompt2 = ChatPromptTemplate.from_messages([
        ("system", """Generates a career-related question dynamically based on previous answers.

        You are an AI career advisor. Your ONLY task is to ask **one career-related multiple-choice question at a time** with exactly **four answer options**.
        You must ask questions in order to narrow the user's career path based on their responses. 
        You must always provide 4 options no matter what, never ask a question without 4 options.
        You must NOT REPEAT questions.

        ### **Instructions (Strict Adherence Required):**
        1. **NO preamble, NO introduction, NO explanations.**
        2. The question must be about **{current_category}**.
        3. **Output Format:**
        - **Question:** (Concise, relevant, and informative)
        - **Four answer choices (A, B, C, D) is a must**
        4. The next question must be **influenced by previous answers** but still follow category rotation.

        ### **User Responses So Far:**
        {history}

        ### **Output Format (STRICTLY FOLLOW THIS, NO EXTRA TEXT):**
        Question: <your generated question>  
        A) <Option 1>  
        B) <Option 2>  
        C) <Option 3>  
        D) <Option 4>  
        """),
        ("user", "Based on all previous answers, generate the next career question.")
    ])

    chain2 = prompt2 | llm | StrOutputParser()

    if not history:
        # First question
        question = chain1.invoke({})
        # history[question]=None  # Removed to prevent double entry
        return question
    else:
        # Before passing to chain2, truncate history to recent entries
        short_history = dict(list(history.items())[-5:])  # Use only the last 5 Q&A pairs

        question = chain2.invoke({
            "history": short_history,
            "current_category": current_category
        })
        # history[question]=None  # Removed to prevent double entry
        return question


#def generate_question(previous_answers):
    """Generates a career-related question dynamically based on previous answers."""
    
    # Handle Empty previous_answers to prevent errors
    previous_answers_str = ", ".join(previous_answers) if previous_answers else "No responses yet"
    
    # Expanded category list for better recommendations
    categories = [
        "Interests", 
        "Skills", 
        "Education", 
        "Experience", 
        "Work Environment Preferences", 
        "Industry Preference", 
        "Career Growth Aspirations"
    ]
    
    # Rotate through categories based on previous answers count
    next_category = categories[len(previous_answers) % len(categories)]  

    # Define the prompt template correctly
    prompt_template = PromptTemplate.from_template("""
    You are an AI career advisor. Your ONLY task is to ask **one career-related multiple-choice question at a time** with exactly **four answer options**.
    You must ask questions in order to narrow the user's career path based on their responses. 
    You must always provide 4 options no matter what, never ask a question without 4 options.
    You must NOT REPEAT questions.

    ### **Instructions (Strict Adherence Required):**
    1. **NO preamble, NO introduction, NO explanations.**
    2. The question must be about **{next_category}**.
    3. **Output Format:**
       - **Question:** (Concise, relevant, and informative)
       - **Four answer choices (A, B, C, D) is a must**
    4. The next question must be **influenced by previous answers** but still follow category rotation.
    
    ### **User Responses So Far:**
    {previous_answers_str}

    ### **Output Format (STRICTLY FOLLOW THIS, NO EXTRA TEXT):**
    Question: <your generated question>  
    A) <Option 1>  
    B) <Option 2>  
    C) <Option 3>  
    D) <Option 4>  
    """)

    # Correctly format the prompt with actual values
    formatted_prompt = prompt_template.format(
        next_category=next_category, 
        previous_answers_str=previous_answers_str
    )

    # Invoke the LLM with the formatted string instead of a template object
    return llm.invoke(formatted_prompt)

def get_career_recommendations(history):
    """Queries ChromaDB for career matches using history with RAG-style retrieval."""
    if not history:
        return ["No history available to recommend careers."]

    # Extract just the answers from the history dictionary
    cleaned_answers = []
    for q, a in history.items():
        if a and ") " in a:
            cleaned_answers.append(a.split(") ", 1)[1])
        elif a:
            cleaned_answers.append(a)

    query_text = " ".join(cleaned_answers)

    # Retrieve top 3 documents relevant to the combined user answers
    results = collection.query(query_texts=[query_text], n_results=3)

    if not results or not results["documents"]:
        return ["No match found"]
    
    job_id = extract_job_ids(results["documents"])
    jobs = fetch_web_results(job_id)
    return jobs

def fetch_web_results(ids):
    final = []
    for i in ids:
        id = i[0]

        """Fetches the header and first <p> content from a given career page and returns as a string."""
        url = f"https://www.onetonline.org/link/details/{id}"
        print(url) # Checking if the URL is valid
        
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

        # Extract Technology Skills (first 5)
        tech_skills = []
        tech_skills_section = soup.find("div", class_="section_TechnologySkills")
        if tech_skills_section:
            skill_items = tech_skills_section.find_all("li", limit=5)
            for item in skill_items:
                skill_text = item.get_text(separator=" ", strip=True).replace("Related occupations", "").strip()
                tech_skills.append(skill_text)

        # Extract Skills (first 5)
        skills_section = soup.find("div", class_="section_Skills")
        skills = []
        if skills_section:
            rows = skills_section.find_all("tr", limit=5)
            for row in rows:
                skill_cell = row.find_all("td")
                if len(skill_cell) > 1:
                    skill_text = skill_cell[1].get_text(separator=" ", strip=True).replace("Related occupations", "").strip()
                    skills.append(skill_text)

        # Extract Knowledge (first 5)
        knowledge_section = soup.find("div", class_="section_Knowledge")
        knowledge = []
        if knowledge_section:
            rows = knowledge_section.find_all("tr", limit=5)
            for row in rows:
                knowledge_cell = row.find_all("td")
                if len(knowledge_cell) > 1:
                    knowledge_text = knowledge_cell[1].get_text(separator=" ", strip=True).replace("Related occupations", "").strip()
                    knowledge.append(knowledge_text)

        # Extract Median Wages and Projected Job Openings
        wages_section = soup.find("div", id="WagesEmployment")
        median_wages = "N/A"
        projected_openings = "N/A"
        if wages_section:
            dl_items = wages_section.find_all("dt")
            dd_items = wages_section.find_all("dd")
            for dt, dd in zip(dl_items, dd_items):
                label = dt.get_text(strip=True)
                value = dd.get_text(strip=True)
                if "Median wages" in label:
                    median_wages = value
                if "Projected job openings" in label:
                    projected_openings = value

        # Extract Related Occupations (first 3)
        related_occupations_section = soup.find("div", class_="section_RelatedOccupations")
        related_occupations = []
        if related_occupations_section:
            related_list = related_occupations_section.find_all("li", limit=3)
            for item in related_list:
                text = item.get_text(separator=" ", strip=True)
                text = re.sub(r'Bright Outlook', '', text).strip()
                text = re.sub(r'^\d{2}-\d{4}\.\d{2}\s*', '', text)  # Remove job codes like 25-1031.00
                related_occupations.append(text)

        # Remove job codes, "Bright Outlook", and "Updated YYYY"
        header = re.sub(r'\d{2}-\d{4}\.\d{2}', '', header)  # Remove job codes like 11-1021.00
        header = re.sub(r'(Bright Outlook|Updated \d{4})', '', header).strip()  # Remove "Bright Outlook" and "Updated YYYY"

        final.append({
            "title": header,
            "description": first_paragraph,
            "technology_skills": tech_skills if tech_skills else ["N/A"],
            "skills": skills if skills else ["N/A"],
            "knowledge": knowledge if knowledge else ["N/A"],
            "median_wages": median_wages,
            "projected_openings": projected_openings,
            "related_occupations": related_occupations if related_occupations else ["N/A"]
        })
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
    # global user_memory
    # for _ in range(5):  # Change to 20 for full experience
    #     question = generate_question(user_memory)
    #     print("\n", question)
        
    #     # Simulate user selecting an answer (in real use case, get input from user)
    #     user_response = input("Choose an option (A, B, C, D): ")
    #     user_memory.append(user_response)  # Store answer

    # # Get Career Recommendations
    # career_matches = get_career_recommendations(user_memory)
    # print("\n🎯 Recommended Careers:", extract_job_ids(career_matches))

# Run the program if executed directly
if __name__ == "__main__":
    run_career_advisor()