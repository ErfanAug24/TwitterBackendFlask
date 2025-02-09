from typing import Optional, List
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Enum
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ...Config.sqlalchemy_conf import db


# from .. import User
# from . import Comment, Like


class Reply(db.Model):
    __tablename__ = "Reply"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("User.id"), nullable=False)
    comment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Comment.id"), nullable=False
    )
    comment: Mapped["Comment"] = relationship(
        "Comment", back_populates="replies", foreign_keys=[comment_id]
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="replies", foreign_keys=[user_id]
    )
    replied_at: Mapped[datetime] = mapped_column(
        DateTime(True), default=datetime.now, nullable=False
    )
    likes: Mapped[List["Like"]] = relationship(
        "Like", back_populates="reply", foreign_keys="Like.reply_id"
    )
    message: Mapped[str] = mapped_column(Text, nullable=False)
