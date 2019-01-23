import logging
import traceback

from flask import current_app
from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError, DataError

log = logging.getLogger('rotating_log')

authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header'
    }
}

api = Api(authorizations=authorizations, version='1.0', title='TransferTo Calculator API',
          description='TransferTo Calculator', security='Bearer')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(traceback.format_exc())

    if not current_app.config['DEBUG']:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    """"
    Resource not found
    """
    log.warning(traceback.format_exc())
    return {'message': 'The requested resource was not found.'}, 404


@api.errorhandler(IntegrityError)
def integrity_error_handler(e):
    """"
    Foreign Key Constraint Problem
    """
    log.warning(traceback.format_exc())
    return {'message': 'Foreign Key Constraint problem'}, 409


@api.errorhandler(DataError)
def data_error_handler(e):
    """"
    Invalid input data.
    """
    log.warning(traceback.format_exc())
    return {'message': 'Foreign Key Constraint problem'}, 400
