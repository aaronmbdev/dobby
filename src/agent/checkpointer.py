from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver

from src.config.settings import settings

_pool = ConnectionPool(
    settings.psycopg_url,
    max_size=10,
    kwargs={"autocommit": True, "prepare_threshold": 0},
)

checkpointer = PostgresSaver(_pool)
