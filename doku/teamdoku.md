# Teamdokumentation

## 1. Datenmodell und Mapping

Unser aktuelles Kerndatenmodell (`UserStory`) konzentriert sich auf die für die Klassifizierung zwingend notwendigen Felder. Im erweiterten Modell (für die Abschlusspräsentation) kommen zusätzliche Metadaten-Felder hinzu.

### Erweitertes Datenmodell

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
| `description` | `description` / `Beschreibung` | `body` / `description` | `<description>` | String, `.strip()` – Default: `""` |
| `id` | — | — | — | Auto-Inkrement via `next_id()` |
| `classification` | — | — | — | Keyword-Score → max(Fach) |

---

## 2. Fachzuordnung

Die Zuordnung zu den Fächern **SDM** (Software & Daten-Management), **GID** (Geschäfts- & Informations-Dienste) und **EVP** (Ereignis-, Verwaltungs- & Prozessmanagement) erfolgt zweistufig:

1. **KI-Klassifizierung (Primär)**: Wenn `AI_API_URL` und `AI_API_KEY` gesetzt sind, wird ein LLM mit einem strikten Prompt aufgerufen (`_AI_PROMPT` in `server.py`). Antwort muss exakt `SDM`, `GID` oder `EVP` sein.
2. **Keyword-Matching (Fallback)**: Ein lokales Wörterbuch (`_KEYWORDS`) zählt Treffer in Titel und Beschreibung. Das Fach mit den meisten Treffern gewinnt.

### Regelwerk V1 – SDM-Regeln

| Regel-ID | Auslöser (Keywords) | Begründung |
|----------|-------------------|-----------|
| R01 | `login`, `passwort`, `anmelden`, `abmelden`, `logout` | Authentifizierung ist Kern von Software-Sicherheit |
| R02 | `benutzer`, `nutzer`, `user`, `account`, `konto`, `profil` | Benutzerkonten-Management gehört zu Datenverwaltung |
| R03 | `rolle`, `berechtigung`, `rechte`, `zugang`, `session`, `token` | Zugriffskontrolle ist Software-Architektur |
| R04 | `registrierung`, `authentifizierung`, `sicherheit`, `security` | Direkte Verbindung zur System-Sicherheit |

### Regelwerk V1 – GID-Regeln

| Regel-ID | Auslöser (Keywords) | Begründung |
|----------|-------------------|-----------|
| R05 | `rechnung`, `bericht`, `report`, `export`, `import` | Berichterstattung und Datenexport sind Geschäftsdienste |
| R06 | `daten`, `data`, `analyse`, `statistik`, `dashboard`, `tabelle` | Datenanalyse als Geschäftsfunktion |
| R07 | `suche`, `filter`, `sortieren`, `liste`, `dokument`, `übersicht` | Informationsbeschaffung als Dienstleistung |
| R08 | `download`, `upload`, `diagramm`, `chart`, `visualisierung` | Datenvisualisierung als Geschäftsdienst |

### Regelwerk V1 – EVP-Regeln

| Regel-ID | Auslöser (Keywords) | Begründung |
|----------|-------------------|-----------|
| R09 | `workflow`, `prozess`, `genehmigung`, `genehmigen`, `anfrage` | Prozesssteuerung ist Kern von EVP |
| R10 | `aufgabe`, `task`, `termin`, `benachrichtigung`, `event` | Aufgaben- und Eventmanagement gehört zu EVP |
| R11 | `erinnerung`, `eskalation`, `kommentar`, `protokoll`, `log` | Verwaltungsprozesse mit Benachrichtigungen |
| R12 | `antrag`, `nachricht`, `message`, `email`, `e-mail`, `kalender` | Kommunikations-Workflow als Prozessschritt |

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
| **Rolle A** (Datenimport & Mapping) | Samuel W. | CSV/JSON/XML-Parsing in `server.py`, data-Mapping, Beispieldaten in `test/manual/` |
| **Rolle B** (Fachlogik & Regelwerk) | Nils B. | Keyword-Wörterbuch `_KEYWORDS`, KI-Prompt `_AI_PROMPT`, Klassifizierungs-Logik `classify()`, Architektur |
| **Rolle C** (API, Tests, Doku) | – | Nicht separat besetzt; Aufgaben auf Rolle A und B verteilt |

---

## 5. Herausforderungen und Lösungswege

### Heterogene Quelldaten
**Problem:** CSV, JSON und XML verwenden unterschiedliche Feldnamen für dasselbe Konzept (z. B. "title" vs. "Aufgabe").  
**Lösung:** Mapping-Tabelle als Design-Dokument vor der Implementierung erstellt. Im Code wird jeder Parser separat implementiert (`csv.DictReader`, `json.loads`, `xml.etree.ElementTree`), aber alle liefern das gleiche Format (`List[dict]` mit `title`/`description`).

### Fachzuordnung ohne KI
**Problem:** Ohne externe API muss die Klassifizierung komplett lokal funktionieren.  
**Lösung:** Keyword-basiertes Scoring-System: Jedes Fach bekommt ein Wortverzeichnis, jedes gefundene Keyword zählt +1. Das Fach mit der höchsten Punktzahl gewinnt. Bei Gleichstand greift die Reihenfolge SDM > GID > EVP als Tiebreaker.

### Fehlerhafte Eingabedaten
**Problem:** Ungültiges JSON/XML oder fehlende Titel-Felder können den Import zum Absturz bringen.  
**Lösung:** Try/Except um jeden Parser, gefilterte `skipped`-Einträge mit Fehlermeldungen in `ImportResult.errors`.
