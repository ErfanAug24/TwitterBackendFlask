from typing import Optional, List
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Enum
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ...Config.sqlalchemy_conf import db


# from .. import User, Tweet
# from . import Comment, Reply


class Like(db.Model):
    __tablename__ = "Like"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    tweet_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Tweet.id"), nullable=False, unique=True
    )
    comment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Comment.id"), nullable=False, unique=True
    )
    reply_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Reply.id"), nullable=False, unique=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("User.id"), nullable=False, unique=True
    )
    tweet: Mapped["Tweet"] = relationship(
        back_populates="likes", foreign_keys=[tweet_id]
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="likes", foreign_keys=[user_id]
    )
    comment: Mapped["Comment"] = relationship(
        "Comment", back_populates="likes", foreign_keys=[comment_id]
    )
    reply: Mapped["Reply"] = relationship(
        "Reply", back_populates="likes", foreign_keys=[reply_id]
    )
    liked_at: Mapped[datetime] = mapped_column(DateTime(True), default=datetime.now)
