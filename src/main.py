from fastapi import FastAPI
from src.api.chat import router


app = FastAPI(
    title="Jarvis Agent"
)


app.include_router(
    router,
    prefix="/api"
)


@app.get("/health")
def health():
    return {"status": "ok"}