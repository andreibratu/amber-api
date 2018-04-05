from flask import request, jsonify
from flask_api import status
from flask_jwt import jwt_required

from app import app
from services.UserService import UserService


@app.route('/', methods=['GET'])
def hello():
    return 'Hi there cutie'


@app.route('/user/', methods=['POST'])
def register_user():
    payload = request.get_json()
    user = UserService.register_user(email=payload['email'], password=payload['password'])
    if not user:
        return 'Email already used', status.HTTP_409_CONFLICT
    else:
        return jsonify(user), status.HTTP_200_OK


@app.route('/user/<int:user_id>/', methods=['GET', 'PUT'])
@jwt_required()
def user_resource(user_id):
    if request.method == 'GET':
        user = UserService.get_user_by_id(user_id=user_id)
        if not user:
            return 'User does not exist', status.HTTP_404_NOT_FOUND
        else:
            return jsonify(user), status.HTTP_200_OK
    if request.method == 'PUT':
        payload = request.get_json()
        user = UserService.update_user(user_id, payload['age'], payload['bio'],
                                       payload['first_name'], payload['given_name'])
        if not user:
            return 'User does not exist', status.HTTP_404_NOT_FOUND
        else:
            return jsonify(user), status.HTTP_200_OK
