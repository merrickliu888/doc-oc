# Contains functions to load a repository from github and get all the files in the repository

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
        elif item.type == 'file':
            try:
                decoded_content = item.decoded_content.decode()
            except Exception as e:
                print(f"Error decoding content of {item.name}: {e}")
                continue

            file = File(repo_path, item.name, item.path, decoded_content)
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
