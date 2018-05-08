import datetime

from flask.json import JSONEncoder

from app.models import User, Event, BusyTime, Place


class Encoder(JSONEncoder):
    def default(self, o):
        def encode_interests(interests):
            interest_dict = {interest.category: [] for interest in interests}
            for interest in interests:
                interest_dict[interest.category].append(interest.label)

            return interest_dict

        if isinstance(o, User):
            return {
                'username': o.email,
                'firstName': o.first_name,
                'lastName': o.given_name,
                'age': o.age,
                'bio': o.bio,
                'firstLogin': o.first_time,
                'interests': encode_interests(o.interests)
            }
        if isinstance(o, Event):
            if not hasattr(o, 'eta'):
                o.eta = ''
            if not hasattr(o, 'dist'):
                o.dist = ''

            return {
                'id': o.id,
                'title': o.title,
                'description': o.description,
                'busyTime': o.busytime,
                'place': o.place,
                'eta': o.eta,
                'dist': o.dist
            }
        if isinstance(o, BusyTime):
            return {
                'startDate': datetime.datetime.fromtimestamp(o.start).__str__(),
                'endDate': datetime.datetime.fromtimestamp(o.end).__str__()
            }
        if isinstance(o, Place):
            return {
                'name': o.name,
                'address': o.address,
                'lat': o.lat,
                'lng': o.lng,
                'thumbnail': o.thumbnail
            }
