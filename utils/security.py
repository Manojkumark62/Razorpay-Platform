from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    normalized_password = (password or "")[:72]
    return pwd_context.hash(normalized_password)


def verify_password(password: str, hashed_password: str) -> bool:
    normalized_password = (password or "")[:72]
    return pwd_context.verify(normalized_password, hashed_password)