# !/usr/bin/env python3
# -*- coding: utf-8 -*
import os
import pandas as pd
import numpy as np
import datetime

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
    :param trajectory_data: The raw data after processing
    :param time: the detail time
    :param distance: collision detection distance
    :return: the encounter detection data
    '''
    selected_data = trajectory_data.loc[trajectory_data['Day'] == time_day]  # based on the day to select
    selected_data = selected_data.loc[selected_data['Hour'] == time_hour]  # based on the hour to locate
    selected_data = selected_data.loc[
        selected_data['Minute'] <= time_minute]  # based on the minute to find the proper range data
    # choose the longitude, latitude, speed and heading fileds
    selected_data1 = selected_data.loc[:, ['MMSI', 'Longitude', 'Latitude', 'Heading', 'Speed']]

    # cluster the data based on the algorithm
    MMSI_list = list(selected_data1['MMSI'])
    Longitude_list = ['{:.3f}'.format(i) for i in list(selected_data1['Longitude'])]
    Latitude_list = ['{:.3f}'.format(i) for i in list(selected_data1['Latitude'])]
    Heading_list = list(selected_data1['Heading'])
    Speed_list = list(selected_data1['Speed'])
    saved_mmsi = []
    saved_long_list = []
    saved_lat_list = []
    saved_heading_list = []
    saved_speed_list = []
    for i, j in Latitude_list, Longitude_list:
        distance_two_points = distance(i + 1, i, j + 1, j)
        if distance_two_points <= dist:
            saved_mmsi.append(MMSI_list(i))
            saved_lat_list.append(Latitude_list(i))
            saved_long_list.append(Longitude_list(j))
            saved_heading_list.append(Heading_list(i))
            saved_speed_list.append((Speed_list(i)))
    # save_data_into_file(saved_mmsi, saved_long_list, saved_lat_list, saved_speed_list, saved_heading_list)
    return saved_mmsi, saved_long_list, saved_lat_list, saved_speed_list, saved_heading_list


def save_data_into_file(MMSI_list, Longitude_list, Latitude_list, Speed_list, Heading_list):
    save_dict = {'MMSI': MMSI_list,
                 'Longitude': Longitude_list,
                 'Latitude': Latitude_list,
                 'Speed': Speed_list,
                 'Heading': Heading_list}
    data = pd.DataFrame(save_dict)
    data.to_csv('/home/rechardchen123/Documents/data/%s.csv' % encounter_data, index=False)


def distance(lat1, lat2, long1, long2):
    '''
    :param lat1: latitude 1
    :param lat2: latutude 2
    :param long1: longitude 1
    :param long2: longitude 2
    :return: distance of the two points
    '''
    delta_lat = lat2 - lat1
    delta_long = long2 - long1
    distance = np.sqrt(np.square(delta_lat) + np.square(delta_long))
    return distance


def conflict_detection(mmsi, long_list, lat_list, speed_list, heading_list):

