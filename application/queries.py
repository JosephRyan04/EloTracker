from application import app,db
from application.models import User, Transaction
import sqlalchemy as sa
import json
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
                                                                    DisplayName = api_response['displayName'],
                                                                    Continent = api_response['continent'],
                                                                    RegionalRank = api_response['regionalRank'],
                                                                    GlobalRank = api_response['globalRank'])
    user = db.session.execute(query)
    user = get_user(api_response['code'])
    if api_response['globalRank']:
        if user.PeakGlobal is None:
            user.PeakGlobal = api_response['globalRank']
        else:
            user.PeakGlobal = min(user.PeakGlobal, api_response['globalRank'])
        

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
    data = dict()
    data['datapoints'] = list()
    data['timestamps'] = list()

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

        data['datapoints'].append((round(rank.Rank, 1)))
        data['timestamps'].append(rank.Timestamp)
    
    data['wins'] = user.transactions[-1].WinCount
    data['losses'] = user.transactions[-1].LossCount
    data['code'] = user.ConnectCode
    data['updatecount'] = user.UpdateCount
    data['globalrank'] = user.GlobalRank
    data['peakplacement'] = user.PeakGlobal
    data['regionalrank'] = user.RegionalRank
    data['continent'] = user.Continent
    data['rank'] = round(user.CurrentRank,1)
    data['latestchange'] = 0
    if len(user.transactions) > 1: 
        data['latestchange'] = data['datapoints'][-1] - data['datapoints'][-2]

    
    data['latestchange'] = round(data['latestchange'],1)
    data['maxstreak'] = max_streak
    user.CurrentStreak = cur_streak
    user.MaxStreak = max_streak
    db.session.commit()
    pyJson = json.dumps(data, default=str)
    return pyJson

def get_leaderboard():
    query = sa.select(User).order_by(User.CurrentRank.desc())
    leaderboard = db.session.execute(query).scalars().fetchmany(3)
    result = list()
    for row in leaderboard:
        result.append(row.as_dict())
    pyJson = json.dumps(result)
    return pyJson