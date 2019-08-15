# !/usr/bin/env python3
# -*- coding: utf-8 -*
from geohelper import bearing
from math import sqrt, sin, cos, radians, asin, fabs

EARTH_RADIUS = 6378.1
n_mile = 1.852

def hav(theta):
    s = sin(theta / 2)
    return s * s


def get_distance_hav(lat0, lng0, lat1, lng1):
    '''
    Using haversine equation to calculate the distance between two points
    transfer the latitude and longitude into radian representation.
    :param lat0:
    :param lng0:
    :param lat1:
    :param lng1:
    :return: two points distance using nautical miles to represent
    '''
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))
    return distance / n_mile
