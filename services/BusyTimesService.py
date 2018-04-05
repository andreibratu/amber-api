from app.models import User, Event


class BusyTimesService:

    @staticmethod
    def get_user_busy_times(user_id):
        user = User.query.filter(User.id == user_id)
        busytimes = []
        for x in user.events:
            busytimes.append(x.busytime)
        return busytimes

    @staticmethod
    def time_periods_overlap(first_time_period_start_date, first_time_period_end_date,
                             second_time_period_start_date, second_time_period_end_date):
        return second_time_period_start_date <= first_time_period_start_date <= second_time_period_end_date \
               or second_time_period_start_date <= first_time_period_end_date <= second_time_period_end_date

    @staticmethod
    def filter_events_by_availability(events, user_busytimes):
        return [x for x in events for y in user_busytimes if not BusyTimesService.time_periods_overlap(
            x.busytime.start_date, x.busytime.end_date, y.start_date, y.end_date
        )]

    @staticmethod
    def is_time_period_available(user_busytimes, user_given_start_date, user_given_end_date):
        return [x for x in user_busytimes.busytimes if BusyTimesService.time_periods_overlap(
            x.start_date, x.end_date, user_given_start_date, user_given_end_date)] == []
        # No event conflicts with the given time period
