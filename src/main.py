from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.agent.checkpointer import checkpointer
from src.api.chat import router
from src.memory.database import engine
from src.summaries.scheduler import scheduler


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