from flask import render_template, request
from flask_cors import CORS
from flask_restx import Resource
from application import app
from application.SlippiProxy import hit_slippi_API
from application.queries import add_stat, get_stat, get_user, get_transactions, leaderboard_by, get_random_user
import application.utils as utils
from application import api

# Create an Api instance

CORS(app, resources=r'/api/*')

# Define a namespace
ns = api.namespace('api/stat', description='User operations')

@ns.route('/')
class Index(Resource):
    def get(self):
        """Index route"""
        return "Stat Controller"

@ns.route('/top-ranked')
class TopRanked(Resource):
    def get(self):
        """Get top ranked users"""
        return leaderboard_by('CurrentRank')

@ns.route('/top-streak')
class TopStreak(Resource):
    def get(self):
        """Get top streak users"""
        return leaderboard_by('MaxStreak')

@ns.route('/most-games')
class MostGames(Resource):
    def get(self):
        """Get users with most games"""
        return leaderboard_by('UpdateCount')

@ns.route('/user-stats/<int:user_id>')
class UserStats(Resource):
    def get(self, user_id):
        """Get user stats by user ID"""
        return get_stat(user_id)

@ns.route('/calc-stat/<int:user_id>')
class CalcStat(Resource):
    def get(self, user_id):
        """Calculate stat for user ID"""
        return add_stat(user_id)