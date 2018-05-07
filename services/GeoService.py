from math import cos, radians


class GeoService:

    @staticmethod
    def events_by_location_filter_builder(lng, lat, search_radius_km=10):
        LAT_TO_KM = 111.13
        LNG_TO_KM = 111.32

        def lng_to_km(lng_delta): return abs(lng_delta) * LNG_TO_KM * cos(radians(lng_delta))

        def lat_to_km(lat_delta): return abs(lat_delta) * LAT_TO_KM

        def pythagoras(lng_km, lat_km, radius): return lng_km ** 2 + lat_km ** 2 <= radius ** 2

        return lambda event: pythagoras(lng_to_km(lng-event.longitude), lat_to_km(lat-event.latitude), search_radius_km)

