# doc-oc

Talk to your codebase.

### How to run:

To run backend:

1. Use pip to install pipenv, the package manager for the backend: `pip install pipenv`
2. Run `pipenv install` to install dependencies
3. Get api keys for `Cohere`, `Pinecone`, `Github`, and `Supabase` (key and url) and put them into a `.env` file.
4. Run `run.py` script to start server. You can also type `uvicorn main:app --reload --port 8000` in the terminal.

To run frontend:

1. Run `npm install` to install dependencies.
2. In the terminal, type `npm run dev` to run in dev mode or run `npm run build` and `npm run start` to run in production mode.

### Database Setup

-   Pinecone - Create a pinecone index called "doc-oc" with dimensions as 1024.
-   Supabase - Create two tables:

    -   `github_repos` - Stores all the index repos

        -   Columns: `id` (PK, int8), `repo_path` (varchar)

    -   `files` - Stores data related to files

        -   Columns: `id` (PK, int8), `repo_id` (FK, int8), `name` (varchar), `path` (varchar), `content` (text), `embedding` (float8[])
