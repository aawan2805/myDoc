# DOCS-RAG
A personal project to retrieve personal information from documents (such as your own passport, official documents) that are pre-added to the database using embedding. It works the following way:

READ -> ADD -> ASK CHATBOT -> GET INFO

# WORKFLOW

# Libraries
This project uses:
- uv (packet manager)
- Postgres (vector extension)
- FastAPI (to upload documents to parse them and add them into the database and query)
- Celery to process large files in background that are meant to be added into the database
