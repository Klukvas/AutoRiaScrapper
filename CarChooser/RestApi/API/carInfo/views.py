from flask import current_app, jsonify, request, Blueprint, render_template
from functools import wraps
import jwt

from CarChooser.RestApi.models import User
from CarChooser.RestApi.CarQuery import CarApiQuery
from CarChooser.Configs.logger import Logger
from CarChooser.Scrapper.AutoRia import ria_parser
from CarChooser.Scrapper.serializer import Serializer
from CarChooser.Scrapper.query import Query
from CarChooser.Configs.config_utils import get_config, Config_env, Config_type

import asyncio
import threading
from os import getenv


log = Logger().custom_logger()
query = CarApiQuery(log)
serializer = Serializer(log)
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


def run_scrapper():
    scrapper_query = Query(log)
    scrapper_api_keys = get_config(
        Config_type.SCRAPPER.value,
        Config_env[getenv('FLASK_ENV', 'Development')].value
    ).AUTO_RIA_API_KEYS
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    parser = ria_parser.AutoRiaParser(log, scrapper_api_keys, scrapper_query, serializer)
    loop.run_until_complete(
        parser.run_car_info_parser()
    )
    return True


@token_required
@cars_blueprint.route('/cars/startParse', methods=['POST'])
def start_parse(*args):
    th = threading.Thread(
        target=run_scrapper,
        daemon=True
    )
    th.start()
    return jsonify({'data': True})


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


@cars_blueprint.route('/cars/gearboxes/getAll', methods=['GET'])
@token_required
def get_all_gearboxes(*args):
    return jsonify({'data': query.get_all_gearboxes()})


@cars_blueprint.route('/cars/categories/getAll', methods=['GET'])
@token_required
def get_all_categories(*args):
    return jsonify({'data': query.get_all_categories()})


@cars_blueprint.route('/cars/models/getAll', methods=['GET'])
@token_required
def get_all_models(*args):
    print('asdasdasd123123123')
    return jsonify({'data': query.get_all_models()})


@cars_blueprint.route('/cars/brands/getAll', methods=['GET'])
@token_required
def get_all_brands(*args):
    return jsonify({'data': query.get_all_brands()})


@cars_blueprint.route('/cars/brands/getWithModels', methods=['GET'])
@token_required
def get_model_by_brand(*args):
    return jsonify({'data': query.get_model_by_brand()})

@cars_blueprint.route('/cars/brands/getcounByCategory', methods=['GET'])
@token_required
def get_count_by_category(*args):
    return jsonify({'data': query.get_count_by_category()})