from fastapi import FastAPI

from .routers import classify, importers, userstories

app = FastAPI(
    title="User Story API",
    version="0.1.0",
    description="Prototype API for importing and normalizing user stories from heterogeneous sources and classifying them into SDM/EvP/GiD.",
)

app.include_router(importers.router)
app.include_router(userstories.router)
app.include_router(classify.router)


@app.get("/health")
def health():
    return {"status": "ok"}
