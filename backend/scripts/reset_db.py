# Scripts to reset databases

from pinecone import Pinecone
from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

def reset_pinecone():
    """
    Reset the Pinecone index
    """
    pinecone_api_key = os.environ.get('PINECONE_API_KEY')
    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index("doc-oc")
    name_spaces = index.describe_index_stats()['namespaces']
    for ns in name_spaces:
        index.delete(namespace=ns, delete_all=True)

def reset_supabase():
    """
    Reset the Supabase database
    """
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_API_KEY')
    sb = create_client(supabase_url, supabase_key)
    sb.table('github_repos').delete().gte('id', -1).execute()
    sb.table('files').delete().gte('id', -1).execute()

if __name__ == "__main__":
    reset_pinecone()
    reset_supabase()
