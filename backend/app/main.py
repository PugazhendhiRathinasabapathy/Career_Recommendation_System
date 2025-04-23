from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from models.recommendation import  get_career_recommendations, gen_questions_langchain

app = FastAPI()

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Store user responses in memory
user_memory = []
history = {}

class UserResponse(BaseModel):
    question: str
    selected_option: str

@app.get("/")
def root():
    return {"message": "Welcome to CareerPathAI 🚀"}

@app.get("/get-question/")
async def get_question():
    """Returns the first or next dynamically generated career-related question."""
    #question = generate_question(user_memory)
    question = gen_questions_langchain(history)
    print(question)
    return {"question": question}

@app.post("/submit-answer/")
async def submit_answer(response: UserResponse):
    print(len(history))
    """Stores user's response and returns the next question or career recommendation."""
    user_memory.append(response.selected_option)
    history[response.question] = response.selected_option

    if len(history) >= 20:  # After 20 questions, return recommendations
        careers = get_career_recommendations(history)
        user_memory.clear()
        print("*" * 50 + " Before clearing history:", history)
        history.clear()
        print("After clearing history:", history)
        return {"message": "Career recommendations ready!", "careers": careers}

    #next_question = generate_question(user_memory)
    next_question = gen_questions_langchain(history)
    return {"question": next_question}

# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)