from math import cos, radians

LATITUDE_TO_KM = 111.23
SEARCH_RADIUS_KM = 10


def longitude_to_km(longitude):
    return LATITUDE_TO_KM * cos(radians(longitude))


def latitude_to_km(latitude):
    return latitude * LATITUDE_TO_KM


class GeoService:

    @staticmethod
    def filter_events_by_location(events, user_longitude, user_latitude):
        return [x for x in events if (
                longitude_to_km(abs(user_longitude - x.longitude)) ** 2 +
                latitude_to_km(abs(user_latitude - x.latitude)) ** 2
                < 10 ^ 2)
                ]
