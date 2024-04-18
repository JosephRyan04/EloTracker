from flask import render_template, request, flash, redirect, url_for
from application import app
from .api_call import hit_slippi_API
from .queries import get_user, get_transactions, top_ranked, top_streak, get_random_user
from . import utils



@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
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
    return top_ranked()

@app.route('/api/top-streak')
def streak_leaderboard():
    return top_streak()

@app.route('/api/random-user')
def random_user():
    return get_random_user()