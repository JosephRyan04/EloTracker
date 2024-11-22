from datetime import datetime, timezone
import sqlalchemy as sqla
from sqlalchemy.orm import mapped_column, Mapped
from application import db
from application.Models.User import User

class Transaction(db.Model):
    __tablename__ = "Transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    Timestamp: Mapped[datetime] = mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    UpdateCount: Mapped[int] = mapped_column(sqla.Integer)
    Rank: Mapped[float] = mapped_column(sqla.FLOAT)
    WinCount: Mapped[int] = mapped_column(sqla.Integer, default=0)
    LossCount: Mapped[int] = mapped_column(sqla.Integer, default=0)
    user_id: Mapped[int] = mapped_column(sqla.ForeignKey("Users.id"), insert_default=-1)
    user: Mapped[User] = db.relationship(back_populates="transactions")

    def __repr__(self):
        return '<Transaction {}>'.format(self.user_id)