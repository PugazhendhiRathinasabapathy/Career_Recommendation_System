from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.recommendation import generate_question, get_career_recommendations
from pydantic import BaseModel
from utils.logger import logger

app = FastAPI(
    title="Career Recommendation System",
    description="The Career Recommendation System is an AI-powered web application designed to assist individuals in making informed career decisions",
    version="1.0.0",
)

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


class UserResponse(BaseModel):
    selected_option: str


@app.get("/get-question")
async def get_question():
    """Returns the first or next dynamically generated career-related question."""
    question = generate_question(user_memory)
    logger.info(question)
    return {"question": question}


@app.post("/submit-answer")
async def submit_answer(response: UserResponse):
    logger.info(len(user_memory))
    """Stores user's response and returns the next question or career recommendation."""
    user_memory.append(response.selected_option)

    if len(user_memory) >= 20:  # After 20 questions, return recommendations
        careers = get_career_recommendations(user_memory)
        user_memory.clear()
        logger.info(user_memory)
        return {"message": "Career recommendations ready!", "careers": careers}

    next_question = generate_question(user_memory)
    return {"question": next_question}


# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn

    logger.info("FASTAPI APP IS RUNNING")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

