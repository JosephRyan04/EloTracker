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
ns = api.namespace('api', description='User operations')

@ns.route('/')
@ns.route('/test-route')
class Index(Resource):
    def get(self):
        """Index route"""
        return "User Controller"

@ns.route('/update-elo')
class UpdateElo(Resource):
    def get(self):
        """Update ELO without name"""
        uid = request.args.get("player")
        if(uid is None):
            app.logger.warning("No UID given, please include in parameters")
            return "Check console"
        uid = utils.format_cc(uid)
        tag = {"cc": uid, "uid": uid}
        return hit_slippi_API(tag)

@ns.route('/update-elo/<string:name>')
class UpdateEloWithName(Resource):
    def get(self, name):
        """Update ELO with name"""
        uid = utils.format_cc(name)
        tag = {"cc": uid, "uid": uid}
        return hit_slippi_API(tag)

@ns.route('/getuser/<string:name>')
class GetUser(Resource):
    def get(self, name):
        """Get user by name"""
        uid = utils.format_cc(name)
        return get_user(uid)

@ns.route('/user-ranks')
class UserRanks(Resource):
    def get(self):
        """Get user ranks"""
        uid = request.args.get("player")
        uid = utils.format_cc(uid)
        return get_transactions(uid)
    
@ns.route('/user-ranks/<string:name>')
class UserRanks(Resource):
    def get(self, name):
        """Get user ranks"""
        uid = utils.format_cc(name)
        return get_transactions(uid)

@ns.route('/random-user')
class RandomUser(Resource):
    def get(self):
        """Get a random user"""
        return get_random_user()