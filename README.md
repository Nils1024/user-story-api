# user-stories-api
Ein FastAPI-basierter Dienst zum Klassifizieren von User Stories in die Bündelungsfächer SDM, GID und EVP.

## Installation & Start

1. Repository klonen
```bash
git clone https://github.com/Nils1024/user-story-api.git
cd user-stories-api
```
2. Dependencies installieren
```bash
pip install -r ./src/backend/requirements.txt
cd ./src/frontend
npm install
cd ../..
```
3. (Optional) Umgebungsvariabeln für KI-Klassifizierung setzen.
```bash
export AI_API_URL="https://api.example.com/v1/chat/completions"
export AI_API_KEY="dein-api-key"
export AI_MODEL="qwen/qwen3-32b"
```
4. Backend starten:
```bash
cd src/backend
uvicorn server:app --reload
```
5. (Optional) Frontend starten:
```bash
cd src/frontend
npm run dev
```
> [!Info]
> npm run dev ist nicht für richtiges deployment empfohlen.
