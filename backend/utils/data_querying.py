# Contains function to query index, database and interact with LLM (Gemini)
from langchain_pinecone import PineconeVectorStore  
from langchain_cohere import ChatCohere, CohereEmbeddings
from langchain.schema import SystemMessage, HumanMessage, AIMessage

from dotenv import load_dotenv
import os
load_dotenv()
cohere_api_key = os.environ.get('COHERE_API_KEY')
pinecone_api_key = os.environ.get('PINECONE_API_KEY')

# Setting up chain
embeddings = CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=cohere_api_key)
llm = ChatCohere(model="command-r", temperature=0.25, streaming=True, cohere_api_key=cohere_api_key)

def augment_prompt(prompt, db_content):
    """
    Augment the prompt with the content from the database
    """
    augmented_prompt = "## Context:\n"
    for i in range(len(db_content)):
        content = db_content[i]
        augmented_prompt += f"File Name {i}: {content['name']}\n"
        augmented_prompt += f"File Path {i}: {content['path']}\n"
        augmented_prompt += f"File Content {i}: {content['content']}\n"
    augmented_prompt += "\n## Prompt (Answer the prompt below using the context provided above:\n"
    augmented_prompt += prompt

    return augmented_prompt

def chat(repo_path, prompt, messages, content_store, k=3):
    """
    Chat with the Language Model
    """
    # Retrieving content ids
    vectorstore = PineconeVectorStore(index_name="doc-oc", 
                                      embedding=embeddings, 
                                      text_key="db_id", 
                                      pinecone_api_key=pinecone_api_key, 
                                      namespace=repo_path)
    vector_content = vectorstore.similarity_search(prompt, k=k)
    
    # Retrieving the content from supabase
    content_ids = [int(c.page_content) for c in vector_content]
    db_content = content_store.table('files').select('name, path, content').in_('id', content_ids).execute().data

    # Chatting with the model
    augmented_prompt = augment_prompt(prompt, db_content)
    messages.append(HumanMessage(content=augmented_prompt))
    for chunk in llm.stream(messages):
        yield chunk.content


def db_contains_repo(sb, repo_path):
    """
    Check if the repository is already indexed in the database
    """
    res = sb.table('github_repos').select('repo_path').eq('repo_path', repo_path).execute()
    return len(res.data) > 0
