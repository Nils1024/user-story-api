# Teamdokumentation

## 1. Datenmodell und Mapping

Unser aktuelles Kerndatenmodell (`UserStory`) konzentriert sich auf die für die Klassifizierung zwingend notwendigen Felder.

### Datenmodell (UserStory)

| Feld | Datentyp | Pflicht | Beschreibung |
|------|----------|---------|-------------|
| `id` | int | ja | Eindeutige, auto-inkrementelle ID (intern via `next_id()`) |
| `title` | string | ja | Kurztitel der User Story |
| `description` | string | nein | Ausführlichere Beschreibung |
| `classification` | Enum (SDM/GID/EVP) | nein | Zugewiesenes Bündelungsfach |

### Mapping-Tabelle

| Zielfeld (Modell) | Quelle A (CSV) | Quelle B (JSON) | Quelle C (XML) | Transformation |
|---|---|---|---|---|
| `title` | `title` | `title` | `<title>` | Wird 1:1 übernommen |
| `description` | `description` | `description` | `<description>` | Wird 1:1 übernommen |
| `id` | — | — | — | Auto-Inkrement via `next_id()` |
| `classification` | — | — | — | Keyword-Score → max(Fach) oder KI |

---

## 2. Fachzuordnung

Die Zuordnung zu den Fächern **SDM**, **GID** und **EVP** erfolgt über eine der folgenden Regeln:

1. **KI-Klassifizierung (Primär)**: Wenn `AI_API_URL` und `AI_API_KEY` gesetzt sind, wird ein LLM mit einem strikten Prompt aufgerufen (`_AI_PROMPT` in `server.py`). Antwort muss exakt `SDM`, `GID` oder `EVP` sein.
2. **Keyword-Matching (Fallback)**: Ein lokales Wörterbuch (`_KEYWORDS`) zählt Treffer in Titel und Beschreibung. Das Fach mit den meisten Treffern gewinnt.

### Regelwerk

| Regel-ID | Fach | Auslöser (Keywords) | Begründung |
|----------|------|---------------------|-----------|
| R1 | **SDM** | `login`, `passwort`, `anmelden`, `abmelden`, `logout`, `benutzer`, `nutzer`, `user`, `account`, `konto`, `profil`, `rolle`, `berechtigung`, `rechte`, `zugang`, `session`, `token`, `registrierung`, `authentifizierung`, `sicherheit`, `security` | Authentifizierung, Benutzerkonten und Zugriffskontrolle gehören zu Software & Daten-Management |
| R2 | **GID** | `rechnung`, `bericht`, `report`, `export`, `import`, `daten`, `data`, `analyse`, `statistik`, `dashboard`, `tabelle`, `suche`, `filter`, `sortieren`, `liste`, `dokument`, `übersicht`, `download`, `upload`, `diagramm`, `chart`, `visualisierung` | Berichterstattung, Datenanalyse und Informationsbeschaffung sind Geschäfts- & Informations-Dienste |
| R3 | **EVP** | `workflow`, `prozess`, `genehmigung`, `genehmigen`, `anfrage`, `aufgabe`, `task`, `termin`, `benachrichtigung`, `event`, `erinnerung`, `eskalation`, `kommentar`, `protokoll`, `log`, `antrag`, `nachricht`, `message`, `email`, `e-mail`, `kalender` | Prozesssteuerung, Aufgabenmanagement und Kommunikations-Workflows gehören zu Ereignis-, Verwaltungs- & Prozessmanagement |
| R4 | **SDM, GID oder EVP** | Wenn `AI_API_URL` und `AI_API_KEY` gesetzt sind: LLM mit striktem Prompt klassifiziert; sonst Keyword-Score (max(Fach) gewinnt) | - |

### Grenzfälle

**Grenzfall 1:** *"Als Manager möchte ich eine Benachrichtigung erhalten, wenn ein Bericht bereitsteht."*  
→ **Entscheidung: GID (primär)**. Kontext "Bericht" dominiert. Die Benachrichtigung ist hier sekundär – sie begleitet den Datenexport.

**Grenzfall 2:** *"Als Entwickler möchte ich ein Logging-System für alle API-Aufrufe implementieren."*  
→ **Entscheidung: SDM**. Das Keyword "logging" ist im SDM-Wörterbuch enthalten. Es geht um technische Systemarchitektur, nicht um einen Geschäftsdienst.

**Fallback (aus Teamabgabe):** Wenn kein Schlüsselwort in Titel oder Beschreibung gefunden wird → Standardzuordnung zu **SDM**, da die App primär als Softwareprodukt konzipiert ist.

---

## 3. Architektur

Das System besteht aus zwei Bestandteilen:

1. **Backend** (`src/backend/server.py`): FastAPI-Dienst, der Dateien über den `POST /import`-Endpunkt entgegennimmt und ins interne Format bringt.
2. **Frontend** (`src/frontend/`): React-Anwendung zum interaktiven Darstellen der User Stories.

### Datenfluss

```
Datei (CSV/JSON/XML) → POST /import → internes Format (UserStory) → KI (falls URL+Key gesetzt) oder Keyword-Regelwerk → Fachzuordnung (SDM/GID/EVP)
```

---

## 4. Rollen und Aufgabenverteilung

| Rolle | Name(n) | Schwerpunktaufgaben |
|-------|---------|-------------------|
| **Rolle A** (Datenimport & Mapping) | Samuel W. | Frontend |
| **Rolle B** (Fachlogik & Regelwerk) | Nils B. | Backend |
| **Rolle C** (API, Tests, Doku) | – | Nicht separat besetzt; Aufgaben auf Rolle A und B verteilt |

---

## 5. Herausforderungen und Lösungswege

### Fachzuordnung ohne KI
**Problem:** Ohne externe API muss die Klassifizierung komplett lokal funktionieren.  
**Lösung:** Keyword-basiertes Scoring-System: Jedes Fach bekommt ein Wortverzeichnis, jedes gefundene Keyword zählt +1. Das Fach mit der höchsten Punktzahl gewinnt. Bei Gleichstand greift die Reihenfolge SDM > GID > EVP als Tiebreaker.

### Fehlerhafte Eingabedaten
**Problem:** Ungültiges JSON/XML oder fehlende Titel-Felder können den Import zum Absturz bringen.  
**Lösung:** Try/Except um jeden Parser, gefilterte `skipped`-Einträge mit Fehlermeldungen in `ImportResult.errors`.
