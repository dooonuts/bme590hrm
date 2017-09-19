#HRM

import pytest
import pytest_pep8
import numpy

def peakDetector(ecg_data):
    """Insert function here"""

    with open(ecg_data) as csvfile:
        heartreader = csv.DictReader(csvfile)

def instant(time, targetTime=0):
    """Insert function here"""
    if targetTime > time[len(time)-1]:
        raise "Target time is out of range of detected peaks", targetTime

    for x in range(0,len(time))
        if time[x] >= targetTime:
            if x+1 >= len(time):
                raise "Target time is out of range of detected peaks", targetTime
            instant_dt = time[x+1] - time[x]
    return 1/instant_dt



def average(time, peak):
    """Insert function here"""

def anomaly(time, peak):
    """Insert function here"""

def main(ecg_data, user_specified_time1=0, user_specified_time2=2000, brady_threshold = 50, tachy_threshold = 100, \
         int = False, avg = False, ano = False):

    """Insert function here"""

    ecg_dict = peakDetector(ecg_data)
    
