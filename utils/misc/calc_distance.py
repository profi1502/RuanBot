from math import radians, cos, sin, asin, sqrt, ceil
from aiogram import types

from utils.misc.cityInfo import get_city
from utils.db_api.db_commands import get_location
from utils.misc import show_on_gmaps

EARTH_RADIUS = 6371


def calc_distance(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers is 6371
    km = EARTH_RADIUS * c
    return ceil(km * 1000)


async def choose_shortest(location: types.Location):
    distances = list()

    for address_id, pharmacy_name, ph_latitude, ph_longitude \
            in (await get_location(get_city(location.latitude, location.longitude))):
        distances.append((address_id, pharmacy_name, calc_distance(location.latitude, location.longitude,
                                                                   float(ph_latitude), float(ph_longitude)),
                          show_on_gmaps.show(float(ph_latitude), float(ph_longitude)),
                          {float(ph_latitude), float(ph_longitude)}
                          ))
    d_filter = filter(lambda x: x[2] < 10000, distances)
    return sorted(d_filter, key=lambda x: x[2])[:5]
