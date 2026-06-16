import json
import csv
import io
import os
import xml.etree.ElementTree as ET
import httpx
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
from enum import Enum

app = FastAPI(title="User Story Service", version="1.0.0")

AI_URL:   str | None = os.getenv("AI_API_URL")
AI_KEY:   str | None = os.getenv("AI_API_KEY")
AI_MODEL: str        = os.getenv("AI_MODEL", "qwen/qwen3-32b")

_AI_PROMPT = """\
Klassifiziere die folgende User Story in genau eines der drei Bündelungsfächer \
und antworte ausschließlich mit dem Kürzel – ohne Erklärung, ohne Leerzeichen, \
ohne Satzzeichen.

Fächer:
  SDM – Software & Daten-Management
        (Login, Passwort, Authentifizierung, Benutzer, Rollen, Berechtigungen, Session, Token)
  GID – Geschäfts- & Informations-Dienste
        (Berichte, Export, Datenanalyse, Dashboards, Dokumente, Suche, Filter, Tabellen)
  EVP – Ereignis-, Verwaltungs- & Prozessmanagement
        (Workflows, Benachrichtigungen, Genehmigungen, Prozesse, Tickets, Aufgaben, Termine)

Titel: {title}
Beschreibung: {description}

Antworte nur mit: SDM, GID oder EVP"""


class Fach(str, Enum):
    SDM = "SDM"
    GID = "GID"
    EVP = "EVP"


class UserStory(BaseModel):
    id: int
    title: str
    description: str
    classification: Fach


class ImportResult(BaseModel):
    imported: int
    skipped: int
    errors: List[str]
    stories: List[UserStory]


user_stories: List[UserStory] = [
    UserStory(
        id=1,
        title="Login",
        description="Als Benutzer möchte ich mich anmelden.",
        classification=Fach.SDM,
    )
]

_KEYWORDS: dict[Fach, list[str]] = {
    Fach.SDM: [
        "login", "passwort", "password", "anmelden", "abmelden", "logout",
        "benutzer", "nutzer", "user", "account", "konto", "profil", "profile",
        "registrierung", "registrieren", "authentifizierung", "authentifizieren",
        "rolle", "berechtigung", "rechte", "zugang", "session", "token",
        "sicherheit", "security", "passwort ändern", "zwei-faktor",
    ],
    Fach.GID: [
        "rechnung", "invoice", "bericht", "report", "export", "import",
        "daten", "data", "analyse", "analysieren", "statistik", "dashboard",
        "auswertung", "auswerten", "dokument", "liste", "übersicht",
        "suche", "suchen", "filter", "filtern", "sortieren", "tabelle",
        "diagramm", "chart", "visualisierung", "download", "upload",
    ],
    Fach.EVP: [
        "benachrichtigung", "benachrichtigen", "ereignis", "event",
        "workflow", "prozess", "genehmigung", "genehmigen", "anfrage",
        "antrag", "status", "ticket", "aufgabe", "task", "termin",
        "erinnerung", "eskalation", "kommentar", "protokoll", "log",
        "nachricht", "message", "email", "e-mail", "kalender",
    ],
}


def classify_keyword(title: str, description: str) -> Fach:
    text = f"{title} {description}".lower()
    scores = {f: sum(1 for kw in kws if kw in text) for f, kws in _KEYWORDS.items()}
    return max(scores, key=lambda f: scores[f])


async def classify_ai(title: str, description: str) -> Fach | None:
    if not AI_URL or not AI_KEY:
        return None
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                AI_URL,
                headers={"Authorization": f"Bearer {AI_KEY}", "Content-Type": "application/json"},
                json={
                    "model": AI_MODEL,
                    "messages": [{"role": "user", "content": _AI_PROMPT.format(title=title, description=description)}],
                },
            )
            response.raise_for_status()
            raw = response.json()["choices"][0]["message"]["content"].strip().upper()
            for fach in Fach:
                if fach.value in raw:
                    return fach
            print(f"[AI] Unerwartete Antwort: {raw!r}")
    except Exception as exc:
        print(f"[AI] Fehler: {exc}")
    return None


async def classify(title: str, description: str) -> Fach:
    return await classify_ai(title, description) or classify_keyword(title, description)


def next_id() -> int:
    return max((s.id for s in user_stories), default=0) + 1


async def build_story(title: str, description: str) -> UserStory:
    return UserStory(
        id=next_id(),
        title=title,
        description=description,
        classification=await classify(title, description),
    )


@app.get("/userstories", response_model=List[UserStory])
def get_user_stories():
    return user_stories


@app.get("/userstories/{story_id}", response_model=UserStory)
def get_user_story_by_id(story_id: int):
    for s in user_stories:
        if s.id == story_id:
            return s
    raise HTTPException(status_code=404, detail="User Story nicht gefunden")


@app.get("/userstories/fach/{fach_str}", response_model=List[UserStory])
def get_user_stories_by_fach(fach_str: str):
    try:
        fach = Fach(fach_str.upper())
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Unbekanntes Fach: {fach_str}")
    return [s for s in user_stories if s.classification == fach]


@app.patch("/userstories/{story_id}/{fach_str}")
def change_classification(story_id: int, fach_str: str):
    for s in user_stories:
        if s.id == story_id:
            try:
                fach = Fach(fach_str.upper())
                s.classification = fach
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Unbekanntes Fach: {fach_str}")
    raise HTTPException(status_code=404, detail="User Story nicht gefunden")


@app.delete("/userstories/{story_id}", status_code=204)
def delete_user_story(story_id: int):
    for i, s in enumerate(user_stories):
        if s.id == story_id:
            user_stories.pop(i)
            return
    raise HTTPException(status_code=404, detail="User Story nicht gefunden")


async def _process_rows(rows: list[dict]) -> ImportResult:
    imported, skipped, errors, added = 0, 0, [], []

    for idx, row in enumerate(rows, start=1):
        try:
            title = str(row.get("title", "")).strip()
            if not title:
                skipped += 1
                errors.append(f"Eintrag {idx}: 'title' fehlt")
                continue

            description = str(row.get("description", "")).strip()
            story = await build_story(title, description)
            user_stories.append(story)
            added.append(story)
            imported += 1

        except Exception as exc:
            skipped += 1
            errors.append(f"Eintrag {idx}: {exc}")

    return ImportResult(imported=imported, skipped=skipped, errors=errors, stories=added)


@app.post("/import", response_model=ImportResult)
async def import_stories(file: UploadFile = File(...)):
    content = await file.read()
    name = (file.filename or "").lower()

    if name.endswith(".csv"):
        rows = list(csv.DictReader(io.StringIO(content.decode("utf-8-sig"))))

    elif name.endswith(".json"):
        try:
            data = json.loads(content.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=400, detail=f"Ungültiges JSON: {exc}")
        if not isinstance(data, list):
            raise HTTPException(status_code=400, detail="JSON muss ein Array sein")
        rows = data

    elif name.endswith(".xml"):
        try:
            root = ET.fromstring(content.decode("utf-8"))
        except ET.ParseError as exc:
            raise HTTPException(status_code=400, detail=f"Ungültiges XML: {exc}")
        items = root.findall("user_story") if root.tag != "user_story" else [root]

        def txt(el, tag: str) -> str:
            child = el.find(tag)
            return (child.text or "").strip() if child is not None else ""

        rows = [{"title": txt(el, "title"), "description": txt(el, "description")} for el in items]

    else:
        raise HTTPException(status_code=415, detail="Format nicht unterstützt – erlaubt: .csv, .json, .xml")

    return await _process_rows(rows)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)