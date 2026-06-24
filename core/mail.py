try:
    from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

    FASTAPI_MAIL_AVAILABLE = True
except ModuleNotFoundError:
    FastMail = None
    MessageSchema = None
    ConnectionConfig = None
    FASTAPI_MAIL_AVAILABLE = False

from core.config import settings


conf = None

if FASTAPI_MAIL_AVAILABLE:
    conf = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=int(settings.MAIL_PORT),
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )