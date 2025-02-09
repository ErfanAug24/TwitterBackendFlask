from typing import Optional, List
from sqlalchemy import Integer, String, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..Config.sqlalchemy_conf import db


class Feedback(db.Model):
    __tablename__ = "Feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("User.id"), nullable=False)
    content: Mapped[str] = mapped_column(db.Text, nullable=False)  # Feedback content
    rating: Mapped[int] = mapped_column(
        Integer, nullable=True
    )  # Optional rating (1-5, for example)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )  # Timestamp
    category: Mapped[str] = mapped_column(db.String(50), nullable=True)
