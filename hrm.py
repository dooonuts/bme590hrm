#HRM

import pytest
import pytest_pep8
import numpy
import pandas
import matplotlib.pyplot as plt

def peakDetector(ecg_data):
    """
        Function to find all of the peaks in the csv
        the peaks will be used to find heart rate
        
        :param ecg_data: the initial csv file given
        :rtype: list of times where a peak occured
    """

    # header is time, voltage
    data = pandas.read_csv(ecg_data, converters = {"times":float,"voltage":float})
    #avgVoltage = numpy.mean(data.voltage.values)
    #minVoltage = numpy.min(data.voltage.values)
    times = data.times.values
    voltages = data.voltage.values
    finalTimes=[];

    # autocorrelation
    autocorr= numpy.correlate(voltages,voltages, mode= 'same');
    #plt.plot(times,autocorr)
    #plt.plot(times,voltages)
    #plt.show()

    # differentiation
    diff= numpy.diff(autocorr)
    #for k in range(0,numpy.size(diff)):
    #    print(diff[k])
    peaks = numpy.where(diff==0)
    # print(peaks)
    for l in range(0,numpy.size(peaks)):
        finalTimes[l]=times[peaks[l]];
    print(finalTimes);

def instant(time, targetTime):
    """
        Function that finds the heart rate at an instant time
        finds the peak that corresponds to given time, if there
        is not a perfect match, it will pick the closest peak after
        the given time

        :param time: list of times at which peaks occur
        :param targetTime: time specified by the user 
        :rtype: heart rate at the specified time

        Heart rate is taken by subtracting the times of
        the two peaks
    """

    if targetTime > time[len(time)-1]:
        raise ValueError('target time is out of range of detected peaks')

    for x in range(0,len(time)):
        if time[x] >= targetTime:
            if x+1 >= len(time):
                raise ValueError('Target time is out of range of detected peaks')
            instant_dt = time[x+1] - time[x]
    return 1/instant_dt

def average(time, begin_time, end_time):
    """
        Function that finds the average heart rate over a
        user specified range. Like the instant function, 
        the peak is chosen from the peak directly after 
        the user specified time

        :param time: list of times at which the peaks occur
        :param begin_time: The user specified time at which the avg starts
        :param end_time: User specified time at which the avg ends
        :rtype: Average heart rate over user specified time

    """

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
    """
        Function for finding if there is bradycardia or tachycardia
        in the ECG data given. The parameters are all configurable. 

        :param time: list of times at which the peaks occur
        :param brady_thresh: The threshold for bradycardia, if a
            heart rate is below this, it is considered bradycardia
        :param brady_time: the length of time the low heart rate has
            to last in order to be considered bradycardia
        :param tachy_thresh: The threshold for tachycardia, if a 
            heart rate is above this, it is considered tachycardia
        :param tachy_time: the length of time the high heart rate has
            to last in order to be considered tachycardia
        :rtype: two lists which hold the when bradycardias first occured
            and when tahcycardias first occured

    """

    dying_slow = 0
    dying_fast = 0
    bradyTimes = []
    tachyTimes = []
    for i in range(1, len(time)):
        if 1/(time[i-1]-time[i]) < brady_thresh:
            dying_slow = time[i-1]
        elif dying_slow != 0:
            if time[i] - dying_slow > brady_time:
                bradyTimes.append(dying_slow)
            dying_slow = 0
        if (time[i-1]-time[i]) > tachy_thresh:
            dying_fast = time[i-1]
        elif dying_fast != 0:
            if time[i] - dying_fast > tachy_time:
                tachyTimes.append(dying_fast)
            dying_fast = 0
    return bradyTimes, tachyTimes

def main(ecg_data, user_specified_time1=0, user_specified_time2=30, brady_threshold = 50, tachy_threshold = 100, \
         brady_time = 5, tachy_time = 5, inst = False, avg = False, ano = False):

    """
        Main function for determining information about
        the ECG data provided. All previous functions are
        called by the main function to provide peaks and
        heart rates

        :param ecg_data: csv file which contains the ecg information
        :param user_specified_time1: Beginning time for the average
            heart rate, it is also the instantaneous time used. Default is 0
        :param user_specified_time2: Ending time for the average heart rate.
            Default is 30 seconds
        :param brady_threshold: Below this heart rate, it is bradycardia
        :param tachy_threshold: Above this heart rate, it is tachycardia
        :param brady_time: the min time that the brady threshold has to
            be breached for it to be considered bradycardia
        :param tachy_time: the min time that the tachy threshold has to
            be breached for it to be considered tachycardia
        :param inst: if this is True, then the instantaneous heart rate
            will be found. Default is False
        :param avg: if this is True, then the average heart rate will be
            found. Default is False
        :param ano: if this is True, then anomalies will be found and
            reported. Default is False
        :rtype: returns based on if only one of the 3 functions is selected.
            returns the heart rate. Also writes to a file

    """

    peak_time = peakDetector(ecg_data)
    ret_file  = open("testfile.txt", "w")

    if inst:
        instant_time = instant(peak_time, user_specified_time1)
        ret_file.write("Instantaneous HR: " + str(instant_time))
        if (inst and not avg and not ano):
            return instant_time

    if avg:
        average_time = average(peak_time, user_specified_time1, user_specified_time2)
        ret_file.write("Average HR from " + user_specified_time1 + " to " + user_specified_time2 + \
                ": " + str(average_time))
        if (avg and not inst and not ano):
            return average_time

    if ano:
        [brady, tachy] = anomaly(peak_time, brady_threshold, brady_time, tachy_threshold, tachy_time)
        ret_file.write("Brady times: " + brady)
        ret_file.write("Tachy times: " + tachy)
        if (ano and not inst and not avg):
            return brady, tachy

    ret_file.close()


if __name__ == '__main__':
    main('full_test.csv');
