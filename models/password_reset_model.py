from sqlalchemy import Column, Integer, String
from core.base import Base

class PasswordReset(Base):
    __tablename__ = "password_resets"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    reset_token = Column(String(500), nullable=False)