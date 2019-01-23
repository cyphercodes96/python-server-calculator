from flask_restplus import fields
from src.api.restplus import api


def my_format_iso8601(self, dt):
    return dt.isoformat().replace('+00:00', 'Z')


fields.DateTime.format_iso8601 = my_format_iso8601

user_credentials = api.model('Login', {
    'email': fields.String(readOnly=True, description='The email used for authentication'),
    'password': fields.String(readOnly=True, description='The password used for authentication')
})

token = api.model('Token', {
    'access_token': fields.String(readOnly=True, description='Access-token'),
    'id': fields.String(readOnly=True, description='The unique identifier of a user'),
    'failed_attempts': fields.Integer(readOnly=True, description='Number of failed attempts'),
    'time_remaining': fields.Integer(readOnly=True, description='Number of seconds before a new login is accepted')
})

user_base = api.model('User', {
    'email': fields.String(description='The email used for authentication'),
    'first_name': fields.String(description='First name'),
    'middle_name': fields.String(description='Middle name'),
    'last_name': fields.String(description='Last name')
})

user_get = api.inherit('UserRead', user_base, {
    'id': fields.String(description='The unique identifier of a user'),
    'created_ts': fields.DateTime(description='Created at this timestamp'),
    'last_modified_ts': fields.DateTime(description='Updated at this timestamp'),
    'deleted_ts': fields.DateTime(description='Deleted at this timestamp')
})

user_post = api.inherit('UserCreate', user_base, {
    'email': fields.String(description='The email used for authentication', required=True),
    'password': fields.String(description='The password used for authentication', required=False),
})

user_put = api.inherit('UserUpdate', user_base, {
    'password': fields.String(description='The password used for authentication', required=False),
})

user_password = api.model('UserUpdatePassword', {
    'password': fields.String(description='The password used for authentication', required=True)
})

user_getbyemail = api.model('UserGetByEmail', {
    'id': fields.String(description='The unique identifier of a user'),
    'failed_attempts': fields.Integer(description='Number of failed attempts'),
    'time_remaining': fields.Integer(description='Number of seconds before a new attempt is accepted')
})

resetpassword = api.model('ResetPassword', {
    'resetpass_base_url': fields.String(required=False, description='Base URL for reset password form')
})

operation = api.model('OperationGet', {
    'id': fields.Integer(description='The unique identifier of an operation'),
    'number0': fields.Float(description='The first number of the operation'),
    'number1': fields.Float(description='The second number of the operation'),
    'created_ts': fields.DateTime(description='Created at this timestamp'),
    'user_id': fields.String(description='The unique identifier of a user to whom this operation belongs to'),
    'operator': fields.String(description='The operator of this operation'),
    'result': fields.Float(description='The result of the operation')
})

operation_post = api.model('OperationForPost', {
    'number0': fields.Float(description='The first number of the operation'),
    'number1': fields.Float(description='The second number of the operation'),
    'operator': fields.String(description='The operator of this operation')
})