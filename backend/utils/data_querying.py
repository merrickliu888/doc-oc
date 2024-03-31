# Contains function to query index, database and interact with LLM (Gemini)


def chat(prompt, messages):
    """
    Chat with the Language Model
    """
    pass


def db_contains_repo(sb, repo_path):
    """
    Check if the repository is already indexed in the database
    """
    _, count = sb.table("github_repos").select("repo_path").eq('repo_path', repo_path).execute()
    return count > 0
    
