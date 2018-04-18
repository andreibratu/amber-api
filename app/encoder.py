import datetime

from flask.json import JSONEncoder

from app.models import User, Event, BusyTime


class Encoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, User):
            return {
                'id': o.id,
                'email': o.email,
                'first_name': o.first_name,
                'given_name': o.given_name,
                'age': o.age,
                'bio': o.bio
            }
        if isinstance(o, Event):
            return {
                'id': o.id,
                'name': o.name,
                'address': o.address,
                'busytime': o.busytime,
                'latitude': o.latitude,
                'longitude': o.longitude,
                'users': o.users
            }
        if isinstance(o, BusyTime):
            return {
                'start_date': datetime.datetime.fromtimestamp(o.start_date).__str__(),
                'end_date': datetime.datetime.fromtimestamp(o.end_date).__str__()
            }