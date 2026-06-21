import structlog
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from src.summaries.service import SummaryService

logger = structlog.get_logger(__name__)

_service = SummaryService()
scheduler = BackgroundScheduler(timezone="UTC")


def _run_weekly_finances() -> None:
    logger.info("generating weekly finance report")
    try:
        _service.send_weekly_finances()
    except Exception:
        logger.exception("weekly finance report failed")


def _run_weekly_diet() -> None:
    logger.info("generating weekly diet report")
    try:
        _service.send_weekly_diet()
    except Exception:
        logger.exception("weekly diet report failed")


def _run_weekly_body() -> None:
    logger.info("generating weekly body report")
    try:
        _service.send_weekly_body()
    except Exception:
        logger.exception("weekly body report failed")


def _run_monthly_finances() -> None:
    logger.info("generating monthly finance report")
    try:
        _service.send_monthly_finances()
    except Exception:
        logger.exception("monthly finance report failed")


# Weekly reports staggered by 5 minutes to avoid concurrent API calls
scheduler.add_job(_run_weekly_finances, CronTrigger(day_of_week="mon", hour=8, minute=0))
scheduler.add_job(_run_weekly_diet,     CronTrigger(day_of_week="mon", hour=8, minute=5))
scheduler.add_job(_run_weekly_body,     CronTrigger(day_of_week="mon", hour=8, minute=10))

# Monthly report runs on the 1st, covering the previous month
scheduler.add_job(_run_monthly_finances, CronTrigger(day=1, hour=8, minute=0))
