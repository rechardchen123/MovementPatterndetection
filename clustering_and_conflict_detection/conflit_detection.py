# !/usr/bin/env python3
# -*- coding: utf-8 -*
import pandas as pd
from clustering_and_conflict_detection.encounter_clustering import clustering
from clustering_and_conflict_detection.calculation_cpa import cpa_calculation
from utils import save_data_into_file

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
data = clustering(after_trajectory_process, time_day, time_hour, time_minute)

# conflict detection accumulation
conflict_mmsi = []
conflict_lat = []
conflict_lng = []
conflict_heading = []
conflict_speed = []
conflict_minute = []
for i in range(0, len(data)):
    selected_data = data.loc[data['Minute'] == i]
    # transfer the data into list for processing
    mmsi = list(selected_data['MMSI'])
    longitude = ['{:.3f}'.format(i) for i in list(selected_data['Longitude'])]
    latitude = ['{:.3f}'.format(i) for i in list(selected_data['Latitude'])]
    heading = list(selected_data['Heading'])
    speed = list(selected_data['Speed'])
    minute = list(selected_data['Minute'])
    dcpa, tcpa = cpa_calculation(latitude[i], longitude[i], latitude[i + 1], longitude[i + 1], speed[i], speed[i + 1],
                                 heading[i], heading[i + 1])
    # using the tcpa and dcpa to detect the risk between two ships.
    if tcpa < 0:
        print("No conflict zones found!")
    elif tcpa >= 0:
        conflict_mmsi.append(mmsi[i])
        conflict_lat.append(latitude[i])
        conflict_lng.append(longitude[i])
        conflict_heading.append(heading[i])
        conflict_speed.append(speed[i])
        conflict_minute.append(minute[i])

# groupby the data by MMSI and save the conflict zones into files
data1 = save_data_into_file(conflict_mmsi, conflict_lng, conflict_lat, conflict_speed, conflict_heading,
                            conflict_minute)

# groupby the data
group_by_mmsi = data1.groupby(['MMSI'])
for group in group_by_mmsi:
    group[1].to_csv(str(group[0]) + '.csv', index=False)
