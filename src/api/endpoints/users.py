from flask_jwt_extended import jwt_required, get_jwt_claims
from flask_restplus import Resource
from sqlalchemy import and_, not_
from sqlalchemy.exc import DatabaseError

from src.api.endpoints.business.user_business import *
from src.api.serializers import user_get, user_post, user_put, \
    resetpassword, user_password, user_getbyemail
from src.api.restplus import api
from src.database.models import User
from src.util.timerplus import TimerPlus

log = logging.getLogger('rotating_log')

ns = api.namespace('users', description='Operations related to users')


@api.header('Authorization', 'Bearer token', required=False)
@ns.route('/')
class UsersCollection(Resource):

    @api.marshal_list_with(user_get)
    @jwt_required
    def get(self):
        """
        Returns list of users
        """
        users = User.query.all()
        return users

    @api.response(201, 'User successfully created')
    @api.doc(security=None)
    # @api.response(409, 'User was not created due to invalid user id')
    @api.expect(user_post)
    @api.marshal_with(user_get)
    def post(self):
        """
        Creates a new user.
        """
        data = request.json
        created_user = create_user(data)
        return created_user, 201


@api.header('Authorization', 'Bearer token', required=True)
@ns.route('/<string:id>')
class UserItem(Resource):

    @api.marshal_with(user_get)
    @jwt_required
    def get(self, id):
        """
         Returns a specific User.
        """
        claims = get_jwt_claims()
        return get_user_by_id(id)

    @api.response(200, 'User successfully updated')
    @api.expect(user_put)
    @api.marshal_with(user_get)
    @jwt_required
    def put(self, id):
        """
        Updates a user.
        """
        # The user needs to be able to retrieve the user to update
        user_to_update = get_user_by_id(id)
        data = request.json
        updated_user = update_user(user_to_update, data)
        return updated_user, 200

    @jwt_required
    # TODO consider having an endpoint (with requires_role(RoleType.sysadmin)) to un-delete a user
    def delete(self, id):
        """
        Deletes a User
        """
        # make sure logged in user can actually retrieve the user that is to be deleted
        user_to_delete = get_user_by_id(id)

        try:
            delete_user(user_to_delete)
        except DatabaseError as e:
            if e.orig.sqlstate == '45000':
                message_text = e.orig.msg
                api.abort(code=409, message=message_text)
        return 'User Successfully deleted', 200


@ns.route('/set_password/<string:token>')
@api.doc(security='None')
class UserSetPassword(Resource):
    @api.response(202, 'Password successfully updated')
    @api.response(404, 'User not found')
    @api.expect(user_password)
    @api.marshal_with(user_get)
    def put(self, token):
        """
        Set password for a specific User
        """
        data = request.json
        updated_user = update_user_password(data, token)
        if updated_user is False:
            return False, 404

        return updated_user, 202


@ns.route('/get_by_token/<string:token>')
@api.doc(security='None')
class UserGetByToken(Resource):
    @api.response(200, "User found")
    @api.response(404, 'User not found')
    @api.marshal_with(user_get)
    def get(self, token):
        """
        Returns a specific user by token
        """
        user = get_user_by_token(token)
        if user is False:
            return False, 404

        return user, 200


trial_cache = {}


def restart_trials(ip):
    tp = TimerPlus(20, restart_trials, (ip,))
    trial_cache[ip] = {'trials': 3, 'timer': tp}


@ns.route('/get_by_email/<string:email>')
@api.doc(security='None')
class UserGetByEmail(Resource):
    @api.response(200, "User id found")
    @api.response(404, 'User id not found')
    @api.response(403, 'Max trials has been exceeded')
    @api.marshal_with(user_getbyemail)
    def get(self, email):
        """
        Returns a specific user's ID by email
        """
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

        id = get_userid_by_email(email)
        if id is False:
            return {'failed_attempts': trial_cache[ip]['trials']}, 404

        trial_cache[ip]['timer'].cancel()
        del(trial_cache[ip])

        return {'id': id}, 200
