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


def clustering(trajectory_data, time_day, time_hour, time_minute, distance):
    '''
    :param trajectory_data: The raw data after processing
    :param time: the detail time
    :param distance: collision detection distance
    '''
    selected_data = trajectory_data.loc[trajectory_data['Day'] == time_day]  # based on the day to select
    selected_data = selected_data.loc[selected_data['Hour'] == time_hour]  # based on the hour to locate
    selected_data = selected_data.loc[
        selected_data['Minute'] <= time_minute]  # based on the minute to find the proper range data
    #choose the longitude, latitude, speed and heading fileds
    selected_data1 = selected_data.loc[:,['MMSI','Longitude','Latitude','Heading','Speed']]

    # cluster the data based on the algorithm
    