from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from datetime import datetime, timedelta

# from . import User
from .. import db


class LowPriority(db.Model):
    __tablename__ = "LowPriority"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("User.id"), nullable=False)
    reason: Mapped[str] = mapped_column(
        String(255), nullable=True
    )  # Reason for restriction
    restricted_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )  # When the restriction was applied
    expires_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )  # Expiry time

    user: Mapped["User"] = relationship("User", back_populates="restrictions")
