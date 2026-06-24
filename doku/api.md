# API Dokumentation

Die API bietet Endpunkte zum Verwalten und Importieren von User Stories.
Interaktive Dokumentation via Swagger UI: `http://localhost:8000/docs`

## Datenmodelle

### UserStory
| Feld | Typ | Beschreibung |
|---|---|---|
| id | int | Eindeutige, auto-inkrementelle ID |
| title | string | Titel der User Story |
| description | string | Beschreibung der User Story |
| classification | string (Enum) | `SDM`, `GID` oder `EVP` |

### ImportResult
| Feld | Typ | Beschreibung |
|---|---|---|
| imported | int | Anzahl erfolgreich importierter Stories |
| skipped | int | Anzahl übersprungener Stories (z.B. wegen fehlendem Titel) |
| errors | array of strings | Liste der Fehlermeldungen |
| stories | array of UserStory | Liste der neu importierten Stories |

### Fach
Enum (SDM/GID/EVP)

## Endpunkte

### 1. User Stories abrufen
- **GET** `/userstories` – Gibt alle gespeicherten User Stories zurück.
- **GET** `/userstories/{story_id}` – Gibt eine spezifische User Story zurück.
- **GET** `/userstories/fach/{fach_str}` – Filtert User Stories nach Bündelungsfach (`SDM`, `GID`, `EVP`).

### 2. User Stories manipulieren
- **PATCH** `/userstories/{story_id}/{fach_str}` – Ändert die Klassifizierung einer bestehenden User Story manuell.
- **DELETE** `/userstories/{story_id}` – Löscht eine User Story aus dem System.

### 3. Datenimport
- **POST** `/import`
  - **Beschreibung**: Importiert User Stories aus einer hochgeladenen Datei.
  - **Content-Type**: `multipart/form-data`
  - **Parameter**: `file` (UploadFile) - Erlaubte Endungen: `.csv`, `.json`, `.xml`.
  - **Fehlercodes**: `400 Bad Request` (ungültiges JSON/XML), `415 Unsupported Media Type` (falsches Dateiformat).