from flask import Flask, jsonify, render_template, request, make_response
from query import ApiQuery
from logger import Logger
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
from AuthModels import Users
from models import DatabaseClient
import datetime

db = DatabaseClient()
app = Flask(__name__)
log = Logger().custom_logger()
query = ApiQuery(log)
app.config['SECRET_KEY'] = 'Th1s1ss3asdascr12ffag2f23t'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        token = token.replace('Bearer ','').strip()
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        print(data)
        current_user = db.session.query(Users).filter_by(public_id=data['public_id']).first()
        # print(f"Error: {err}")
        # return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator


@app.route('/register', methods=['GET', 'POST'])
def signup_user():
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return jsonify({'data': 'Content-Type not supported! Expected Content-Type: application/json'})

        raw_data = str(request.data)
        if len(raw_data) <= 3:
            return jsonify({'data': 'Password or Name are required fields'})
        data = request.get_json()
        if 'password' not in data.keys():
            return jsonify({'data': 'Password or Name are required fields'})
        hashed_password = generate_password_hash(data['password'], method='sha256')

        new_user = Users(public_id=int(str(uuid.uuid4().int)[:10]), name=data['name'], password=hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'registered successfully'})
    elif request.method == 'GET':
        return render_template('register.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        raw_data = str(request.data)
        if len(raw_data) <= 3:
            return jsonify({'data': 'Password or Name are required fields'})
        auth = request.get_json()
        if not auth or not auth.get("name") or not auth.get("password"):
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
        user = db.session.query(Users).filter_by(name=auth.get("name")).first()
        print(user.password)
        if check_password_hash(user.password, auth.get("password")):
            token = jwt.encode(
                {
                    'public_id': user.public_id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)
                },
                app.config['SECRET_KEY'],
                "HS256"
            )
            return jsonify({'token': token})

        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
    elif request.method == 'GET':
        return render_template('login.html')
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/cars/getAllData', methods=['GET'])
@token_required
def get_all_car_data(*args):
    return jsonify({'data': query.get_all_car_data()})


@app.route('/gearboxes/getAll', methods=['GET'])
@token_required
def get_all_gearboxes():
    return jsonify({'data': query.get_all_gearboxes()})


@app.route('/categories/getAll', methods=['GET'])
@token_required
def get_all_categories():
    return jsonify({'data': query.get_all_categories()})


@app.route('/models/getAll', methods=['GET'])
@token_required
def get_all_models():
    return jsonify({'data': query.get_all_models()})


@app.route('/brands/getAll', methods=['GET'])
@token_required
def get_all_brands():
    return jsonify({'data': query.get_all_brands()})


@app.route('/brands/getWithModels', methods=['GET'])
@token_required
def get_model_by_brand():
    return jsonify({'data': query.get_model_by_brand()})


if __name__ == '__main__':
    app.run(debug=True)
