#HRM

import pytest
import pytest_pep8
import numpy
import pandas
import csv

def peakDetector(ecg_data):
    """Insert function here

    with open(ecg_data) as csvfile:
        heartreader = csv.DictReader(csvfile)
        for row in heartreader:
            voltageList=list(row["voltage"])"""

    data = pandas.read_csv(ecg_data, converters = {"times":float,"voltage":float}, names = {"times2","voltage2"})
    print(data.times2)
    #avgVoltage = numpy.mean()
    #print(avgVoltage)

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



def average(time, begin_time, end_time):
    """Insert function here"""
    if time[len(time)] < end_time:
        raise ValueError('End time occurs outside of range of csv file')
    if time[len(time)] < begin_time:
        raise ValueError('Begin time occurs outside of range of csv file')

    begin = 0
    end   = 0

    for i in range(1, len(time)):
        if time[i-1] == begin_time:
            begin = i-1
        elif (time[i-1] < begin_time and time[i] > begin_time):
            begin = i
        if time[i-1] == end_time:
            end = i-1
        elif (time[i-1] < end_time and time[i] > end_time):
            end = i
    
    time_count = 0

    for k in range(begin+1, end+1):
        time_count = time[k-1] - time[k]
    
    div = begin-end
    time_avg = time_count/div

    return 1/time_avg

    


def anomaly(time, peak):
    """Insert function here"""

def main(ecg_data, user_specified_time1=0, user_specified_time2=2000, brady_threshold = 50, tachy_threshold = 100, \
         int = False, avg = False, ano = False):

    """Insert function here"""

    ecg_dict = peakDetector('full_test.csv')



if __name__ == '__main__':
    main('full_test.csv');