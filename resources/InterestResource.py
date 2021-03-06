from flask import jsonify
from flask_jwt import jwt_required
from app import app
from services.InterestService import InterestService
from flask_api import status


@app.route('/interests/', methods=['GET'], strict_slashes=False)
@jwt_required()
def interests_endpoint():
    return jsonify(InterestService.interests), status.HTTP_200_OK
