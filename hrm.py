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

    data = pandas.read_csv(ecg_data, converters = {"times":float,"voltage":float})
    avgVoltage = numpy.mean(data.voltage.values)
    minVoltage = numpy.min(data.voltage.values)
    threshVoltage = avgVoltage + minVoltage

    threshTimes= numpy.where(data.voltage.values>threshVoltage)
    print(threshTimes)

def instant(time, targetTime):
    """Insert function here"""
    if targetTime > time[len(time)-1]:
        raise ValueError('target time is out of range of detected peaks')

    for x in range(0,len(time)):
        if time[x] >= targetTime:
            if x+1 >= len(time):
                raise ValueError('Target time is out of range of detected peaks')
            instant_dt = time[x+1] - time[x]
    return 1/instant_dt

def average(time, begin_time, end_time):

    if begin_time >= end_time:
        raise ValueError('Begin time is before end time')
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

def anomaly(time, brady_thresh, brady_time, tachy_thresh, tachy_time):
    """Insert function here"""
    dying_slow = 0
    dying_fast = 0
    for i in range(1, len(time)):
        if 1/(time[i-1]-time[i]) < brady_thresh
            dying_slow = time[i-1]
        elif dying_slow != 0
            if time[i] - dying_slow > brady_time
                bradyTimes.append(dying_slow)
            dying_slow = 0
        if (time[i-1]-time[i]) > tachy_thresh
            dying_fast = time[i-1]
        elif dying_fast != 0
            if time[i] - dying_fast > tachy_time
                tachyTimes.append(dying_fast)
            dying_fast = 0
    return bradyTimes, tachyTimes
            
        

def main(ecg_data, user_specified_time1=0, user_specified_time2=2000, brady_threshold = 50, tachy_threshold = 100, \
         brady_time = 5, tachy_time = 5, inst = False, avg = False, ano = False):

    """Insert function here"""

    ecg_data = peakDetector('full_test.csv')
    if inst:
        instant_time = instant(ecg_data, user_specified_time1)
        print ("Instantaneous HR: " + str(instant_time))
        if (inst and !avg and !ano):
            return instant_time

    if avg:
        average_time = average(ecg_data, user_specified_time1, user_specified_time2)
        print ("Average HR from " + user_specified_time1 + " to " + user_specified_time2 + \
                ": " + str(average_time))
        if (avg and !inst and !ano):
            return average_time

    if ano:
        [brady, tachy] = anomaly(ecg_data, brady_threshold, brady_time, tachy_threshold, tachy_time)
        print ("Brady times: " + brady)
        print ("Tachy times: " + tachy)
        if (ano and !inst and !avg):
            return brady tachy



if __name__ == '__main__':
    main('full_test.csv');
