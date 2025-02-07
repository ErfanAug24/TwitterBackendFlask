from typing import Optional, List
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Enum
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ... import db


# from .. import User, Tweet
# from . import Reply, Like


class Comment(db.Model):
    __tablename__ = "Comment"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tweet_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Tweet.id"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("User.id"), nullable=False)
    tweet: Mapped["Tweet"] = relationship(
        "Tweet", back_populates="comments", foreign_keys=[tweet_id]
    )
    message: Mapped[str] = mapped_column(Text, nullable=False)
    commented_by: Mapped["User"] = relationship(
        "User", back_populates="comments", foreign_keys=[user_id]
    )
    replies: Mapped[List["Reply"]] = relationship(
        "Reply", back_populates="comment", foreign_keys="Reply.comment_id"
    )
    likes: Mapped[List["Like"]] = relationship(
        "Like", back_populates="comment", foreign_keys="Like.comment_id"
    )
    commented_at: Mapped[datetime] = mapped_column(
        DateTime(True), default=datetime.now, nullable=False
    )
    modified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(True), nullable=True
    )
