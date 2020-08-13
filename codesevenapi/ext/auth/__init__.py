from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager

def init_app(app):
    login_manager.init_app(app)
