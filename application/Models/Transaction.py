from datetime import datetime, timezone
import sqlalchemy as sqla
import sqlalchemy.orm as so
from application import db
from application.Models.User import User

class Transaction(db.Model):
    __tablename__ = "Transactions"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    Timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    UpdateCount: so.Mapped[int] = so.mapped_column(sqla.Integer)
    Rank: so.Mapped[float] = so.mapped_column(sqla.FLOAT)
    WinCount: so.Mapped[int] = so.mapped_column(sqla.Integer, default=0)
    LossCount: so.Mapped[int] = so.mapped_column(sqla.Integer, default=0)
    user_id: so.Mapped[int] = so.mapped_column(sqla.ForeignKey("Users.id"), insert_default=-1)
    user: so.Mapped[User] = db.relationship(back_populates="transactions")

    def __repr__(self):
        return '<Transaction {}>'.format(self.user_id)