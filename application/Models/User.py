from datetime import datetime, timezone
from typing import List
import sqlalchemy as sqla
import sqlalchemy.orm as so
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

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    LastUpdate: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc), onupdate=datetime.utcnow)
    DisplayName: so.Mapped[str] = so.mapped_column(sqla.String(16), unique=False)
    ConnectCode: so.Mapped[str] = so.mapped_column(sqla.String(9), index=True, unique=True)
    CurrentRank: so.Mapped[float] = so.mapped_column(sqla.Float)
    UpdateCount: so.Mapped[int] = so.mapped_column(sqla.Integer, nullable=True)
    MaxStreak: so.Mapped[int] = so.mapped_column(sqla.Integer, nullable=True)
    CurrentStreak: so.Mapped[int] = so.mapped_column(sqla.Integer, nullable=True)
    Continent: so.Mapped[str] = so.mapped_column(sqla.String(16), nullable=True)
    GlobalRank: so.Mapped[int] = so.mapped_column(sqla.Integer, nullable=True)
    PeakGlobal: so.Mapped[int] = so.mapped_column(sqla.Integer, nullable=True)
    RegionalRank: so.Mapped[int] = so.mapped_column(sqla.Integer, nullable=True)
    transactions: so.Mapped[List["Transaction"]] = db.relationship(back_populates="user")

    def __repr__(self):
        return '<User {}>'.format(self.ConnectCode)