from github import Github
from dotenv import load_dotenv
import os

load_dotenv()
github_token = os.environ.get('GITHUB_TOKEN')


def load_repo(repo_path):
    """
    Load a repository from github
    """
    g = Github(github_token)
    repo = g.get_repo(repo_path)
    return repo

def get_files(repo, path):
    contents = repo.get_contents(path)
    files = []  # List of file objects

    for item in contents:
        if item.type == "dir":
            files.extend(get_files(repo, f"{path}/{item.name}"))
        else:
            file = File(repo.name, item.name, item.path, item.decoded_content)
            files.append(file)
    
    return files

class File:
    """
    A class to represent a file in a repository
    """
    def __init__(self, repo_name, name, path, content):
        self.repo_name = repo_name
        self.name = name
        self.path = path
        self.content = content

if __name__ == '__main__':
    repo = load_repo("merrickliu888/doc-oc")
    files = get_files(repo, "")
    for file in files:
        print(file.content)
    # print(files)
