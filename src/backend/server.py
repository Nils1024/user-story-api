from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
from enum import Enum

app = FastAPI(
    title="User Story Service",
    version="1.0.0"
)


class UserStory(BaseModel):
    id: int
    title: str
    description: str
    classification: Fach


class ClassificationRequest(BaseModel):
    user_story: str


class ClassificationResponse(BaseModel):
    domain: str


class Fach(Enum):
    SDM = 1
    GID = 2
    EVP = 3


user_stories = [
    UserStory(
        id=1,
        title="Login",
        description="Als Benutzer möchte ich mich anmelden.",
        classification=Fach.SDM
    )
]


@app.get("/userstories", response_model=List[UserStory])
def get_user_stories():
    return user_stories


@app.get("/userstories/{story_id}", response_model=UserStory)
def get_user_story(story_id: int):
    for story in user_stories:
        if story.id == story_id:
            return story

    raise HTTPException(
        status_code=404,
        detail="User Story nicht gefunden"
    )


@app.post("/import")
async def import_csv(file: UploadFile = File(...)):
    content = await file.read()

    # Hier später CSV parsen

    return {
        "filename": file.filename,
        "size": len(content),
        "message": "CSV erfolgreich empfangen"
    }


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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)