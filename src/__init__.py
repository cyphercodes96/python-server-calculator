from flask_login import LoginManager
from .database.models import User

login_manager = LoginManager()


@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == id).first()
