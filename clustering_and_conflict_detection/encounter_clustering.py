# !/usr/bin/env python3
# -*- coding: utf-8 -*
from clustering_and_conflict_detection.distance_transform import get_distance_hav
from utils import save_data

'''
The clustering algorithm is:
1. select the time and collision detection distance 
2. get the selected time data
3. compare any two data for the distance is less the collision detection distance.
4. get the  encounter clustering 
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
