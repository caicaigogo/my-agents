# python -m venv venv
# source venv/bin/activate
# pip install -e .
# OLLAMA_HOST=0.0.0.0 ollama serve
uvicorn app.api.main:app --host 0.0.0.0 --port 8000