try:
    from fastapi_mail import FastMail, MessageSchema
    FASTAPI_MAIL_AVAILABLE = True
except ModuleNotFoundError:
    FastMail = MessageSchema = None
    FASTAPI_MAIL_AVAILABLE = False

from core.mail import conf


async def send_email(email: str, subject: str, body: str):
    if not FASTAPI_MAIL_AVAILABLE:
        raise RuntimeError("fastapi-mail is required to send emails")

    message = MessageSchema(subject=subject, recipients=[email], body=body, subtype="html")
    fm = FastMail(conf)
    try:
        await fm.send_message(message)
    except Exception as exc:
        message_text = str(exc)
        if not message_text:
            message_text = "SMTP authentication failed"
        raise RuntimeError(
            f"Failed to send email: {message_text}. Check your SMTP credentials or use an app password for Gmail."
        ) from exc