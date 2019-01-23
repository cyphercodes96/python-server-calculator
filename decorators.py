from functools import wraps

import jwt
from flask import request
from src.database.models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return {'message': 'Token is missing'}, 401

        try:
            data = jwt.decode(token, 'secret')
            current_user = User.query.filter(User.public_id == data['public_id']).one()
        except:
            return "Token is invalid", 401

        return f(*args, current_user, **kwargs)

    return decorated
