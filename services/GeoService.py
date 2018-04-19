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
        print('Geo unfiltered: ', events)

        filtered_events = []

        for x in events:

            print(user_lat, x.latitude)
            print(user_lng, x.longitude)

            lat_delta = abs(user_lat-x.latitude)
            lng_delta = abs(user_lng-x.longitude)

            print(lng_delta, lat_delta)

            lng_km = longitude_to_km(lng_delta, user_lat)
            lat_km = latitude_to_km(lat_delta)

            print(lng_km, lat_km)

            if lng_km ** 2 + lat_km ** 2 <= search_radius_km ** 2:
                filtered_events.append(x)

        print('Geo filtered: ', filtered_events)

        return filtered_events

