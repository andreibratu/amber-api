from flask import request, jsonify
from flask_api import status
from flask_jwt import jwt_required

from app import app
from services.EventService import EventService


@app.route('/event/', methods=['POST'])
@jwt_required()
def add_event_endpoint():
    payload = request.get_json()
    event = EventService.add_event(payload['user_id'], payload['name'], payload['address'], payload['start_date'],
                                   payload['end_date'], payload['latitude'], payload['longitude'])
    if not event:
        return 'Time frame taken by other event', status.HTTP_409_CONFLICT
    else:
        return jsonify(event), status.HTTP_200_OK


@app.route('/event/<int:event_id>/', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def event_endpoint(event_id):
    if request.method == 'GET':
        events = EventService.get_event_by_id(event_id)
        if not events:
            return 'Resource not found', status.HTTP_404_NOT_FOUND
        else:
            return jsonify(events), status.HTTP_200_OK
    if request.method == 'PUT':
        payload = request.get_json()
        event = EventService.update_event(event_id, payload['name'], payload['address'],
                                          payload['start_date'], payload['end_date'],
                                          payload['latitude'], payload['longitude'])
        if not event:
            return 'Event not found', status.HTTP_404_NOT_FOUND
        else:
            return jsonify(event), status.HTTP_200_OK
    if request.method == 'DELETE':
        result = EventService.delete_event(event_id)
        if not result:
            return 'Event not found', status.HTTP_404_NOT_FOUND
        else:
            return 'Deleted', status.HTTP_200_OK


@app.route('/event/available_events/<int:user_id>/', methods=['GET'])
@jwt_required()
def user_available_events_endpoint(user_id):
    payload = request.get_json()
    return EventService.get_available_events(user_id, payload['longitude'], payload['latitude'])


@app.route('/event/user/<int:user_id>/', methods=['GET', 'POST', 'DELETE'])
@jwt_required()
def user_event_endpoint(user_id):
    if request.method == 'GET':
        return jsonify(EventService.get_user_events(user_id)), status.HTTP_200_OK
    if request.method == 'POST':
        event_id = request.get_json()['event_id']
        result = EventService.add_user_to_event(user_id, event_id)
        if result == -1:
            return "Resource not found", status.HTTP_404_NOT_FOUND
        elif result == -2:
            return "Time frame taken another event", status.HTTP_409_CONFLICT
    if request.method == 'DELETE':
        event_id = request.get_json()['event_id']
        result = EventService.user_abandon_event(user_id, event_id)
        if not result:
            return 'Resource not found', status.HTTP_404_NOT_FOUND
        else:
            return jsonify(EventService.get_user_events(user_id)), status.HTTP_200_OK


@app.route('/event/<int:event_id>/messages/', methods=['GET'])
@jwt_required()
def event_messages_endpoint(event_id):
    return EventService.get_event_messages(event_id)
