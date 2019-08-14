# !/usr/bin/env python3
# -*- coding: utf-8 -*
import os
import pandas as pd
import numpy as np
import datetime
from math import sqrt, sin, cos, pi, acos, radians,asin, atan2
from geohelper import bearing
EARTH_RADIUS = 6378.1
n_mile = 1.852
'''
The clustering algorithm is:
1. select the time and collision detection distance 
2. get the selected time data
3. compare any two data for the distance is less the collision detection distance.
4. get the  encounter clustering 
'''

'''
The confict detection algorithm:
Using the CPA and DCPA to detect the data
'''


def clustering(trajectory_data, time_day, time_hour, time_minute, dist):
    '''
    Clustering the data
    :param trajectory_data: the AIS dataset
    :param time_day: the selected day
    :param time_hour: the selected hour
    :param time_minute: the selected minute
    :param dist: the user-defined distance
    :return: the clustering data
    '''
    selected_data = trajectory_data.loc[trajectory_data['Day'] == time_day]  # based on the day to select
    selected_data = selected_data.loc[selected_data['Hour'] == time_hour]  # based on the hour to locate
    selected_data = selected_data.loc[
        selected_data['Minute'] <= time_minute]  # based on the minute to find the proper range data
    # choose the longitude, latitude, speed and heading fileds
    selected_data1 = selected_data.loc[:, ['MMSI', 'Longitude', 'Latitude', 'Heading', 'Speed', 'Minute']]

    # cluster the data based on the algorithm
    MMSI_list = list(selected_data1['MMSI'])
    Longitude_list = ['{:.3f}'.format(i) for i in list(selected_data1['Longitude'])]
    Latitude_list = ['{:.3f}'.format(i) for i in list(selected_data1['Latitude'])]
    Heading_list = list(selected_data1['Heading'])
    Speed_list = list(selected_data1['Speed'])
    Minute_list = list(selected_data1['Minute'])
    saved_mmsi = []
    saved_long_list = []
    saved_lat_list = []
    saved_heading_list = []
    saved_speed_list = []
    saved_minute_list = []
    for i, j in Latitude_list, Longitude_list:
        distance_two_points = get_distance_hav(i + 1, i, j + 1, j)
        if distance_two_points <= dist:
            saved_mmsi.append(MMSI_list(i))
            saved_lat_list.append(Latitude_list(i))
            saved_long_list.append(Longitude_list(j))
            saved_heading_list.append(Heading_list(i))
            saved_speed_list.append((Speed_list(i)))
            saved_minute_list.append((Minute_list(i)))
    # save_data_into_file(saved_mmsi, saved_long_list, saved_lat_list, saved_speed_list, saved_heading_list,
    #                    saved_minute_list)
    # return saved_mmsi, saved_long_list, saved_lat_list, saved_speed_list, saved_heading_list, saved_minute_list
    data = save_data(saved_mmsi, saved_long_list, saved_lat_list, saved_speed_list, saved_heading_list,
                               saved_minute_list)
    return data


def save_data(MMSI_list, Longitude_list, Latitude_list, Speed_list, Heading_list, Minute_list):
    save_dict = {'MMSI': MMSI_list,
                 'Longitude': Longitude_list,
                 'Latitude': Latitude_list,
                 'Speed': Speed_list,
                 'Heading': Heading_list,
                 'Minute': Minute_list}
    data = pd.DataFrame(save_dict)
    # data.to_csv('/home/rechardchen123/Documents/data/%s.csv' % encounter_data, index=False)
    return data


def save_data_into_file(MMSI_list, Longitude_list, Latitude_list, Speed_list, Heading_list):
    save_dict = {'MMSI': MMSI_list,
                 'Longitude': Longitude_list,
                 'Latitude': Latitude_list,
                 'Speed': Speed_list,
                 'Heading': Heading_list}
    data = pd.DataFrame(save_dict)
    data.to_csv('/home/rechardchen123/Documents/data/%s.csv'% conflict_trajectories, index=False)


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
    distance = get_distance_hav(x1, x2, y1, y2)

    alpha = heading2 - heading1
    if alpha > 180:
        alpha-= 360
    elif alpha < -180:
        alpha += 360

    #relative speed
    relative_speed = sqrt(v2**2 + v1**2 - 2*v2*cos(alpha/180.0 * pi))
    Q = acos((relative_speed**2 + v2**2 - v1**2)/(2*relative_speed*v2)) * 180.0 / pi

    #relative course
    if alpha >0:
        relative_course = heading2 + Q
    else:
        relative_course = heading2 - Q

    #relative bearing
    bearing = bearing.initial_compass_bearing(x2, y2, x1, y1) - relative_course
    DCPA = distance * sin(bearing*pi/180.0)
    TCPA = distance * cos(bearing*pi/180.0)/relative_speed
    return DCPA, TCPA

def hav(theta):
    s = sin(theta/2)
    return s*s

def get_distance_hav(lat0,lng0, lat1,lng1):
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
    h = hav(dlat)+cos(lat0)*cos(lat1)*hav(dlng)
    distance = 2*EARTH_RADIUS*asin(sqrt(h))
    return distance/n_mile


