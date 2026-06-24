# user-story-api

Ein FastAPI-basierter Dienst zum Klassifizieren von User Stories in die Bündelungsfächer SDM, GID und EVP.

Um das Projekt so schnell wie möglich nutzen zu können, verweisen wir auf die Website, wo wir das Projekt selber hosten:  

[user-story-api.saviwie.com](user-story-api.saviwie.com)

---

## Teammitglieder und Rollen

| Rolle | Name(n) | Schwerpunktaufgaben |
|-------|---------|-------------------|
| **Rolle A** (Datenimport & Mapping) | Samuel W. | Frontend |
| **Rolle B** (Fachlogik & Regelwerk) | Nils B. | Backend |
| **Rolle C** (API, Tests, Doku) | – | Nicht separat besetzt; Aufgaben verteilt |

---

## Installation & Start

1. Repository klonen
```bash
git clone https://github.com/Nils1024/user-story-api.git
cd user-stories-api
```
2. Dependencies installieren
```bash
pip install -r src/backend/requirements.txt
```

Python: 3.14.3
Abhängigkeiten: `fastapi>=0.110`, `uvicorn>=0.29`, `pydantic>=2.6`, `python-multipart>=0.0.9`, `httpx>=0.28`
npm: 11.4.1
node: 22.16.0

3. (Optional) Umgebungsvariabeln für KI-Klassifizierung setzen.

```bash
export AI_API_URL="https://api.example.com/v1/chat/completions"
export AI_API_KEY="dein-api-key"
export AI_MODEL="qwen/qwen3-32b"
```
> [!NOTE]
> Ohne diese Umgebungsvariablen funktioniert die Klassifizierung ausschließlich über das Keyword-Regelwerk.

4. Backend starten

```bash
cd src/backend
uvicorn server:app --reload
```

Die API ist dann unter `http://localhost:8000` erreichbar. Die Swagger-Dokumentation unter `http://localhost:8000/docs`.

5. (Optional) Frontend starten

```bash
cd src/frontend
npm install
npm run dev
```
> [!NOTE]
> `npm run dev` ist nicht für Produktionseinsatz empfohlen.

---

## API-Quickstart

```bash
# Alle Stories abrufen
curl http://localhost:8000/userstories

# CSV importieren
curl -F "file=@test/manual/userstories.csv" http://localhost:8000/import

# Nach Fach filtern
curl http://localhost:8000/userstories/fach/SDM
```

## Bekannter Stand

### ✅ Funktioniert
- Import
- Manipulation von User Stories
- Frontend

### 🔧 In Arbeit / Fehlend
- Präsentation
- Swagger UI muss noch erweitert werden
- Mehr Tests

