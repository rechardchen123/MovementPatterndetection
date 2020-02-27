# !/usr/bin/env python3
# -*- coding: utf-8 -*
from math import sqrt, sin, cos, pi, acos, fabs
from distance_transform import get_distance_hav
from geohelper import bearing


def relative_bearing(own_object_heading, object_bearing):
    '''
    :param own_object_heading: the first ship's heading
    :param object_bearing: the second ship's heading
    :return:
    '''
    a = own_object_heading - object_bearing
    if a > 0:
        relative_bearing = 360 - a
    else:
        relative_bearing = -a
    return relative_bearing


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
    if fabs(v1 - v2 <= 0.5):
        DCPA = 0
        TCPA = 0
        return DCPA, TCPA
    else:
        # relative distance
        distance = get_distance_hav(x1, y1, x2, y2)
        # relative bearing
        alpha = relative_bearing(heading1, heading2)
        # relative speed
        relative_speed = sqrt(v2 ** 2 + v1 ** 2 - 2 * v1 * v2 * cos(alpha / 180.0 * pi))
        # Solved(richard_chen): The problem of this is that the result is -1 and I did not understand why -1 can
        #  raise math domain error. Maybe I cannot use the pi here. please check it. The reason is that the float
        #  precision is over the -1. And the range of acos is [-1,1]. Here use the round function to solve the problem
        middle_result = round((relative_speed ** 2 + v2 ** 2 - v1 ** 2) / (2 * relative_speed * v2), 6)
        Q = acos(middle_result) * 180.0 / pi
        # relative course
        if alpha > 0:
            relative_course = heading2 + Q
        else:
            relative_course = heading2 - Q

        # relative bearing
        bearing1 = bearing.initial_compass_bearing(
            float(x2), float(y2), float(x1), float(y1)) - relative_course
        DCPA = distance * sin(bearing1 * pi / 180.0)
        TCPA = distance * cos(bearing1 * pi / 180.0) / relative_speed
        return DCPA, TCPA
