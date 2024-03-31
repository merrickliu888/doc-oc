from pydantic import BaseModel

class GithubRequest(BaseModel):
    repo_path: str

class ChatRequest(BaseModel):
    prompt: str
    messages: list