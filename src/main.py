from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.agent.checkpointer import checkpointer
from src.api.chat import router
from src.memory.database import engine
from src.summaries.scheduler import scheduler

_CLIENT_DIST = Path(__file__).parent.parent / "client" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    with engine.connect():
        pass
    checkpointer.setup()
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(title="Jarvis Agent", lifespan=lifespan)

app.include_router(router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}


# Serve React static assets (JS, CSS, images) if the build exists
if (_CLIENT_DIST / "assets").exists():
    app.mount("/assets", StaticFiles(directory=_CLIENT_DIST / "assets"), name="assets")


# Catch-all: serve React index.html for any non-API route
@app.get("/")
@app.get("/{full_path:path}")
def serve_spa(full_path: str = ""):
    index = _CLIENT_DIST / "index.html"
    if index.exists():
        return FileResponse(index)
    return {"detail": "React app not built. Run `npm run build` inside /client."}