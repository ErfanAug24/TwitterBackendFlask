from datetime import datetime
from typing import List, Optional
from xmlrpc.client import DateTime

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..Config.sqlalchemy_conf import db


class User(db.Model):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    fullname: Mapped[Optional[str]] = mapped_column(String(50), nullable=False)
    birthdate: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(10), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    old_password_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    profile_picture_url: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    join_date: Mapped[datetime] = mapped_column(default=datetime.now)
    update_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    # Tweet Relationships
    tweets: Mapped[List["Tweet"]] = relationship(
        "Tweet", back_populates="user", foreign_keys="Tweet.user_id"
    )
    # Follow RelationShips
    followers: Mapped[List["Follow"]] = relationship(
        "Follow", back_populates="follower", foreign_keys="Follow.follower_id"
    )
    followings: Mapped[List["Follow"]] = relationship(
        "Follow", back_populates="following", foreign_keys="Follow.following_id"
    )
    # Comment RelationShips
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="commented_by", foreign_keys="Comment.user_id"
    )
    # Reply RelationShips
    replies: Mapped[List["Reply"]] = relationship(
        "Reply", back_populates="user", foreign_keys="Reply.user_id"
    )
    # Report RelationShips
    reports_received: Mapped[List["Report"]] = relationship(
        "Report", back_populates="reported", foreign_keys="Report.user_reported_id"
    )
    reports_made: Mapped[List["Report"]] = relationship(
        "Report", back_populates="reporter", foreign_keys="Report.user_reporter_id"
    )
    # LowPriority
    restrictions: Mapped[List["LowPriority"]] = relationship(
        "LowPriority",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    likes: Mapped[List["Like"]] = relationship(
        "Like",
        back_populates="user",
        foreign_keys="Like.user_id",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"user(id={self.id!r}, username={self.username!r},\
         email={self.email}, join_date={self.join_date!r}, is_verified={self.is_verified!r})"

    def __str__(self):
        return f"username:{self.fullname}-phone:{self.phone}-join_date:{self.join_date}-is_user_verified:{self.is_verified}"
