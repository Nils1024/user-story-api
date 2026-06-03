from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="User Story Service",
    version="1.0.0"
)

# --------------------------------------------------
# Modelle
# --------------------------------------------------

class UserStory(BaseModel):
    id: int
    title: str
    description: str


class ClassificationRequest(BaseModel):
    user_story: str


class ClassificationResponse(BaseModel):
    domain: str


# --------------------------------------------------
# Beispiel-Datenbank (In-Memory)
# --------------------------------------------------

user_stories = [
    UserStory(
        id=1,
        title="Login",
        description="Als Benutzer möchte ich mich anmelden."
    ),
    UserStory(
        id=42,
        title="Passwort zurücksetzen",
        description="Als Benutzer möchte ich mein Passwort zurücksetzen."
    )
]


# --------------------------------------------------
# GET /userstories
# Gibt alle gespeicherten User Stories zurück
# --------------------------------------------------

@app.get("/userstories", response_model=List[UserStory])
def get_user_stories():
    return user_stories


# --------------------------------------------------
# GET /userstories/{id}
# Gibt eine User Story anhand ihrer ID zurück
# --------------------------------------------------

@app.get("/userstories/{story_id}", response_model=UserStory)
def get_user_story(story_id: int):
    for story in user_stories:
        if story.id == story_id:
            return story

    raise HTTPException(
        status_code=404,
        detail="User Story nicht gefunden"
    )


# --------------------------------------------------
# POST /import/csv
# CSV-Datei hochladen und verarbeiten
# --------------------------------------------------

@app.post("/import/csv")
async def import_csv(file: UploadFile = File(...)):
    content = await file.read()

    # Hier später CSV parsen
    # z.B. mit pandas oder csv-Modul

    return {
        "filename": file.filename,
        "size": len(content),
        "message": "CSV erfolgreich empfangen"
    }


# --------------------------------------------------
# POST /import/json
# JSON-Datei hochladen und verarbeiten
# --------------------------------------------------

@app.post("/import/json")
async def import_csv(file: UploadFile = File(...)):
    content = await file.read()

    # Hier später CSV parsen
    # z.B. mit pandas oder csv-Modul

    return {
        "filename": file.filename,
        "size": len(content),
        "message": "CSV erfolgreich empfangen"
    }


# --------------------------------------------------
# POST /classify
# User Story klassifizieren
# --------------------------------------------------

@app.post(
    "/classify",
    response_model=ClassificationResponse
)
def classify_story(request: ClassificationRequest):

    text = request.user_story.lower()

    # Dummy-Klassifikation
    if "login" in text or "passwort" in text:
        domain = "Benutzerverwaltung"
    elif "rechnung" in text:
        domain = "Abrechnung"
    else:
        domain = "Allgemein"

    return ClassificationResponse(domain=domain)