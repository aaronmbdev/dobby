import structlog

from src.agent.checkpointer import _pool

logger = structlog.get_logger(__name__)


class ThreadService:
    def list_threads(self) -> list[str]:
        logger.info("Listing threads")
        with _pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT DISTINCT thread_id FROM checkpoints ORDER BY thread_id"
                )
                return [row[0] for row in cur.fetchall()]

    def delete_thread(self, thread_id: str) -> bool:
        logger.info("Deleting thread", thread_id=thread_id)
        with _pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM checkpoints WHERE thread_id = %s LIMIT 1",
                    (thread_id,),
                )
                if cur.fetchone() is None:
                    return False
                cur.execute("DELETE FROM checkpoint_writes WHERE thread_id = %s", (thread_id,))
                cur.execute("DELETE FROM checkpoint_blobs WHERE thread_id = %s", (thread_id,))
                cur.execute("DELETE FROM checkpoints WHERE thread_id = %s", (thread_id,))
                return True
