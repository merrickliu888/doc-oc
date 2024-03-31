# Embedding funtions for files and queries using the Cohere API

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

    return response.embedding[0]


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
            batch[i].embedding = response.embeddings[i]
