from datetime import datetime
from app.models import Event, User, BusyTime, Place
from services.InterestService import InterestService
from services.BusyTimeService import BusyTimeService
from services.GeoService import GeoService
from app.extensions import db


class EventService:
    @staticmethod
    def add_event(user_id, title, description, busytime, place):
        def string_to_timestamp(date, time):
            time_string = date + ' ' + time
            dt = datetime.strptime(time_string, '%Y-%m-%d %H:%M')
            return int(dt.timestamp())

        start = string_to_timestamp(busytime['startDate'], busytime['startTime'])
        end = string_to_timestamp(busytime['endDate'], busytime['endTime'])

        if BusyTimeService.is_time_period_available(user_id, start, end):
            busytime = BusyTime(start=start, end=end)
            place = Place(name=place['name'], address=place['address'], lat=place['lat'],
                          lng=place['lng'], thumbnail=place['thumbnail'], type=place['type'])

            new_event = Event(title=title, description=description, busytime=busytime, place=place)

            user_creating_event = User.query.get(user_id)
            new_event.users.append(user_creating_event)

            db.session.add(new_event)
            db.session.commit()

            return new_event
        else:
            return None

    @staticmethod
    def get_event_by_id(event_id):
        return Event.query.get(event_id)

    @staticmethod
    def get_user_events(user_id, user_lat, user_lng):
        user = User.query.get(user_id)
        if not user:
            return None
        else:
            events = user.events
            for event in events:
                dist, eta = GeoService.calculate_dist_eta(user_lng=user_lng, user_lat=user_lat,
                                                          event_lat=event.place.lat, event_lng=event.place.lng)
                event.dist = dist
                event.eta = eta
            return events

    @staticmethod
    def add_user_to_event(user_id, event_id):
        user = User.query.get(user_id)
        event = Event.query.get(event_id)
        if not user or not event:
            return -1
        elif not BusyTimeService.is_time_period_available(
                user_id, event.busytime.start, event.busytime.end):
            return -2
        else:
            event.users.append(user)
            db.session.commit()
            return event

    @staticmethod
    def get_available_events(user_id, user_lng, user_lat, search_radius):
        filters = [BusyTimeService.events_by_availability_filter_builder(user_id),
                   GeoService.events_by_location_filter_builder(user_lng, user_lat, search_radius),
                   InterestService.events_by_interests_filter_builder(user_id)
                   ]

        events = Event.query.all()

        for f in filters:
            events = list(filter(f, events))

        for event in events:
            dist, eta = GeoService.calculate_dist_eta(user_lng=user_lng, user_lat=user_lat,
                                                      event_lat=event.place.lat, event_lng=event.place.lng)
            event.dist = dist
            event.eta = eta

        return events

    @staticmethod
    def leave_event(event_id, user_id):
        event = Event.query.get(event_id)
        user = Event.query.get(user_id)

        if not event or not user:
            return None
        else:
            event.users = [user for user in event.users if user.id != user_id]
            db.session.commit()
            return event

