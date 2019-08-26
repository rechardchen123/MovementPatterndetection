# !/usr/bin/env python3
# -*- coding: utf-8 -*
from math import sqrt, sin, cos, radians, asin, fabs, pi, atan2

EARTH_RADIUS = 6378.1
n_mile = 1.852


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
    lat0 = radians(float(lat0))
    lat1 = radians(float(lat1))
    lng0 = radians(float(lng0))
    lng1 = radians(float(lng1))

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = sin(dlat / 2.) ** 2 + cos(lat0) * cos(lat1) * sin(dlng / 2.) ** 2
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))
    distance1 = distance / n_mile
    return distance1

