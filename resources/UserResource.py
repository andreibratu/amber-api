import flask_jwt
from flask import request, jsonify
from flask_api import status
from flask_jwt import jwt_required
from app import app
from services.UserService import UserService


@app.route('/', methods=['GET'], strict_slashes=False)
def hello():
    return 'Hi there cutie'


@app.route('/register', methods=['POST'], strict_slashes=False)
def register_user():

    payload = request.get_json()
    user = UserService.register_user(email=payload['username'], password=payload['password'])

    if not user:
        return 'Email already used', status.HTTP_409_CONFLICT
    else:
        return jsonify(user), status.HTTP_200_OK


@app.route('/user/', methods=['GET', 'PUT'], strict_slashes=False)
@jwt_required()
def user_resource():

    if request.method == 'GET':
        user_id = flask_jwt.current_identity.id
        user = UserService.get_user_by_id(user_id=user_id)

        if not user:
            return 'User does not exist', status.HTTP_404_NOT_FOUND
        else:
            return jsonify(user), status.HTTP_200_OK

    if request.method == 'PUT':
        payload = request.get_json()
        user_id = flask_jwt.current_identity.id
        user = UserService.update_user(user_id, payload['age'], payload['bio'],
                                       payload['firstName'], payload['lastName'], payload['interests'])

        if not user:
            return 'User does not exist', status.HTTP_404_NOT_FOUND
        else:
            return jsonify(user), status.HTTP_200_OK


@app.route('/user/people', methods=['GET'], strict_slashes=False)
@jwt_required()
def people_endpoint():
    people = UserService.get_people()
    return jsonify(people), status.HTTP_200_OK
