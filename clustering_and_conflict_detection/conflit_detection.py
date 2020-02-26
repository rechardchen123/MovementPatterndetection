# !/usr/bin/env python3
# -*- coding: utf-8 -*
import glob
import pandas as pd
from clustering_and_conflict_detection.encounter_clustering import clustering
from clustering_and_conflict_detection.calculation_cpa import cpa_calculation
from utils import save_data_into_file1
import os

'''
The confilit detection includes:
1. Encounter clustering
The cluster algorithm is using the spatio-temporal data.
Given an observation time t and a collected AIS trajectory data,
extract a snapshot data. By user-defined circle of observation, the cluster of encounters is dsicovered.
2. Conflict detection.
Conflict detection module is designed to estimate the possible conflict for each cluster of encounters.
In the conflict detection, the distance at the closest point of approach and the time to collision avoidance
are adopted to measure the maritime conflict behavior.
'''
# parameters
OBSERVATION_CIRCLE = 0.4

# read the data by hour
read_data = glob.glob(
    r'C:\Users\ucesxc0\Documents\Repository-My programming and coding\data\data_resemble\test\groupby_hour\*.csv')

for file in read_data:
    file_name = os.path.split(file)[-1].split('.')[0]
    group = pd.read_csv(file)
    data = clustering(group, OBSERVATION_CIRCLE)
    print(file)
    # conflict detection accumulation
    conflict_mmsi = []
    conflict_lat = []
    conflict_lng = []
    conflict_heading = []
    conflict_speed = []
    conflict_minute = []
    cpa = []
    tcpa1 = []

    for i in range(0, len(data) - 1):
        # todo(richard_chen): add a MMSI filter to sort the sequence...
        # transfer the data into list for processing
        mmsi = list(data['MMSI'])
        longitude = list(data['Longitude'])
        latitude = list(data['Latitude'])
        heading = list(data['Heading'])
        speed = list(data['Speed'])
        minute = list(data['Minute'])

        # add a selection for calculating the value error
        dcpa, tcpa = cpa_calculation(latitude[i], longitude[i], latitude[i + 1], longitude[i + 1], speed[i],
                                     speed[i + 1], heading[i], heading[i + 1])
        # using the tcpa and dcpa to detect the risk between two ships.
        if tcpa < 0.1:
            print("No conflict zones found %s" % str(i))
        elif tcpa >= 0.1:
            conflict_mmsi.append(mmsi[i])
            conflict_lat.append(latitude[i])
            conflict_lng.append(longitude[i])
            conflict_heading.append(heading[i])
            conflict_speed.append(speed[i])
            conflict_minute.append(minute[i])
            cpa.append(dcpa)
            tcpa1.append(tcpa)

    # groupby the data by MMSI and save the conflict zones into files
    data1 = save_data_into_file1(file_name, conflict_mmsi, conflict_lng, conflict_lat, conflict_speed, conflict_heading,
                                 conflict_minute, cpa, tcpa1)
