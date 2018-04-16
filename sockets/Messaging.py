from flask_socketio import join_room, send, leave_room

from app import socketIO


@socketIO.on('join')
def on_join(data):
    name = data['name']
    room = data['room']
    join_room(room)
    send(name + ' has joined the event', room=room)


@socketIO.on('leave')
def on_leave(data):
    name = data['name']
    room = data['room']
    leave_room(room)
    send(name + ' has left the event', room=room)


@socketIO.on('message')
def on_message(data):
    text = data['text']
    date = data['date']
    user_id = data['user_id']
    event_id = data['event_id']
