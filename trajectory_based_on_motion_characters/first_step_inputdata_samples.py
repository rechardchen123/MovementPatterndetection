# !/usr/bin/env python3
# -*- coding: utf-8 -*

'''
Data processing is that it firstly read the whole dataframe from database.
And then, it should use the same segments based on the 24 hours of the trajectory for each ship.
Next, the segment number is based on the median value. And then get the data between the 30 seconds to 2 minutes.
Finally, store the data into file.
'''

import pandas as pd
import glob

ais_file = pd.read_csv('/home/rechardchen123/Documents/data/dataset-ais-origin/drop_decimals_finish_drop.csv')

# group by data based on MMSI
groupby_mmsi = ais_file.groupby(['MMSI'])
for group in groupby_mmsi:
    group[1].to_csv('/home/rechardchen123/Documents/data/ais_data_processed/%s.csv' % str(group[0]), index=False)

# split the data by day
groupby_data = glob.glob('/home/rechardchen123/Documents/data/ais_data_processed/*.csv')

for f in groupby_data:
    read_file = pd.read_csv(f)
    read_file['Day'] = pd.to_datetime(read_file['Record_Datetime']).dt.day
    read_file['Hour'] = pd.to_datetime(read_file['Record_Datetime']).dt.hour
    read_file['Minute'] = pd.to_datetime(read_file['Record_Datetime']).dt.minute
    read_file['Seconds'] = pd.to_datetime(read_file['Record_Datetime']).dt.second
    groupby_day = read_file.groupby(read_file['Day'])
    name = int(read_file.iloc[0]['MMSI'])
    for group in groupby_day:
        group[1].to_csv(
            '/home/rechardchen123/Documents/data/data_after_processed_1/%s-%s.csv' % (str(name), str(group[0])),
            index=False)

# second delete the small data segment using delete_small_file.py
