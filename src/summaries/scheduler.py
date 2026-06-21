import structlog
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from src.summaries.service import SummaryService

logger = structlog.get_logger(__name__)

_service = SummaryService()
scheduler = BackgroundScheduler(timezone="UTC")


def _run_weekly() -> None:
    logger.info("generating weekly summary")
    try:
        _service.generate_and_save("weekly")
    except Exception:
        logger.exception("weekly summary generation failed")


def _run_monthly() -> None:
    logger.info("generating monthly summary")
    try:
        _service.generate_and_save("monthly")
    except Exception:
        logger.exception("monthly summary generation failed")


scheduler.add_job(_run_weekly, CronTrigger(day_of_week="mon", hour=8, minute=0))
scheduler.add_job(_run_monthly, CronTrigger(day=1, hour=8, minute=0))
