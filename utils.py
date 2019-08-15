# !/usr/bin/env python3
# -*- coding: utf-8 -*
import os
import pandas as pd


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


def save_data_into_file(MMSI_list, Longitude_list, Latitude_list, Speed_list, Heading_list, Minute_list):
    save_dict = {'MMSI': MMSI_list,
                 'Longitude': Longitude_list,
                 'Latitude': Latitude_list,
                 'Speed': Speed_list,
                 'Heading': Heading_list,
                 'Minute':Minute_list}
    data = pd.DataFrame(save_dict)
    data.to_csv('/home/rechardchen123/Documents/data/conflict_trajectory.csv', index=False)



