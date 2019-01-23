from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def reset_database():
    db.drop_all()
    db.create_all()


def drop_database():
    db.drop_all()


def create_database():
    db.create_all()
