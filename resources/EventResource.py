import flask_jwt
from flask import request, jsonify
from flask_api import status
from flask_jwt import jwt_required

from app import app
from services.EventService import EventService


@app.route('/event', methods=['POST', 'GET'], strict_slashes=False)
@jwt_required()
def event_endpoint():
    if request.method == 'POST':

        payload = request.get_json()
        user_id = flask_jwt.current_identity
        event = EventService.add_event(user_id=user_id, title=payload['title'],
                                       description=payload['description'], busytime=payload['busyTime'],
                                       place=payload['place'])

        if not event:
            return 'Time frame taken by other event', status.HTTP_409_CONFLICT

        else:
            return jsonify(event), status.HTTP_200_OK

    if request.method == 'GET':

        event_id = request.args.get('event_id')
        events = EventService.get_event_by_id(event_id)

        if not events:
            return 'Not found', status.HTTP_404_NOT_FOUND
        else:
            return jsonify(events), status.HTTP_200_OK


@app.route('/event/available-events', methods=['GET'], strict_slashes=False)
@jwt_required()
def user_available_events_endpoint():
    user_id = flask_jwt.current_identity
    lng = float(request.args.get('lng'))
    lat = float(request.args.get('lat'))
    search_radius = float(request.args.get('searchRadius'))
    return jsonify(EventService.get_available_events(user_id=user_id, user_lng=lng,
                                                     user_lat=lat, search_radius=search_radius)), status.HTTP_200_OK


@app.route('/event/user', methods=['GET', 'PATCH'], strict_slashes=False)
@jwt_required()
def user_event_endpoint():
    if request.method == 'GET':
        user_id = flask_jwt.current_identity.id
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        return jsonify(EventService.get_user_events(
            user_id=user_id, user_lat=lat, user_lng=lng)), status.HTTP_200_OK

    if request.method == 'PATCH':

        payload = request.get_json()
        user_id = flask_jwt.current_identity.id
        result = EventService.add_user_to_event(user_id, payload['eventId'])

        if result == -1:
            return 'Not found', status.HTTP_404_NOT_FOUND

        elif result == -2:
            return 'Time frame taken by another event', status.HTTP_409_CONFLICT

        else:
            return jsonify(result), status.HTTP_200_OK
