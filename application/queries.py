from application import app,db
from application.Models.Stat import Stat
from application.Models.Transaction import Transaction
from application.Models.User import User
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
                                                                    DisplayName = api_response['displayName'])
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
    if user is None:
        return 'User not found', 404, {'ContentType':'text/html'}
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


def leaderboard_by(numeric_column):
    match numeric_column:
        case 'UpdateCount':
            query = sa.select(User).order_by(User.UpdateCount.desc())
        
        case 'MaxStreak':
            query = sa.select(User).order_by(User.MaxStreak.desc())

        case 'CurrentRank':
            query = sa.select(User).order_by(User.CurrentRank.desc())
    
    leaderboard = db.session.execute(query).scalars().fetchmany(10)
    result = list()
    for row in leaderboard:
        result.append(row.as_dict())
    pyJson = json.dumps(result)
    return pyJson

def get_random_user():
    query = sa.select(User).order_by(sa.func.random()).limit(1)
    user = db.session.execute(query).scalar()
    print(user.ConnectCode)
    return json.dumps(user.ConnectCode)

def get_stat(user_id):
    query = sa.select(Stat).where(Stat.user_id == user_id)
    
    stat = db.session.execute(query).scalar()
    return stat.as_dict() or "Stat not found"

def add_stat(stat: Stat):
    stat = Stat(user_id=stat.user_id,
                MaxStreak=stat.MaxStreak,
                CurrentStreak=stat.CurrentStreak,
                PeakGlobal=stat.PeakGlobal,
                PeakRegional=stat.PeakRegional)
    db.session.add(stat)
    db.session.commit()
    return stat.as_dict()