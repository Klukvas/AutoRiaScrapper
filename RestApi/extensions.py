"""
https://github.com/cookiecutter-flask/cookiecutter-flask/blob/c78027c298d329f0c9c959915b0b474c2b9a1a2f/%7B%7Bcookiecutter.app_name%7D%7D/%7B%7Bcookiecutter.app_name%7D%7D/extensions.py#L1
"""

# from flask_caching import Cache
# from flask_debugtoolbar import DebugToolbarExtension
# from flask_login import LoginManager
# from flask_migrate import Migrate
# from flask_static_digest import FlaskStaticDigest
# from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
# csrf_protect = CSRFProtect()
# login_manager = LoginManager()
db = SQLAlchemy()
# migrate = Migrate()
# cache = Cache()
# debug_toolbar = DebugToolbarExtension()
# flask_static_digest = FlaskStaticDigest()