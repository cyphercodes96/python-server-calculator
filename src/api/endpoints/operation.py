import math
import re
from builtins import eval, str

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_claims
from flask_restplus import Resource
from sqlalchemy import and_, not_
from sqlalchemy.exc import DatabaseError

from src.api.endpoints.business.operation_business import create_operation, search_operations
from src.api.endpoints.business.user_business import *
from src.api.parsers import operation_arguments
from src.api.serializers import user_get, user_post, user_put, \
    resetpassword, user_password, user_getbyemail, operation_post, operation
from src.api.restplus import api
from src.database.models import User
from src.util.timerplus import TimerPlus

log = logging.getLogger('rotating_log')

ns = api.namespace('operations', description='Operations related to operations under users')


@api.header('Authorization', 'Bearer token', required=False)
@ns.route('/')
class OperationsCollection(Resource):

    @api.expect(operation_post)
    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        current_user_id = claims.get('user_id')
        data = request.json
        a = data.get('number0')
        operator = data.get('operator')
        b = data.get('number1')
        if not a:
            m = True
        else:
            m = re.match('-?\d+', str(a))
        if not b:
            n = True
        else:
            n = re.match('-?\d+', str(b))
        if m is None or n is None or operator not in '+-*/^%!√∛':
            return jsonify(result='I Catch a BUG!')
        if operator == '/':
            result = eval(str(a) + operator + str(b))
        elif operator == '^':
            result = math.pow(a, b)
        elif operator == '!':
            result = math.factorial(a)
        elif operator == '√':
            result = math.sqrt(b)
        elif operator == '∛':
            result = math.pow(b, 1/3)
        else:
            result = eval(str(a) + operator + str(b))
        create_operation(a, operator, b, result, current_user_id)
        return jsonify(result=result)

    @jwt_required
    @api.expect(operation_arguments, validate=True)
    @api.marshal_list_with(operation)
    def get(self):
        claims = get_jwt_claims()
        current_user_id = claims.get('user_id')
        args = operation_arguments.parse_args(request)
        start_time = args.get('start_time')
        stop_time = args.get('end_time')
        if start_time and stop_time and start_time >= stop_time:
            api.abort(code=400, message="Stop time must be after Start time")
        return search_operations(current_user_id, start_time, stop_time)