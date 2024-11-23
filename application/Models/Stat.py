from datetime import datetime, timezone
from typing import List
import sqlalchemy as sqla
from sqlalchemy.orm import mapped_column, Mapped
from application import db

class Stat(db.Model):
    __tablename__ = "Stats"

    def as_dict(self):
        return {
            'currentstreak': self.CurrentStreak,
            'maxstreak': self.MaxStreak,
            'peakregional': self.PeakRegional,
            'peakglobal': self.PeakGlobal
        }

    id: Mapped[int] = mapped_column(primary_key=True)
    LastCalculated: Mapped[datetime] = mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc), onupdate=datetime.utcnow)
    MaxStreak: Mapped[int] = mapped_column(sqla.Integer, nullable=True)
    CurrentStreak: Mapped[int] = mapped_column(sqla.Integer, nullable=True)
    PeakGlobal: Mapped[int] = mapped_column(sqla.Integer, nullable=True)
    PeakRegional: Mapped[int] = mapped_column(sqla.Integer, nullable=True)
    user_id: Mapped[int] = mapped_column(sqla.ForeignKey("Users.id"), insert_default=-1)

    def __repr__(self):
        return '<Stat {}>'.format(self.id)