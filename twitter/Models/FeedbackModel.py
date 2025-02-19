from sqlalchemy import Integer, String, ForeignKey, DateTime, CheckConstraint, Enum
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from ..Config.sqlalchemy_conf import db
from ..Utils.Common import Rating
from typing import List


class Feedback(db.Model):
    __tablename__ = "Feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("User.id"), nullable=False)
    content: Mapped[str] = mapped_column(db.Text, nullable=False)  # Feedback content
    rating: Mapped[List[Rating]] = mapped_column(
        Enum(Rating),
        CheckConstraint("rating BETWEEN 1 AND 5"),  # DB-level constraint
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )  # Timestamp
    category: Mapped[str] = mapped_column(db.String(50), nullable=True)
