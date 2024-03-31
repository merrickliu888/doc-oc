# Contains functions to load a repository from github and get all the files in the repository

ignored_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico']

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
            if any(item.name.endswith(ext) for ext in ignored_extensions):
                continue
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
