import datetime
import uuid

from mixins import IDMixin, TimestampMixin
from sqlalchemy import JSON, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class ChatMessage(Base, IDMixin, TimestampMixin):
    __tablename__ = "chat_messages"

    user_id = Column(String(36))
    message = Column(JSON)
