# user-stories-api
Ein FastAPI-basierter Dienst zum Klassifizieren von User Stories in die Bündelungsfächer SDM, GID und EVP.

## Installation & Start

1. Repository klonen
```bash
git clone 
```
2. Dependencies installieren
```bash
pip install -r ./src/backend/requirements.txt
```
3. (Optional) Umgebungsvariabeln für KI-Klassifizierung setzen.
```bash
export AI_API_URL="https://api.example.com/v1/chat/completions"
export AI_API_KEY="dein-api-key"
export AI_MODEL="qwen/qwen3-32b"
```
4. Starten:
```bash
pm2 start "npm run dev -- --host" --name "frontend" --cwd /var/www/user-story-api/src/frontend
pm2 start "/var/www/user-story-api/src/backend/venv/bin/uvicorn server:app --host 0.0.0.0 --port 8000" --name "backend" --cwd /var/www/user-story-api/src>
```

