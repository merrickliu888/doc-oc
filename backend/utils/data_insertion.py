# Functions to upsert data into Pinecone and Supabase

def upsert_files(pc, index, sb, files):
    """
    Upsert a list of files to the Pinecone index and Supbase
    """
    # Supabase
    res, _ = sb.table('github_repos').upsert({'repo_path': files[0].repo_path}).execute()
    repo_id = res[1][0]['id']
    res, _ = sb.table('files').upsert(
        [{'repo_id': repo_id, 'name': file.name, 'path': file.path, 'content': file.content, 'embedding': file.embedding} for file in files]
    ).execute()

    # Pinecone
    index = pc.Index(index)
    vector_data = []
    for i in range(len(files)):
        vector_data.append({
            'id': str(res[1][i]['id']),
            'values': files[i].embedding,
            'metadata': {
                'name': files[i].name,
                'path': files[i].path
            }
        })

    index.upsert(
        vectors=vector_data,
        namespace=files[0].repo_path
    )
