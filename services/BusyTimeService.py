from services.UserService import UserService
from functools import reduce


class BusyTimeService:

    @staticmethod
    def events_by_availability_filter_builder(user_id):
        def time_periods_overlap(ftpsd, ftped, stpsd, stped):
            return stpsd <= ftpsd <= stped or stpsd <= ftped <= stped \
                   or stpsd <= ftpsd <= stped or stpsd <= ftped <= stped

        busytimes = UserService.get_user_busy_times(user_id)

        if not busytimes:
            return lambda busytime: True

        return lambda event: reduce(
            (lambda x, y: x and y),
            map(
                (lambda busytime: not time_periods_overlap(
                    event.busytime.start, event.busytime.end, busytime.start, busytime.end)),
                busytimes
            )
        )

    @staticmethod
    def is_time_period_available(user_id, user_given_start_date, user_given_end_date):
        def time_periods_overlap(ftpsd, ftped, stpsd, stped): return stpsd <= ftpsd <= stped or stpsd <= ftped <= stped

        if user_given_end_date <= user_given_start_date:
            return False

        busytimes = UserService.get_user_busy_times(user_id)

        return list(
            filter((lambda busytime: time_periods_overlap(
                user_given_start_date, user_given_end_date, busytime.start, busytime.end)), busytimes)
        ) == []
        # No event conflicts with the given time period
