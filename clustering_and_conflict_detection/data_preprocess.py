# !/usr/bin/env python3
# -*- coding: utf-8 -*
import glob
import pandas as pd
import os

ais_file = pd.read_csv(
    r'C:\Users\ucesxc0\Documents\Repository-My programming and coding\data\dataset-ais-origin\drop_decimals_finish_drop.csv')

# group data by day
ais_file['Record_Datetime'] = pd.to_datetime(ais_file['Record_Datetime'])
ais_file['Month'] = pd.to_datetime(ais_file['Record_Datetime']).dt.month
ais_file['Day'] = pd.to_datetime(ais_file['Record_Datetime']).dt.day
ais_file['Hour'] = pd.to_datetime(ais_file['Record_Datetime']).dt.hour
ais_file['Minute'] = pd.to_datetime(ais_file['Record_Datetime']).dt.minute
name = int(ais_file.iloc[0]['Month'])
groupby_day = ais_file.groupby(['Day'])
for group in groupby_day:
    group[1].to_csv(
        r'C:\Users\ucesxc0\Documents\Repository-My programming and coding\data\data_resemble\data-monthly\%s-%s.csv' % (
            str(name), str(group[0])), index=False)

# group the data by hour
trajectory_process = glob.glob('/home/richardchen123/Documents/data/data_resemble/test/*.csv')
for f in trajectory_process:
    read_file = pd.read_csv(f)
    # get the filename
    filename = os.path.splitext(os.path.basename(f))[0]
    groupby_hour = read_file.groupby(read_file['Hour'])
    for group in groupby_hour:
        group[1].to_csv(
            '/home/richardchen123/Documents/data/data_resemble/test/groupby_hour/%s-%s.csv' % (filename, str(group[0])),
            index=False)
