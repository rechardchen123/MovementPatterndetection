# !/usr/bin/env python3
# -*- coding: utf-8 -*
from distance_transform import get_distance_hav
from utils import save_data, save_data_into_file

'''
The clustering algorithm is:
1. select the time and collision detection distance 
2. get the selected time data
3. compare any two data for the distance is less the collision detection distance.
4. get the  encounter clustering 
'''



def clustering(trajectory_data, dist):
    '''
    Clustering the data
    :param trajectory_data: the AIS dataset
    :param dist: the user-defined distance
    :param obs_minute: the observation minute
    :return: the clustering data
    '''
    selected_data = trajectory_data.loc[:, ['MMSI', 'Longitude', 'Latitude', 'Heading', 'Speed', 'Minute']]
    MMSI_list = list(selected_data['MMSI'])
    Longitude_list = ['{:.3f}'.format(i) for i in list(selected_data['Longitude'])]
    Latitude_list = ['{:.3f}'.format(i) for i in list(selected_data['Latitude'])]
    Heading_list = list(selected_data['Heading'])
    Speed_list = list(selected_data['Speed'])
    Minute_list = list(selected_data['Minute'])
    saved_mmsi = []
    saved_long_list = []
    saved_lat_list = []
    saved_heading_list = []
    saved_speed_list = []
    saved_minute_list = []
    for i in range(0, len(Latitude_list) - 1):
        distance_two_points = get_distance_hav(Latitude_list[i], Longitude_list[i], Latitude_list[i + 1],
                                               Longitude_list[i + 1])
        if distance_two_points <= dist:
            saved_mmsi.append(MMSI_list[i])
            saved_lat_list.append(Latitude_list[i])
            saved_long_list.append(Longitude_list[i])
            saved_heading_list.append(Heading_list[i])
            saved_speed_list.append(Speed_list[i])
            saved_minute_list.append(Minute_list[i])
    data = save_data_into_file(saved_mmsi, saved_long_list, saved_lat_list, saved_speed_list, saved_heading_list,
                               saved_minute_list)
    data = save_data(saved_mmsi, saved_long_list, saved_lat_list, saved_speed_list, saved_heading_list,
                     saved_minute_list)
    return data
