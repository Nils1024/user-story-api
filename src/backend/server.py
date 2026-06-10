import json
import csv
import io
import xml.etree.ElementTree as ET
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

app = FastAPI(
    title="User Story Service",
    version="1.0.0"
)


class Fach(str, Enum):
    """Bündelungsfächer"""
    SDM = "SDM"
    GID = "GID"
    EVP = "EVP"


class UserStory(BaseModel):
    id: int
    title: str
    description: str
    classification: Optional[Fach] = None


class ImportResult(BaseModel):
    imported: int
    skipped: int
    errors: List[str]
    stories: List[UserStory]


user_stories = [
    UserStory(
        id=1,
        title="Login",
        description="Als Benutzer möchte ich mich anmelden.",
        classification=Fach.SDM
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


def classify(title: str, description: str) -> Fach:
    text = f"{title} {description}".lower()
    scores = {f: sum(1 for kw in kws if kw in text) for f, kws in _KEYWORDS.items()}
    return max(scores, key=lambda f: scores[f])
 
 
def next_id() -> int:
    return max((s.id for s in user_stories), default=0) + 1
 
 
def id_exists(story_id: int) -> bool:
    return any(s.id == story_id for s in user_stories)
 
 
def build_story(story_id: int, title: str, description: str) -> UserStory:
    return UserStory(
        id=story_id,
        title=title,
        description=description,
        classification=classify(title, description),
    )


@app.get("/userstories", response_model=List[UserStory])
def get_user_stories(fach: Optional[Fach] = None):
    return [s for s in user_stories if fach is None or s.classification == fach]
 
 
@app.get("/userstories/{story_id}", response_model=UserStory)
def get_user_story(story_id: int):
    for s in user_stories:
        if s.id == story_id:
            return s
    raise HTTPException(status_code=404, detail="User Story nicht gefunden")
 
 
@app.post("/userstories", response_model=UserStory, status_code=201)
def create_user_story(story: UserStory):
    if id_exists(story.id):
        raise HTTPException(status_code=409, detail=f"ID {story.id} bereits vorhanden")
    story.classification = classify(story.title, story.description)
    user_stories.append(story)
    return story
 
 
@app.put("/userstories/{story_id}", response_model=UserStory)
def update_user_story(story_id: int, updated: UserStory):
    for i, s in enumerate(user_stories):
        if s.id == story_id:
            updated.classification = classify(updated.title, updated.description)
            user_stories[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="User Story nicht gefunden")
 
 
@app.delete("/userstories/{story_id}", status_code=204)
def delete_user_story(story_id: int):
    for i, s in enumerate(user_stories):
        if s.id == story_id:
            user_stories.pop(i)
            return
    raise HTTPException(status_code=404, detail="User Story nicht gefunden")


def _process_rows(rows: list[dict]) -> ImportResult:
    imported, skipped, errors, added = 0, 0, [], []
 
    for idx, row in enumerate(rows, start=1):
        try:
            title = str(row.get("title", "")).strip()
            if not title:
                skipped += 1
                errors.append(f"Eintrag {idx}: 'title' fehlt")
                continue
 
            description = str(row.get("description", "")).strip()
            story = build_story(title, description)
            user_stories.append(story)
            added.append(story)
            imported += 1
 
        except Exception as exc:
            skipped += 1
            errors.append(f"Eintrag {idx}: {exc}")
 
    return ImportResult(imported=imported, skipped=skipped, errors=errors, stories=added)
 
 
@app.post("/import", response_model=ImportResult)
async def import_stories(file: UploadFile = File(...)):
    """
    Erkennt das Format automatisch anhand der Dateiendung.
    ID und Klassifikation werden intern vergeben – nur title und description werden gelesen.
 
    CSV  →  title,description
    JSON →  [{"title": "...", "description": "..."}]
    XML  →  <user_stories><user_story><title>…</title><description>…</description></user_story></user_stories>
    """
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
 
    return _process_rows(rows)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)