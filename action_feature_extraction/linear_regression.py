# !/usr/bin/env python3
# -*- coding: utf-8 -*
'''
Linear regression with smoothing method to erase the noise.
'''
import glob
import pandas as pd
from utils import save_data


def mean5_3(data, m):
    '''
    five points smoothing
    :param data: the heading data
    :param m: iteration number
    :return:
    '''
    n = len(data)
    a = data
    b = data.copy()
    for i in range(m):
        b[0] = (69 * a[0] + 4 * (a[1] + a[3]) - 6 * a[2] - a[4]) / 70
        b[1] = (2 * (a[0] + a[4]) + 27 * a[1] + 12 * a[2] - 8 * a[3]) / 35
        for j in range(2, n - 2):
            b[j] = (-3 * (a[j - 2] + a[j + 2]) + 12 * (a[j - 1] + a[j + 1]) + 17 * a[j]) / 35
        b[n - 2] = (2 * (a[n - 1] + a[n - 5]) + 27 * a[n - 2] + 12 * a[n - 3] - 8 * a[n - 4]) / 35
        b[n - 1] = (69 * a[n - 1] + 4 * (a[n - 2] + a[n - 4]) - 6 * a[n - 3] - a[n - 5]) / 70
        a = b.copy()
    return a


# read the conflict data into the model
data = glob.glob()

# process every data using the linear regression method
for f in data:
    read_file = pd.read_csv(f)
    # get the heading series
    heading = read_file['Heading']
    after_regression_heading = mean5_3(heading, 10)
    mmsi = list(read_file['MMSI'])
    lat = list(read_file['Latitude'])
    lng = list(read_file['Longitude'])
    speed = list(read_file['Speed'])
    minute = list(read_file['MInute'])
    # get a new dataframe
    save_data(mmsi, lng, lat, speed, after_regression_heading, minute)
