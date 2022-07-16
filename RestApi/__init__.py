# """Flask app initialization via factory pattern."""
# from flask import Flask
# from flask_bcrypt import Bcrypt
# from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
# import os
#
# cors = CORS()
# db = SQLAlchemy()
# bcrypt = Bcrypt()
#
#
# def get_active_config() -> str or None:
#     list_of_configs = ["DevelopmentConfig", "TestingConfig", "ProductionConfig"]
#     for item in list_of_configs:
#         if str(os.getenv(item, "0")) == "1":
#             return item
#     raise SystemError(f"Can not find allowed config")
#
#
# def create_app():
#     app = Flask(__name__)
#     config_object = "config." + get_active_config()
#     app.config.from_object(config_object)
#     from API import api_bp
#     app.register_blueprint(api_bp)
#
#     cors.init_app(app)
#     db.init_app(app)
#     bcrypt.init_app(app)
#     return app
