# Frontend starten (Vite braucht hier oft das -- --host, damit es erreichbar ist)
pm2 start "npm run dev -- --host" --name "frontend" --cwd /var/www/user-story-api/src/frontend

# Backend starten
pm2 start "/var/www/user-story-api/src/backend/venv/bin/uvicorn server:app --host 0.0.0.0 --port 8000" --name "backend" --cwd /var/www/user-story-api/src/backend