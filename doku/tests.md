# Tests

## Test-Übersicht

Alle Tests befinden sich in [`test/unit/api_test.py`](../test/unit/api_test.py) und verwenden **pytest** mit FastAPIs `TestClient`. Jeder Test resetet den globalen Zustand (`user_stories.clear()`) vor dem Start.

---

## Testfälle

| Test-ID | Was wird geprüft? | Erwartet | Ergebnis | Bestanden |
|---------|-------------------|----------|----------|-----------|
| T01 | `GET /userstories` – Alle Stories abrufen | Status 200, Array mit mind. 1 Eintrag | 200, Array mit Seed-Daten | ✅ Ja |
| T02 | `GET /userstories/{id}` – Existierende ID abfragen | Status 200, korrekte Story zurück | 200, id=1 | ✅ Ja |
| T03 | `GET /userstories/{id}` – Nicht existierende ID | Status 404, Detail-Meldung | 404, "nicht gefunden" | ✅ Ja |
| T04 | `GET /userstories/fach/SDM` – Gültiges Fach | Status 200, gefiltertes Ergebnis | 200, 1 Treffer | ✅ Ja |
| T05 | `GET /userstories/fach/XYZ` – Ungültiges Fach | Status 400, Detail-Meldung | 400, "Unbekanntes Fach" | ✅ Ja |
| T06 | `DELETE /userstories/{id}` – Existierende Story löschen | Status 204, danach 404 auf GET | 204, dann 404 | ✅ Ja |
| T07 | `PATCH /userstories/{id}/EVP` – Klassifizierung ändern | Status 200, veränderte Story | Status 200, Fach = EVP | ✅ Ja |
| T08 | `POST /import` mit CSV | Status 200, imported=Anzahl Zeilen | 200, imported=2 | ✅ Ja |
| T09 | `POST /import` mit JSON | Status 200, imported=Array-Größe | 200, imported=2 | ✅ Ja |
| T10 | `POST /import` mit XML | Status 200, imports alle `<user_story>`-Elemente | 200, imported=2 | ✅ Ja |
| T11 | `POST /import` mit ungültigem Format (.txt) | Status 415, Unsupported Media Type | 415 | ✅ Ja |

---

## Tests ausführen

```bash
pytest test/unit/ -v
```

---

## Bekannte Test-Lücken

| Lücke | Beschreibung | Priorität |
|-------|-------------|-----------|
| Edge Cases für Import | Kein Test für leere Dateien, sehr große Dateien, Sonderzeichen in Titeln | Niedrig |

---

## Manuelle Tests

In [`test/manual/`](../test/manual/) befinden sich manuelle Test-Dateien:

| Datei | Zweck |
|-------|-------|
| `userstories.csv` | CSV-Eingabe zum Testen von `/import` |
| `userstories.json` | JSON-Eingabe zum Testen von `/import` |
| `userstories.xml` | XML-Eingabe zum Testen von `/import` |
| `import_file.sh` | Shell-Skript für curl-Testaufrufe |

### Manueller Test mit curl

```bash
# CSV importieren
curl -F "file=@test/manual/userstories.csv" http://localhost:8000/import

# Alle Stories abfragen
curl http://localhost:8000/userstories

# Nach Fach filtern
curl http://localhost:8000/userstories/fach/SDM
```
