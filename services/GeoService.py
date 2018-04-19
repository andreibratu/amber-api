from math import cos, radians

LAT_TO_KM = 111.13
LNG_TO_KM = 111.32


def longitude_to_km(lng_delta, lat):
    return lng_delta * LNG_TO_KM * cos(radians(lat))


def latitude_to_km(lat_delta):
    return lat_delta * LAT_TO_KM


class GeoService:

    @staticmethod
    def filter_events_by_location(events, user_lng, user_lat, search_radius_km = 10):
        events = [x for x in events if (
                longitude_to_km(abs(user_lng - x.longitude), user_lat) ** 2 +
                latitude_to_km(abs(user_lat - x.latitude)) ** 2
                < search_radius_km ** 2)
                ]

        return events

