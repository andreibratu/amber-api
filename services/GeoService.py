from math import cos, radians, sqrt

LAT_TO_KM = 111.13
LNG_TO_KM = 111.32
KM_PER_MIN = float(5.0/3)


class GeoService:

    @staticmethod
    def calculate_dist_eta(event_lat, event_lng, user_lat, user_lng):
        def lng_to_km(lng_delta): return abs(lng_delta) * LNG_TO_KM * cos(radians(lng_delta))

        def lat_to_km(lat_delta): return abs(lat_delta) * LAT_TO_KM

        def dist(lng_km, lat_km): return sqrt(lng_km ** 2 + lat_km ** 2)

        dist = dist(lng_km=lng_to_km(user_lng-event_lng), lat_km=lat_to_km(event_lat-user_lat))
        eta = dist/KM_PER_MIN

        return dist, eta

    @staticmethod
    def events_by_location_filter_builder(lng, lat, search_radius_km):
        def lng_to_km(lng_delta): return abs(lng_delta) * LNG_TO_KM * cos(radians(lng_delta))

        def lat_to_km(lat_delta): return abs(lat_delta) * LAT_TO_KM

        def dist(lng_km, lat_km): return sqrt(lng_km ** 2 + lat_km ** 2)

        def pythagoras(lng_km, lat_km, radius): return dist(lng_km=lng_km, lat_km=lat_km) <= sqrt(radius)

        return lambda event: pythagoras(lng_to_km(lng-event.longitude), lat_to_km(lat-event.latitude), search_radius_km)

