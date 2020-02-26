# !/usr/bin/env python3
# -*- coding: utf-8 -*
import pandas as pd
import matplotlib.pyplot as plt
#import matplotlib
#matplotlib.use('Agg')


def plot_conflit_trajectory(file_name, conflict_mmsi, conflict_lng, conflict_lat):
    '''
    Plot the conflict trajectory
    :param file_name: it indicates the day and the hour of the trajectory.
    :param conflict_mmsi: the conflict ship identification
    :param conflict_lng: the longitude of the conflicted ship
    :param conflict_lat: the latitude of the conflicted ship
    :return: the trajectory
    '''
    # todo(richard_chen): based on the conflict trajectory, how to select the two ship's trajectory.