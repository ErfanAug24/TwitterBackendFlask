from typing import Optional, List
from sqlalchemy import Integer, String
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from .. import db


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    fullname: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(String(10), unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column(String(16))
    profile_picture_url: Mapped[str] = mapped_column(String(255))
    join_date: Mapped[datetime] = mapped_column(default=datetime.now)
    update_date: Mapped[Optional[str]]
    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)

    def __init__(
        self,
    ):
        self.username = None

    def __repr__(self):
        return f"<User(id={self.id!r}, username={self.username!r},\
         email={self.email}, join_date={self.join_date!r}, is_verified={self.is_verified!r}"

    def __str__(self):
        return f"username:{self.fullname}-phone:{self.phone}-join_date:{self.join_date}-is_user_verified:{self.is_verified}"
