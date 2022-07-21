from flask import current_app, jsonify, request, Blueprint, render_template
from functools import wraps
import jwt
from CarChooser.RestApi.models import User
from CarChooser.RestApi.CarQuery import CarApiQuery
from CarChooser.Configs.logger import Logger

log = Logger().custom_logger()
query = CarApiQuery(log)

cars_blueprint = Blueprint('cars', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return {
                       "message": "Authentication Token is missing!",
                       "data": None,
                       "error": "Unauthorized"
                   }, 401
        try:
            auth_token = auth_header.split(" ")[1]
            data = jwt.decode(
                auth_token,
                current_app.config.get('SECRET_KEY'),
                algorithms=["HS256"]
            )
            current_user = User.get_by_id(data["sub"])
            if current_user is None:
                return {
                           "message": "Invalid Authentication token!",
                           "data": None,
                           "error": "Unauthorized"
                       }, 401
        except Exception as e:
            return {
                       "message": "Something went wrong",
                       "data": None,
                       "error": str(e)
                   }, 500

        return f(current_user, *args, **kwargs)

    return decorated


@cars_blueprint.route('/', methods=['GET'])
def get_index(*args):
    return render_template('index.html')


@cars_blueprint.route('/cars/dashboard', methods=['GET'])
def get_dashboard(*args):
    return render_template('dashboard.html')


@cars_blueprint.route('/cars/getAllData', methods=['GET'])
@token_required
def get_all_car_data(*args):
    return jsonify({'data': query.get_all_car_data()})


@cars_blueprint.route('/gearboxes/getAll', methods=['GET'])
@token_required
def get_all_gearboxes(*args):
    return jsonify({'data': query.get_all_gearboxes()})


@cars_blueprint.route('/categories/getAll', methods=['GET'])
@token_required
def get_all_categories(*args):
    return jsonify({'data': query.get_all_categories()})


@cars_blueprint.route('/models/getAll', methods=['GET'])
@token_required
def get_all_models(*args):
    return jsonify({'data': query.get_all_models()})


@cars_blueprint.route('/brands/getAll', methods=['GET'])
@token_required
def get_all_brands(*args):
    return jsonify({'data': query.get_all_brands()})


@cars_blueprint.route('/brands/getWithModels', methods=['GET'])
@token_required
def get_model_by_brand(*args):
    return jsonify({'data': query.get_model_by_brand()})
