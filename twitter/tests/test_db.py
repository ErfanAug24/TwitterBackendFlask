from typing import Optional, List
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .. import db


class Test(db.get_instance().Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    fullname: Mapped[Optional[str]] = mapped_column(String(50), nullable=False)
    join_date: Mapped[datetime] = mapped_column(default=datetime.now)
    update_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
