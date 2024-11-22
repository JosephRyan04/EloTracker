from datetime import datetime, timezone
from typing import List
import sqlalchemy as sqla
from sqlalchemy.orm import mapped_column, Mapped
from application import db

class User(db.Model):
    __tablename__ = "Users"

    def as_dict(self):
        return {
            'code': self.ConnectCode,
            'maxstreak': self.MaxStreak,
            'rank': self.CurrentRank,
            'gamecount': self.UpdateCount
        }

    id: Mapped[int] = mapped_column(primary_key=True)
    LastUpdate: Mapped[datetime] = mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc), onupdate=datetime.utcnow)
    DisplayName: Mapped[str] = mapped_column(sqla.String(16), unique=False)
    ConnectCode: Mapped[str] = mapped_column(sqla.String(9), index=True, unique=True)
    CurrentRank: Mapped[float] = mapped_column(sqla.Float)
    UpdateCount: Mapped[int] = mapped_column(sqla.Integer, nullable=True)
    MaxStreak: Mapped[int] = mapped_column(sqla.Integer, nullable=True)
    CurrentStreak: Mapped[int] = mapped_column(sqla.Integer, nullable=True)
    Continent: Mapped[str] = mapped_column(sqla.String(16), nullable=True)
    GlobalRank: Mapped[int] = mapped_column(sqla.Integer, nullable=True)
    PeakGlobal: Mapped[int] = mapped_column(sqla.Integer, nullable=True)
    RegionalRank: Mapped[int] = mapped_column(sqla.Integer, nullable=True)
    transactions: Mapped[List["Transaction"]] = db.relationship(back_populates="user")

    def __repr__(self):
        return '<User {}>'.format(self.ConnectCode)