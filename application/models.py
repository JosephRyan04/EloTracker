from datetime import datetime, timezone
from typing import List, Optional
import sqlalchemy as sqla
import sqlalchemy.orm as so
from application import db


# Each User has many Transactions, which each represent an info update from
# the server. This is a nullable one to many relationship. Users are
# primarily used to group and search Transactions. Additionally,
# the user timestamp ensures that slippi api is not queried too often.
class User(db.Model):

    __tablename__ = "Users"

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
    RegionalRank: so.Mapped[int] = so.mapped_column(sqla.Integer, nullable=True)
    #transactions = so.Mapped[List["Transaction"]] = db.relationship()

    #TransactionKey: so.Mapped[Optional[int]] = so.mapped_column(sqla.ForeignKey("Transactions.id"))
    transactions: so.Mapped[List["Transaction"]] = db.relationship(back_populates="user")

    def __repr__(self):
        return '<User {}>'.format(self.ConnectCode)
    



# T
class Transaction(db.Model):

    __tablename__ = "Transactions"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    Timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    UpdateCount: so.Mapped[int] = so.mapped_column(sqla.Integer)
    Rank: so.Mapped[float] = so.mapped_column(sqla.FLOAT)
    WinCount: so.Mapped[int] = so.mapped_column(sqla.Integer, nullable=True)
    LossCount: so.Mapped[int] = so.mapped_column(sqla.Integer, nullable=True)
    user_id: so.Mapped[int] = so.mapped_column(sqla.ForeignKey("Users.id"), insert_default=-1)
    user: so.Mapped["User"] = db.relationship(back_populates="transactions")

    def __repr__(self):
        return '<Transaction {}>'.format(self.user_id)
