#source venv/bin/activate
nohup env OLLAMA_HOST=0.0.0.0 ollama serve > ollama.log 2>&1 &
nohup uvicorn app.api.main:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &
