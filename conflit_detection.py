# !/usr/bin/env python3
# -*- coding: utf-8 -*
import os
import numpy as np
import pandas as pd
import datetime
import glob

'''
The confilit detection includes:
1. Encounter clustering
The cluster algorithm is using the spatio-temporal data.
Given an observation time t and a collected AIS trajectory data,
extract a snapshot data. By user-defined circle of observation, the cluster of encounters is dsicovered.
2. Conflict detection
Conflict detection module is designed to estimate the possible conflict for each cluster of encounters.
In the conflict detection, the distance at the closest point of approach and the time to collision avoidance
are adopted to measure the maritime conflict behavior.
'''
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
# read ais data and get the distance and time parameters
trajectory_process = pd.read_csv('/home/rechardchen123/Documents/data/dataset-ais-origin/drop_decimals_finish_drop.csv')

observation_distance = int(input('please input the observation distance: '))
time_day = int(input('please input the day: '))
time_hour = int(input('please input the hour time: '))
time_minute = int(input('please input the condition time (minutes): '))

# read the data
count_MMSI = 0

for i in trajectory_process['MMSI'].duplicated():
    if i == False:
        count_MMSI = count_MMSI + 1
print('total MMSI number is: %d' % count_MMSI)

trajectory_process['Record_Datetime'] = pd.to_datetime(trajectory_process['Record_Datetime'])
trajectory_process['Day'] = pd.to_datetime(trajectory_process['Record_Datetime']).dt.day
trajectory_process['Hour'] = pd.to_datetime(trajectory_process['Record_Datetime']).dt.hour
trajectory_process['Minute'] = pd.to_datetime(trajectory_process['Record_Datetime']).dt.minute

# delete the middle field
after_trajectory_process = trajectory_process.drop(columns=['Record_Datetime'])
print(after_trajectory_process.head(100))

# clustering the data
