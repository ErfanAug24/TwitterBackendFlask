from typing import Optional, List
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .. import db


# from .Reactions import Comment, Like
# from . import User


def create_slug(title):
    return ""


class Tweet(db.Model):
    __tablename__ = "Tweet"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    slug: Mapped[str] = mapped_column(
        String(255), nullable=False, default=create_slug(title), unique=True
    )
    created_date: Mapped[datetime] = mapped_column(DateTime(True), default=datetime.now)
    updated_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("User.id"), nullable=False)
    user: Mapped["User"] = relationship(
        "User", back_populates="tweets", foreign_keys=[user_id]
    )
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="tweet", foreign_keys="Comment.tweet_id"
    )
    likes: Mapped[List["Like"]] = relationship(
        "Like", back_populates="tweet", foreign_keys="Like.tweet_id"
    )

    def __repr__(self):
        return f"user(id={self.id}, title={self.title}, slug={self.slug}, created_date={self.created_date}, user_id={self.user_id}, user={self.user})"

    def __str__(self):
        return f"id:{self.id} | title:{self.title} | user:{self.user}"

    def get_by_id(self, tweet_id):
        return (
            db.session.execute(db.select(self.__class__).where(self.id == tweet_id))
            .scalars()
            .first()
        )

    def get_by_title(self, title):
        return (
            db.session.execute(db.select(self.__class__).where(self.title == title))
            .scalars()
            .first()
        )

    def get_by_user_id(self, user_id):
        return (
            db.session.execute(db.select(self.__class__).where(self.user_id == user_id))
            .scalars()
            .first()
        )
