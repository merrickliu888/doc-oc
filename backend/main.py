from dotenv import load_dotenv
from request_body import GithubRequest, ChatRequest
from utils.github_contents import load_repo, get_files
from utils.embedding import embed_files
from utils.data_insertion import upsert_files
from utils.data_querying import chat

import os
import fastapi
from pinecone import Pinecone
from cohere import Client
from github import Github
from supabase import create_client

# Loading the .env file
load_dotenv()
cohere_api_key = os.environ.get('COHERE_API_KEY')
github_token = os.environ.get('GITHUB_TOKEN')
pinecone_api_key = os.environ.get('PINECONE_API_KEY')
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_API_KEY')

# Creating a FastAPI app and initializing api clients
app = fastapi.FastAPI()
co = Client(cohere_api_key)
ghub = Github(github_token)
pc = Pinecone(api_key=pinecone_api_key)
sb = create_client(supabase_url, supabase_key)


# Post Request for indexing github repo
@app.post("/api/index")
async def index_github_repo(body: GithubRequest):
    """
    Index a github repository
    """
    try:
        # Retrieving files from the repository
        repo = load_repo(ghub, body.repo_path)
        files = get_files(body.repo_path, repo, "")

        # Embedding the files
        embed_files(co, files)

        # Upserting the files
        upsert_files(pc, "doc-oc", sb, files)

        return {"message": "Indexing successful"}
    except Exception as e:
        return {"message": str(e)}
    
# Post request for chatting with LLM
@app.post("/api/chat")
async def chat_with_llm(body: ChatRequest):
    """
    Chat with the Language Model
    """
    prompt = body.prompt
    messages = body.messages
    try:
        chat(prompt, messages)
        return {"message": "Chat successful"}
    except Exception as e:
        return {"message": str(e)} 
