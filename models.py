from sqlalchemy import Column, String, Boolean, DateTime

from datetime import datetime

from database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False)
    password = Column(String(80), nullable=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
