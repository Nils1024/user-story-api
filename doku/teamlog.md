# Teamlog – Entwicklungsprotokoll

## Übersicht

Dieses Protokoll dokumentiert, was wann von wem bearbeitet wurde.

---

## Entwicklungstagebuch

| Datum | Wer | Was wurde gemacht? | Offene Punkte | Nächster Schritt |
|-------|-----|-------------------|--------------|-----------------|
| 27.05. | Nils B., Samuel W. | Projektstart: Team gebildet, Quellen (CSV, JSON, XML) ausgewählt, erste Modell-Idee skizziert | Datenmodell verfeinern | Mapping-Tabelle fertigstellen |
| 03.06. | Nils B. | Server.py Basis mit FastAPI aufgesetzt, UserStory/ImportResult Models definiert, Keyword-Regelwerk `_KEYWORDS` erstellt | KI-API-Integration fehlt | KI-Prompt implementieren |
| 03.06. | Samuel W. | GET `/userstories`, GET `/userstories/{id}`, DELETE `/userstories/{id}` Endpunkte implementiert | PATCH und POST /import fehlen | REST-Vollständigkeit herstellen |
| 10.06. | Nils B. | Mapping-Tabelle fertig, Regelwerk V1 dokumentiert (R01–R12), API-Skizze erstellt | XML-Parsing fehlt | CSV+JSON+XML import |
| 10.06. | Samuel W. | POST `/import` für alle drei Formate implementiert, API-Skizze vervollständigt | Tests fehlen | curl-Tests + Unit-Tests |
| 17.06. | Nils B. | KI-Klassifizierung mit `classify_ai()` und `_AI_PROMPT`, httpx-Integration, CORS-Middleware | Edge Cases im Import | Fehlerbehandlung verbessern |
| 17.06. | Samuel W. | Unit-Tests in `test/unit/api_test.py` (11 Tests), curl-Manual-Test-Skript erstellt | Patch-Bug bleibt offen | PATCH fixen + Test abdecken |
| 24.06. | Nils B. | Dokumentation vervollständigt: teamdoku.md mit Regelwerk, Abgabedokument erstellt | PATCH-Bug nicht gefixt | Bugfix für nächste Woche |
| 24.06. | Samuel W. | API-Dokumentation erweitert, Tests.md erstellt, Reflexionsvorlage vorbereitet | Frontend fehlt | Demo-Vorbereitung |

---

## Offene Punkte

| Nr. | Punkt | Verantwortlich | Priorität |
|-----|-------|---------------|-----------|
| 1 | API-Dokumentation in Swagger erweitern | Team | Niedrig |
| 2 | Mehr Tests schreiben | Team | Niedrig |
| 3 | Präsentation machen | Team | Hoch |

---

## Nächste Schritte

1. Präsentation machen
2. API-Dokumentation in Swagger erweitern
3. Mehr Tests schreiben
