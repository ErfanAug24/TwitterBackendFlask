from sqlalchemy import String, Integer, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from .. import db


class Token(db.Model):
    __tablename__ = "Token"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    jti: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    token: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"), nullable=False)
    expiration: Mapped[datetime] = mapped_column(nullable=False)
    revoked_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    def __repr__(self):
        return f"Token(id={self.id!r}, jti={self.jti!r}, user_id={self.user_id!r}, expiration={self.expiration!r}, revoked_at={self.revoked_at!r}, reason={self.reason!r})"

    def __str__(self):
        return f"user_id:{self.user_id} | jti:{self.jti} | revoked_at:{self.revoked_at}"

    def get_by_id(self, token_id):
        return (
            db.session.execute(db.select(self.__class__).where(self.id == token_id))
            .scalars()
            .first()
        )

    def get_by_jti(self, jti):
        return (
            db.session.execute(db.select(self.__class__).where(self.jti == jti))
            .scalars()
            .first()
        )
