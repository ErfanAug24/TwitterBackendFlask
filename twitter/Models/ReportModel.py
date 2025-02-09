from typing import Optional, List
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Enum
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..Config.sqlalchemy_conf import db

# from . import User
from ..Utils.Auth import ReportOptions


class Report(db.Model):
    __tablename__ = "Report"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_reporter_id = mapped_column(ForeignKey("User.id"), nullable=False)
    user_reported_id = mapped_column(ForeignKey("User.id"), nullable=False)
    reasons: Mapped[List[ReportOptions]] = mapped_column(
        Enum(ReportOptions), nullable=False
    )
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reporter: Mapped["User"] = relationship(
        "User", foreign_keys=[user_reporter_id], back_populates="reports_made"
    )
    reported: Mapped["User"] = relationship(
        "User", back_populates="reports_received", foreign_keys=[user_reported_id]
    )
    reported_at: Mapped[DateTime] = mapped_column(
        DateTime(True), nullable=False, default=datetime.now
    )
