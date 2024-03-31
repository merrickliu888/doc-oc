from pydantic import BaseModel

class GithubRequest(BaseModel):
    repo_path: str

class ChatRequest(BaseModel):
    repo_path: str
    prompt: str
    messages: list