# python -m venv venv
# source venv/bin/activate
# pip install -e .
# pip install -e ".[search]"
# pip install -e ".[memory]"
# pip install -e ".[all]"
# OLLAMA_HOST=0.0.0.0 ollama serve
uvicorn app.api.main:app --host 0.0.0.0 --port 8000