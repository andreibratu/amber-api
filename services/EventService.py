from app.models import Event, User, BusyTime
from services.BusyTimesService import BusyTimesService
from services.GeoService import GeoService
from app.extensions import db


class EventService:

    @staticmethod
    def add_event(user_id, name, address, start_date, end_date, latitude, longitude):

        if BusyTimesService.is_time_period_available(user_id, start_date, end_date):

            new_event = Event(name=name, address=address, latitude=latitude, longitude=longitude)

            user_creating_event = User.query.get(user_id)
            new_event.users.append(user_creating_event)

            busy_time = BusyTime(start_date= start_date, end_date=end_date)

            new_event.busytime = busy_time

            db.session.add(new_event)
            db.session.commit()

            return new_event
        else:
            return None

    @staticmethod
    def get_event_by_id(event_id):
        return Event.query.get(event_id)

    @staticmethod
    def update_event(event_id, name, address, start_date, end_date, latitude, longitude):
        event = Event.query.get(event_id)
        if not event:
            return event
        event.name = name
        event.address = address
        event.busytime = BusyTime(start_date=start_date, end_date=end_date)
        event.latitude = latitude
        event.longitude = longitude
        db.session.commit()
        return event

    @staticmethod
    def delete_event(event_id):
        event = Event.query.get(event_id)
        if event:
            db.session.delete(event)
            db.session.commit()
            return True
        else:
            return False

    @staticmethod
    def get_user_events(user_id):
        user = User.query.get(user_id)
        if not user:
            return None
        else:
            return user.events

    @staticmethod
    def add_user_to_event(user_id, event_id):
        user = User.query.get(user_id)
        event = Event.query.get(event_id)
        if not user or not event:
            return -1
        elif not BusyTimesService.is_time_period_available(
                user.busytimes, event.busytime.start_date, event.busytime.end_date):
            return -2
        else:
            event.users.append(user)
            db.session.commit()
            return 1

    @staticmethod
    def user_abandon_event(user_id, event_id):
        user = User.query.get(user_id)
        event = Event.query.get(event_id)
        if not user or not event:
            return False
        else:
            event.users = [x for x in event.users if x.id != user_id]
            db.session.commit()
            return True

    @staticmethod
    def get_event_messages(event_id):
        event = Event.query.get(event_id)
        if not event:
            return []
        else:
            return event.messages

    @staticmethod
    def get_available_events(user_id, user_lng, user_lat, search_radius):
        events = Event.query.all()
        events = GeoService.filter_events_by_location(events, user_lng, user_lat, search_radius)

        user = User.query.get(user_id)
        user_busytimes = [x.busytime for x in user.events]

        events = BusyTimesService.filter_events_by_availability(events, user_busytimes)
        return events

