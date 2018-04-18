from flask import request, jsonify
from flask_api import status
from flask_jwt import jwt_required

from app import app
from services.EventService import EventService


@app.route('/event', methods=['POST', 'GET', 'PUT', 'DELETE'], strict_slashes=False)
@jwt_required()
def event_endpoint():

    if request.method == 'POST':

        payload = request.get_json()
        event = EventService.add_event(payload['user_id'], payload['name'], payload['address'], payload['start_date'],
                                       payload['end_date'], payload['latitude'], payload['longitude'])

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

    if request.method == 'PUT':

        payload = request.get_json()
        event = EventService.update_event(payload['event_id'], payload['name'], payload['address'],
                                          payload['start_date'], payload['end_date'],
                                          payload['latitude'], payload['longitude'])
        if not event:
            return 'Not found', status.HTTP_404_NOT_FOUND

        else:
            return jsonify(event), status.HTTP_200_OK

    if request.method == 'DELETE':

        event_id = request.args.get('event_id')
        result = EventService.delete_event(event_id)

        if not result:
            return 'Not found', status.HTTP_404_NOT_FOUND

        else:
            return 'Deleted', status.HTTP_200_OK


@app.route('/event/available_events', methods=['GET'], strict_slashes=False)
@jwt_required()
def user_available_events_endpoint():

    user_id = request.args.get('user_id')
    lng = request.args.get('lng')
    lat = request.args.get('lat')
    return jsonify(EventService.get_available_events(user_id, lng, lat)), status.HTTP_200_OK


@app.route('/event/user', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@jwt_required()
def user_event_endpoint():

    if request.method == 'GET':

        user_id = request.args.get('user_id')
        return jsonify(EventService.get_user_events(user_id)), status.HTTP_200_OK

    if request.method == 'POST':

        payload = request.get_json()['event_id']
        result = EventService.add_user_to_event(payload['user_id'], payload['event_id'])

        if result == -1:
            return 'Not found', status.HTTP_404_NOT_FOUND

        elif result == -2:
            return 'Time frame taken by another event', status.HTTP_409_CONFLICT

    if request.method == 'DELETE':

        user_id = request.args.get('user_id')
        event_id = request.args.get('event_id')
        result = EventService.user_abandon_event(user_id, event_id)

        if not result:
            return 'Not found', status.HTTP_404_NOT_FOUND

        else:
            return jsonify(EventService.get_user_events(user_id)), status.HTTP_200_OK


@app.route('/event/messages', methods=['GET'], strict_slashes=False)
@jwt_required()
def event_messages_endpoint(event_id):

    event_id = request.args.get('event_id')
    return jsonify(EventService.get_event_messages(event_id)), status.HTTP_200_OK
