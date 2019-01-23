import datetime
import logging

from flask import make_response, jsonify, Flask, request
from flask_jwt_extended import JWTManager, create_access_token
from flask_restplus import Resource
from werkzeug.security import check_password_hash

from src.api.endpoints.business.login_business import create_token
from src.api.serializers import user_credentials, token
from src.api.restplus import api
from src.database.models import User
from src.util.timerplus import TimerPlus

log = logging.getLogger('rotating_log')
ns = api.namespace('login', description='Login with credentials')
jwt = JWTManager()


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user_id = User.query.filter(User.email == identity).one().id
    return {
        'email': identity,
        'user_id': user_id
    }


trial_cache = {}


def restart_trials(ip):
    tp = TimerPlus(20, restart_trials, (ip,))
    trial_cache[ip] = {'trials': 3, 'timer': tp}


@ns.route('/')
@api.doc(security=None)
class Authentication(Resource):
    @api.response(401, 'Invalid username or password')
    @api.response(403, 'Max trials has been exceeded')
    @api.expect(user_credentials)
    @api.marshal_with(token)
    def post(self):

        ip = request.remote_addr
        if ip in trial_cache:
            if trial_cache[ip]['trials'] == 6:
                time_remaining = trial_cache[ip]['timer'].remaining()
                return {'time_remaining': int(time_remaining)+1}, 403
            else:
                trial_cache[ip]['trials'] += 1
                if trial_cache[ip]['trials'] == 6:
                    trial_cache[ip]['timer'].start()
        else:
            tp = TimerPlus(20, restart_trials, (ip, ))
            trial_cache[ip] = {'trials': 1, 'timer': tp}

        data = request.json
        email = str.lower(data.get('email')) if data.get('email') else None
        password = data.get('password')
        existing_account = User.query.filter(User.email == email).first()
        if existing_account and check_password_hash(existing_account.password, password):
            token = create_access_token(identity=email)
            serialized_token = create_token(token)
            trial_cache[ip]['timer'].cancel()
            del(trial_cache[ip])
            return {'access_token': serialized_token.access_token, 'id': existing_account.id}

        return {'failed_attempts': trial_cache[ip]['trials']}, 401
