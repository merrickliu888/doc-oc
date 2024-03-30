def batch_list(lst, batch_size):
    """
    Batch a list into smaller lists of size batch_size
    """
    for i in range(0, len(lst), batch_size):
        yield lst[i:i + batch_size]


def embed_query(cohere_client, query):
    """
    Embed a query using the Cohere API
    """
    response = cohere_client.embed(
        texts=[query],
        model='embed-english-v3.0',
        input_type='search_query'
    )

    return response.embeddings[0]


def embed_files(cohere_client, files, batch_size=10):
    """
    Embed a list of files using the Cohere API

    Mutates file attribute
    """
    for batch in batch_list(files, batch_size):
        response = cohere_client.embed(
            texts=[file.content for file in batch],
            model='embed-english-v3.0',
            input_type='search_query'
        )   

        for i in range(len(batch)):
            batch[i].embeddings = response.embeddings[i]


if __name__ == '__main__':
    class File:
        """
        A class to represent a file in a repository
        """
        def __init__(self, repo_name, name, path, content):
            self.repo_name = repo_name
            self.name = name
            self.path = path
            self.content = content
            self.embeddings = None

    # Loading env variables
    from dotenv import load_dotenv
    import os
    load_dotenv()
    cohere_api_key = os.environ.get('COHERE_API_KEY')

    # Creating a Cohere client
    import cohere
    co = cohere.Client(cohere_api_key)

    # Testing embedding
    files = [
        File("repo", "file1", "path1", "content1"),
        File("repo", "file2", "path2", "content2"),
        File("repo", "file3", "path3", "content3"),
    ]

    embed_files(co, files)
    for f in files:
        print(f.embeddings)
        print("----------------------------------------------------")
