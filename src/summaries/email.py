import resend

from src.config.settings import settings

resend.api_key = settings.resend_api_key


def send_summary(summary_type: str, content: str) -> None:
    resend.Emails.send({
        "from": settings.resend_from_email,
        "to": settings.resend_to_email,
        "subject": f"Dobby — {summary_type.capitalize()} Summary",
        "text": content,
    })
