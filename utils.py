# !/usr/bin/env python3
# -*- coding: utf-8 -*
import pandas as pd

def save_data(MMSI_list, Longitude_list, Latitude_list, Speed_list, Heading_list, Minute_list):
    save_dict = {'MMSI': MMSI_list,
                 'Longitude': Longitude_list,
                 'Latitude': Latitude_list,
                 'Speed': Speed_list,
                 'Heading': Heading_list,
                 'Minute': Minute_list}
    data = pd.DataFrame(save_dict)
    return data


def save_data_into_file(MMSI_list, Longitude_list, Latitude_list, Speed_list, Heading_list, Minute_list):
    save_dict = {'MMSI': MMSI_list,
                 'Longitude': Longitude_list,
                 'Latitude': Latitude_list,
                 'Speed': Speed_list,
                 'Heading': Heading_list,
                 'Minute':Minute_list}
    data = pd.DataFrame(save_dict)
    data.to_csv('/home/rechardchen123/Documents/data/data_resemble/test/clustering_trajectory.csv', index=False)

def save_data1(MMSI_list,Longitude_list, Latitude_list, Speed_list, Heading_list, Minute_list, zero_centerd_heading):
    save_dict = {'MMSI': MMSI_list,
                 'Longitude': Longitude_list,
                 'Latitude': Latitude_list,
                 'Speed': Speed_list,
                 'Heading': Heading_list,
                 'Minute': Minute_list,
                 'Centered_heading':zero_centerd_heading}
    data = pd.DataFrame(save_dict)
    data.to_csv('/home/rechardchen123/Documents/data/conflict_trajectory_centered.csv', index=False)

def save_data_into_file1(MMSI_list, Longitude_list, Latitude_list, Speed_list, Heading_list, Minute_list, cpa, tcpa):
    save_dict = {'MMSI': MMSI_list,
                 'Longitude': Longitude_list,
                 'Latitude': Latitude_list,
                 'Speed': Speed_list,
                 'Heading': Heading_list,
                 'Minute':Minute_list,
                 'CPA': cpa,
                 'TCPA': tcpa}
    data = pd.DataFrame(save_dict)
    data.to_csv('/home/rechardchen123/Documents/data/data_resemble/test/conflict_trajectory.csv', index=False)