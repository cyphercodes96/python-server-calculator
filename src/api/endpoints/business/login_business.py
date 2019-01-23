from src.database.models import Token
from src.util.logging import trace


@trace('debug')
def create_token(token):
    created_token = Token(token)
    return created_token
