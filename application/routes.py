from flask import  Flask, render_template, request
from flask_cors import CORS, cross_origin
from application import app
from .api_call import hit_slippi_API
from .queries import add_stat, get_stat, get_user, get_transactions, leaderboard_by, get_random_user
from . import utils

CORS(app, resources=r'/api/*')

@app.route('/')
@app.route('/test-route')
def index():
    user = {'username': 'Wens'}
    posts = [
        {
            'Player': {'username': 'CWAX#450'},
            'body': 'Rating: 3100'
        },
        {
            'Player': {'username': 'RARE#797'},
            'body': 'Rating: 2450'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/api/update-elo')
def elo():
    uid = request.args.get("player")
    if(uid == None):
        app.logger.warning("No UID given, please include in parameters")
        return "Check console"
    uid = utils.format_cc(uid)
    tag = {"cc": uid, "uid": uid}
    return hit_slippi_API(tag)

@app.route('/api/update-elo/<string:name>')
def update_elo(name):
    uid = utils.format_cc(name)
    tag = {"cc": uid, "uid": uid}
    return hit_slippi_API(tag)

@app.route('/api/getuser/<string:name>')
def ping_user(name):
    uid = utils.format_cc(name)
    return get_user(uid)

@app.route('/api/user-ranks')
def user_ranks():
    uid = request.args.get("player")
    uid = utils.format_cc(uid)
    return get_transactions(uid)

@app.route('/api/top-ranked')
def rank_leaderboard():
    return leaderboard_by('CurrentRank')

@app.route('/api/top-streak')
def streak_leaderboard():
    return leaderboard_by('MaxStreak')

@app.route('/api/most-games')
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def games_leaderboard():
    return leaderboard_by('UpdateCount')

@app.route('/api/random-user')
def random_user():
    return get_random_user()

@app.route('/api/user-stats/<int:user_id>')
def user_stats(user_id):
    return get_stat(user_id)

@app.route('/api/calc-stat/<int:user_id>')
def calc_stat(user_id):
    return add_stat(user_id)