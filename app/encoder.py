import datetime

from flask.json import JSONEncoder

from app.models import User, Event, BusyTime


class Encoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, User):
            return {
                'username': o.email,
                'firstName': o.first_name,
                'lastName': o.given_name,
                'age': o.age,
                'bio': o.bio,
                'firstLogin': o.first_time,
                'interests': {interest.category: interest.label for interest in o.interests}
            }
        if isinstance(o, Event):
            return {
                'id': o.id,
                'name': o.name,
                'address': o.address,
                'busyTime': o.busytime,
                'lat': o.latitude,
                'lng': o.longitude,
                'users': o.users
            }
        if isinstance(o, BusyTime):
            return {
                'startDate': datetime.datetime.fromtimestamp(o.start_date).__str__(),
                'endDate': datetime.datetime.fromtimestamp(o.end_date).__str__()
            }