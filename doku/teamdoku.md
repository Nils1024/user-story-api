# Teamdokumentation

## 1. Datenmodell und Mapping
Unser aktuelles Kerndatenmodell (`UserStory`) konzentriert sich auf die für die Klassifizierung zwingend notwendigen Felder.

### Mapping-Tabelle
| Zielfeld (Modell) | Quelle A (CSV) | Quelle B (JSON) | Quelle C (XML) | Transformation |
|---|---|---|---|---|
| `title` | `title` / `Aufgabe` | `title` | `<title>` | String, Trim |
| `description` | `description` / `Beschreibung` | `body` / `description` | `<description>` | String, Trim |
| `id` | - | - | - | Auto-Inkrement (intern via `next_id()`) |
| `classification` | - | - | - | Berechnet via KI oder Keyword-Regelwerk |

*Hinweis: Das erweiterte Datenmodell für die Abschlusspräsentation umfasst zusätzlich Felder wie `quelle`, `priorität`, `status` etc., die im aktuellen MVP-Kern noch nicht persistiert werden.*

## 2. Fachzuordnung
Die Zuordnung zu den Fächern SDM (Software & Daten-Management), GID (Geschäfts- & Informations-Dienste) und EVP (Ereignis-, Verwaltungs- & Prozessmanagement) erfolgt zweistufig:

1. **KI-Klassifizierung (Primär)**: Wenn `AI_API_URL` und `AI_API_KEY` gesetzt sind, wird ein LLM mit einem strikten Prompt aufgerufen.
2. **Keyword-Matching (Fallback)**: Ein lokales Wörterbuch (`_KEYWORDS`) zählt Treffer in Titel und Beschreibung. Das Fach mit den meisten Treffern gewinnt.
