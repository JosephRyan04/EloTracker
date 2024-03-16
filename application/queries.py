from application import app,db
from application.models import User, Transaction
import sqlalchemy as sa
import random


def get_user(connectCode):
    query = sa.select(User).where(User.ConnectCode == connectCode)
    user = db.session.execute(query).scalar()
    if user is None:
        app.logger.info("User does not exist")
        #user = add_user(connectCode)
        return None
    
    return user

def user_exists(connectCode):
    query = sa.select(User.id).where(User.ConnectCode == connectCode)
    user = db.session.execute(query).scalar()
    if user is None:
        return False
    
    return True

def add_user(api_response):
    tmp_user = User(ConnectCode = api_response['code'],
                    DisplayName = api_response['displayName'],
                    CurrentRank = api_response['ratingOrdinal'],
                    UpdateCount = api_response['updateCount'])
    
    db.session.add(tmp_user)
    db.session.commit()

def update_user(api_response):
    query = sa.update(User).where(User.ConnectCode
                                   == api_response['code']).values(CurrentRank = api_response['ratingOrdinal'],
                                                                    UpdateCount = api_response['updateCount'],
                                                                    DisplayName = api_response['displayName'])
    user = db.session.execute(query)
    db.session.commit()

    return "Success"

def add_transaction(api_response):
    tmp_transaction = Transaction(
                    Rank = api_response['ratingOrdinal'],
                    UpdateCount = api_response['updateCount'],
                    WinCount = api_response['wins'],
                    LossCount = api_response['losses'])
    
    tmp_user = get_user(api_response['code'])
    tmp_user.transactions.append(tmp_transaction)

    db.session.add(tmp_transaction)
    db.session.commit()
    return tmp_transaction

def get_transactions(connectCode):
    data = list()

    loss = 0
    last_loss = 0
    cur_streak = 0
    max_streak = 0

    user = get_user(connectCode)
    for rank in user.transactions:

        if rank.LossCount > loss:
            loss = rank.LossCount
            last_loss = rank.UpdateCount
            cur_streak = 0

        elif rank.LossCount == loss:
            cur_streak = rank.UpdateCount - last_loss
            max_streak = max(max_streak, cur_streak)

        data.append((rank.Rank))

    user.CurrentStreak = cur_streak
    user.MaxStreak = max_streak
    db.session.commit()
    print(data, max_streak)
    return data