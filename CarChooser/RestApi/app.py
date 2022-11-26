from flask import Flask
from sqlalchemy_utils import database_exists, create_database
from CarChooser.Configs.config_utils import get_config, Config_env, Config_type
from .extensions import (
    bcrypt,
    db
)


def create_app(config_env):
    """
    Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    """
    config_object = get_config(
            Config_type.API.value, 
            Config_env[config_env].value
        )

    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config_object)
    # print(f"ANDRIIPX: {db.engine.url}")
    register_extensions(app)
    register_blueprints(app)
    app.app_context().push()
    engine = db.engine
    try:
        if not database_exists(engine.url):
            create_database(engine.url)
    except Exception as err:
        print(f"Some error with creating database with url: {engine.url}: {err}")
    db.create_all()
    # register_errorhandlers(app)
    # register_shellcontext(app)
    # register_commands(app)
    # configure_logger(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    # cache.init_app(app)
    db.init_app(app)
    # csrf_protect.init_app(app)
    # login_manager.init_app(app)
    # debug_toolbar.init_app(app)
    # migrate.init_app(app, db)
    # flask_static_digest.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    from CarChooser.RestApi.API.auth.views import auth_blueprint
    from CarChooser.RestApi.API.carInfo.views import cars_blueprint
    # from API.auth.views import auth_blueprint
    # from API.carInfo.views import cars_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(cars_blueprint)
    # app.register_blueprint(user.views.blueprint)
#
#
# def register_errorhandlers(app):
#     """Register error handlers."""
#
#     def render_error(error):
#         """Render error template."""
#         # If a HTTPException, pull the `code` attribute; default to 500
#         error_code = getattr(error, "code", 500)
#         return render_template(f"{error_code}.html"), error_code
#
#     for errcode in [401, 404, 500]:
#         app.errorhandler(errcode)(render_error)
#     return None

#
# def register_shellcontext(app):
#     """Register shell context objects."""
#
#     def shell_context():
#         """Shell context objects."""
#         return {"db": db, "User": user.models.User}
#
#     app.shell_context_processor(shell_context)
#
#
# def register_commands(app):
#     """Register Click commands."""
#     app.cli.add_command(commands.test)
#     app.cli.add_command(commands.lint)

#
# def configure_logger(app):
#     """Configure loggers."""
#     handler = logging.StreamHandler(sys.stdout)
#     if not app.logger.handlers:
#         app.logger.addHandler(handler)
