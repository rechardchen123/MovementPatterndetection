# !/usr/bin/env python3
# -*- coding: utf-8 -*
from math import sqrt, sin, cos, pi, acos
from clustering_and_conflict_detection.distance_transform import get_distance_hav
from geohelper import bearing


def cpa_calculation(x1, y1, x2, y2, v1, v2, heading1, heading2):
    '''
    Time to closest point of approach
    :param x1: latitude of ship 1
    :param y1: longitude of ship 1
    :param x2: latitude of ship 2
    :param y2: longitude of ship 2
    :param v1: speed of ship 1
    :param v2: speed of ship 2
    :param heading1: the heading of ship 1
    :param heading2: the heading of ship 2
    :return: the tcpa and dcpa
    '''
    distance = get_distance_hav(x1, y1, x2, y2)
    alpha = heading2 - heading1
    if alpha > 180:
        alpha -= 360
    elif alpha < -180:
        alpha += 360
    # relative speed
    relative_speed = sqrt(v2 ** 2 + v1 ** 2 - 2 * v1 * v2 * cos(alpha / 180.0 * pi))
    Q = acos((relative_speed ** 2 + v2 ** 2 - v1 ** 2) / (2 * relative_speed * v2)) * 180.0 / pi

    # relative course
    if alpha > 0:
        relative_course = heading2 + Q
    else:
        relative_course = heading2 - Q

    # relative bearing
    bearing1 = bearing.initial_compass_bearing(float(x2), float(y2), float(x1), float(y1)) - relative_course
    DCPA = distance * sin(bearing1 * pi / 180.0)
    TCPA = distance * cos(bearing1 * pi / 180.0) / relative_speed
    return DCPA, TCPA
