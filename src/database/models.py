import pytz
from dateutil import tz
from sqlalchemy import BigInteger
from src.database import db


class Token:
    def __init__(self, access_token):
        self.access_token = access_token


class AwareDateTime(db.TypeDecorator):

    impl = db.DateTime

    def process_result_value(self, value, dialect):
        if value and not value.tzinfo:
            value = value.replace(tzinfo=pytz.utc)
        return value

    def process_bind_param(self, value, dialect):
        if value:
            return value.astimezone(tz.gettz('UTC'))
        else:
            return value


class User(db.Model):
    id = db.Column(db.String(300), primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    middle_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_ts = db.Column(AwareDateTime)
    last_modified_ts = db.Column(AwareDateTime)
    deleted_ts = db.Column(AwareDateTime)

    def __init__(self,
                 id=None,
                 email=None,
                 password=None,
                 first_name=None,
                 last_name=None,
                 middle_name=None,
                 created_ts=None,
                 last_modified_ts=None,
                 deleted_ts=None):
        self.id = id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.created_ts = created_ts
        self.last_modified_ts = last_modified_ts
        self.deleted_ts = deleted_ts


class Operation(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.String(300), db.ForeignKey('user.id'), nullable=False)
  created_ts = db.Column(AwareDateTime)
  operator = db.Column(db.String(1), nullable=False)
  number0 = db.Column(db.Float, nullable=True)
  number1 = db.Column(db.Float, nullable=True)
  result = db.Column(db.Float, nullable=False)

  def __init__(self,
               id=None,
               user_id=None,
               created_ts=None,
               number0=None,
               number1=None,
               result=None,
               operator=None):
      self.id = id
      self.user_id = user_id
      self.created_ts = created_ts
      self.number0 = number0
      self.number1 = number1
      self.result = result
      self.operator = operator