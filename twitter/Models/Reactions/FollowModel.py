from typing import Optional, List
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Enum
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ... import db


# from .. import User  # from twitter.Models import user


class Follow(db.Model):
    __tablename__ = "follow"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    follower_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("User.id"), nullable=True
    )
    following_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("User.id"), nullable=True
    )
    follower: Mapped["User"] = relationship(
        "User", foreign_keys=[follower_id], back_populates="followings", lazy="joined"
    )
    following: Mapped["User"] = relationship(
        "User", foreign_keys=[following_id], back_populates="followers", lazy="joined"
    )
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
