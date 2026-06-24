# user-story-api

Ein FastAPI-basierter Dienst zum Klassifizieren von User Stories in die Bündelungsfächer SDM, GID und EVP.

---

## Projektstruktur

```
user-story-api/
├── src/
│   ├── backend/
│   │   ├── server.py          # FastAPI-Anwendung (Endpunkte, Models, Logik)
│   │   └── requirements.txt   # Python-Dependencies
│   └── frontend/
│       ├── App.tsx            # Frontend-Komponente (React + TypeScript)
│       ├── App.css            # Styles
│       └── components/        # UI-Komponenten
├── test/
│   ├── unit/
│   │   └── api_test.py        # pytest-Tests für alle Endpunkte
│   └── manual/
│       ├── userstories.csv    # Beispiel-CSS-Datei
│       ├── userstories.json   # Beispiel-JSON-Datei
│       ├── userstories.xml    # Beispiel-XML-Datei
│       └── import_file.sh     # curl-Test-Skript
├── doku/
│   ├── abgabe_2026-06-24.md  # Abgabedokument Kernstand
│   ├── api.md                # API-Dokumentation
│   ├── teamdoku.md           # Technische Dokumentation & Regelwerk
│   ├── tests.md              # Testdokumentation
│   ├── teamlog.md            # Entwicklungsprotokoll
│   ├── vertretungsauftrag_10-06.md
│   ├── vertretungsauftrag_24-06.md
│   ├── praesentation_und_abschluss.md
│   └── reflexion_projektabschluss_lf8.md
├── README.md
├── pytest.ini
└── requirements.txt
```

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

Abhängigkeiten: `fastapi>=0.110`, `uvicorn>=0.29`, `pydantic>=2.6`, `python-multipart>=0.0.9`, `httpx>=0.28`

3. (Optional) Umgebungsvariabeln für KI-Klassifizierung setzen.

```bash
export AI_API_URL="https://api.example.com/v1/chat/completions"
export AI_API_KEY="dein-api-key"
export AI_MODEL="qwen/qwen3-32b"
```

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

---

## Tests

```bash
# Alle Tests
pytest test/unit/ -v
```

---

## Klassifizierungslogik

1. **KI-Methode:** Falls `AI_API_URL` und `AI_API_KEY` gesetzt sind → LLM mit striktem Prompt (`SDM|GID|EVP`)
2. **Keyword-Fallback:** 60+ Stichwörter pro Fach in Titel und Beschreibung zählen → höchster Score gewinnt

Details im [Regelwerk](doku/teamdoku.md#2-fachzuordnung).

---

## Bekannter Stand

### ✅ Funktioniert
- CSV/JSON/XML-Import über `/import`
- CRUD-Endpunkte für User Stories (`GET`, `PATCH`, `DELETE`)
- Fachfilterung nach SDM/GID/EVP
- Keyword-basierte Klassifizierung
- 11 Unit-Tests bestanden
- Swagger UI Dokumentation

### 🔧 In Arbeit / Fehlend
- PATCH-Bug: `/userstories/{id}/{fach}` gibt immer 404 zurück (sollte aktualisierte Story zurückgeben)
- KI-Klassifizierung nur mit externem API-Key funktional
- Frontend für interaktive Verwaltung

