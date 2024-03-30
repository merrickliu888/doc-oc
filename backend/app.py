from dotenv import load_dotenv
import os
import fastapi

# Loading the .env file
load_dotenv()

# Creating a FastAPI app
app = fastapi.FastAPI()

# Post Request for indexing github repo
@app.post("/index-github-repo")
async def index_github_repo(repo_path: str):
    """
    Index a github repository
    """
    pass

# Post request for chatting with LLM
@app.post("/chat")
async def chat_with_llm(message: str):
    """
    Chat with the Language Model
    """
    pass