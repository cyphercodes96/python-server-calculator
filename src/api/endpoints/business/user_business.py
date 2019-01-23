import datetime
import uuid

from flask import logging, request, current_app
from src.database import db
from src.util.utc_parser import utcnow
from werkzeug.security import generate_password_hash
from src.database.models import User
from itsdangerous import URLSafeTimedSerializer
from src.util.logging import trace


@trace('debug')
def create_user(data):
    id = str(uuid.uuid4())
    email = str.lower(data.get('email')) if data.get('email') else None
    hashed_password = generate_password_hash(data.get('password'), method='sha512')
    first_name = data.get('first_name')
    middle_name = data.get('middle_name')
    last_name = data.get('last_name')
    created_ts = utcnow()
    user = User(
        id=id,
        email=email,
        password=hashed_password,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        created_ts=created_ts,
        last_modified_ts=created_ts,
        deleted_ts=None)
    db.session.add(user)
    db.session.flush()
    db.session.commit()
    return user


@trace('debug')
def get_user_by_id(user_id):
    filter_condition = User.id == user_id
    user = User.query.filter(filter_condition).one()
    return user


@trace('debug')
def delete_user(user_to_delete):
    db.session.query(User).filter(User.id == user_to_delete.id).delete()
    db.session.commit()


# def update_user(id, data):
@trace('debug')
def update_user(user_to_update, data):
    user_to_update.email = str.lower(data.get('email')) if data.get('email') else None
    if data.get('password'):
        user_to_update.password = generate_password_hash(data.get('password'), method='sha512')
    user_to_update.first_name = data.get('first_name')
    user_to_update.middle_name = data.get('middle_name')
    user_to_update.last_name = data.get('last_name')
    user_to_update.last_modified_ts = utcnow()
    db.session.add(user_to_update)
    db.session.commit()
    return user_to_update


@trace('debug')
def update_user_password(data, token):
    serializer = URLSafeTimedSerializer(current_app.config['RESETPASS_SECRET_KEY'])
    try:
        user_id = serializer.loads(
            token,
            salt=current_app.config['RESETPASS_SALT'],
            max_age=current_app.config['RESETPASS_EXPIRATION']
        )
        user_to_update = User.query.filter(User.id == user_id).one()
    except:
        return False

    if data.get('password'):
        user_to_update.password = generate_password_hash(data.get('password'), method='sha512')
        user_to_update.is_confirmed = True
        user_to_update.last_modified_ts = utcnow()
        db.session.add(user_to_update)
        db.session.commit()

    return user_to_update


@trace('debug')
def create_resetpass_token(id):
    serializer = URLSafeTimedSerializer(current_app.config['RESETPASS_SECRET_KEY'])
    return serializer.dumps(id, salt=current_app.config['RESETPASS_SALT'])


@trace('debug')
def get_user_by_token(token):
    serializer = URLSafeTimedSerializer(current_app.config['RESETPASS_SECRET_KEY'])
    try:
        user_id = serializer.loads(
            token,
            salt=current_app.config['RESETPASS_SALT'],
            max_age=current_app.config['RESETPASS_EXPIRATION']
        )
        user = User.query.filter(User.id == user_id).one()
    except:
        return False

    return user


@trace('debug')
def get_userid_by_email(email):
    email_lower = str.lower(email) if email else None
    try:
        user = User.query.filter(User.email == email_lower).one()
    except:
        return False

    return user.id