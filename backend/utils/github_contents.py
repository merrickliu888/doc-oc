def load_repo(g, repo_path):
    """
    Load a repository from github
    """ 
    repo = g.get_repo(repo_path)
    return repo

def get_files(repo_path, repo, path):
    contents = repo.get_contents(path)
    files = []  # List of file objects

    for item in contents:
        if item.type == "dir":
            files.extend(get_files(repo_path, repo, f"{path}/{item.name}"))
        else:
            file = File(repo_path, item.name, item.path, item.decoded_content.decode())
            files.append(file)
    
    return files

class File:
    """
    A class to represent a file in a repository
    """
    def __init__(self, repo_path, name, path, content):
        self.repo_path = repo_path
        self.name = name
        self.path = path
        self.content = content
        self.embedding = None

# if __name__ == '__main__':
#     # Loading env variables
#     from dotenv import load_dotenv
#     load_dotenv()
#     import os
#     from github import Github
#     github_token = os.environ.get('GITHUB_TOKEN')
#     g = Github(github_token)

#     repo = load_repo(g, "merrickliu888/doc-oc")
#     files = get_files("merrickliu888/doc-oc", repo, "")
#     for file in files:
#         print(file.content)
#         print("----------------------------------------------------")
