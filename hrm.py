# HRM


import numpy
import pandas
import scipy.signal
import matplotlib.pyplot as plt

def file_checker(ecg_data_file, names):
    try:
        df = pandas.read_csv(ecg_data_file, header = None, names = names, \
                converters = {"times" : float, "voltages" : float})
        err_Bool = False
        return err_Bool
    except ValueError:
        err_Bool = True
        return err_Bool

def peak_detector(ecg_data_file):
    """Function to find all of the peaks in the csv

        The peaks will be used to find heart rate

        :param ecg_data: the initial csv file given
        :rtype: list of times where a peak occured
    """
    peak_times=[0]

    names = ["times","voltages"]
    data_error = False
    data_error = file_checker(ecg_data_file, names)
    if (data_error == True):
        print("Non-Numeric Value Entered")
        return peak_times

    ecg_data = pandas.read_csv(ecg_data_file, header = None, names = names, \
            converters = {"times" : float, "voltages": float})
    times = ecg_data.times.values
    voltages = ecg_data.voltages.values

    # Differentiation/AutoCorr Method
    # autocorr = numpy.correlate(voltages, voltages, mode='same')


    # diff = numpy.diff(autocorr)/numpy.diff(times);

    # diff = numpy.diff(autocorr)

    # for k in range(0,numpy.size(diff)):
    #    print(k)
    #    print(diff[k])
    #    if((diff[k] >= -0.0015) and (diff[k] <= 0.0015)):
        # if((diff[k] >= -1) and (diff[k] <= 1)):
            # peakTimes.append(times[k])

    # peakTimes.pop(0);

    # Data Visualization
    # plt.plot(times, autocorr)
    # plt.plot(times, voltages)
    # plt.show()

    # Threshold Method
    avg_voltage = numpy.average(voltages)
    thresh_voltage = abs(avg_voltage) * 2

    peaks = numpy.where(voltages >= thresh_voltage)
    peaks1 = peaks[0]
    peaks2 = peaks1.tolist()
    first_peak = 0.0;
    second_peak = 0.0;
    for i in range(1, len(peaks2) - 1):
       if (voltages[peaks2[i]] >= voltages[peaks2[i - 1]]) and \
               (voltages[peaks2[i]] >= voltages[peaks2[i + 1]]):
           recent_val = peak_times[len(peak_times) - 1]
           peak_times.append(times[peaks2[i]])
           if(len(peak_times)==2):
               first_peak = times[peaks2[i]]
           if(len(peak_times)==3):
               second_peak = times[peaks2[i]]
           if(times[peaks2[i]] - recent_val <= 0.5*(second_peak-first_peak)):
               peak_times.pop()
    peak_times.pop(0)
    # print(len(peak_times))
    # print(peak_times)

    return peak_times

def instant(time, target_time):
    """Function that finds the heart rate at an instant time

        Finds the peak that corresponds to given time, if there
        is not a perfect match, it will pick the closest peak after
        the given time

        :param time: list of times at which peaks occur
        :param targetTime: time specified by the user
        :rtype: heart rate at the specified time

        Heart rate is taken by subtracting the times of
        the two peaks
    """

    if target_time > time[len(time) - 1]:
        raise ValueError('target time is out of range of detected peaks')

    for x in range(0, len(time)):
        if time[x] >= target_time:
            if x + 1 >= len(time):
                raise ValueError(
                    'Target time is out of range of detected peaks')
            instant_dt = time[x + 1] - time[x]
            break
    return (60 / instant_dt) / 1000


def average(time, begin_time, end_time):
    """Function that finds the average heart rate over a user specified time

        Like the instant function,
        the peak is chosen from the peak directly after
        the user specified time

        :param time: list of times at which the peaks occur
        :param begin_time: The user specified time at which the avg starts
        :param end_time: User specified time at which the avg ends
        :rtype: Average heart rate over user specified time

    """

    if begin_time >= end_time:
        raise ValueError('Begin time is before end time')
    if time[len(time) - 1] < end_time:
        raise ValueError('End time occurs outside of range of csv file')
    if time[len(time) - 1] < begin_time:
        raise ValueError('Begin time occurs outside of range of csv file')

    begin = 0
    end = 0

    for i in range(1, len(time)):
        if time[i - 1] / 1000 == begin_time:
            begin = i - 1
        elif time[i - 1] / 1000 < begin_time and time[i] / 1000 > begin_time:
            begin = i
        if time[i - 1] / 1000 == end_time:
            end = i - 1
        elif (time[i - 1] / 1000 < end_time) and (time[i] / 1000 > end_time):
            end = i

    time_count = 0

    for k in range(begin + 1, end + 1):
        time_count = time_count + (time[k] - time[k - 1]) / 1000

    div = end - begin

    if div == 0:
        raise ValueError('Begin and End time are too close')

    time_avg = time_count / div

    return 60 / time_avg


def anomaly(time, brady_thresh, brady_time, tachy_thresh, tachy_time):
    """Function for finding if there is bradycardia or tachycardia

        The parameters are all configurable.

        :param time: list of times at which the peaks occur
        :param brady_thresh (bpm): The threshold for bradycardia, if a
            heart rate is below this, it is considered bradycardia
        :param brady_time: the length of time the low heart rate has
            to last in order to be considered bradycardia
        :param tachy_thresh (bpm): The threshold for tachycardia, if a
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
    counter = 0
    for i in range(1, len(time)):
        if (60000 / (time[i] - time[i - 1]) < brady_thresh) and \
                (dying_slow == 0):
            dying_slow = time[i - 1]
            print("here")
        elif (dying_slow != 0) and \
                (60000 / (time[i] - time[i - 1]) > brady_thresh):
            if time[i] - dying_slow > brady_time:
                bradyTimes.append(dying_slow / 1000)
                print("here2")
            dying_slow = 0
        if (60000 / (time[i] - time[i - 1]) > tachy_thresh) and \
                (dying_fast == 0):
            dying_fast = time[i - 1]
        elif (dying_fast != 0) and \
                (60000 / (time[i] - time[i - 1]) < tachy_thresh):
            if time[i] - dying_fast > tachy_time:
                tachyTimes.append(dying_fast / 1000)
            dying_fast = 0
    return bradyTimes, tachyTimes


def main(
        ecg_data_file,
        user_specified_time1=0,
        user_specified_time2=30,
        brady_threshold=50,
        tachy_threshold=100,
        brady_time=5,
        tachy_time=5,
        inst=False,
        avg=False,
        ano=False):
    """Main function for determining information about ECG data

        All previous functions are
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
    peak_time = peak_detector(ecg_data_file)
    ret_file = open("testfile.txt", "w")

    if inst:
        instant_time = instant(peak_time, user_specified_time1)
        ret_file.write("Instantaneous HR: " + str(instant_time) + "\n")
        if (inst and not avg and not ano):
            return instant_time

    if avg:
        average_time = average(
            peak_time,
            user_specified_time1,
            user_specified_time2)
        ret_file.write(
            "Average HR from " +
            str(user_specified_time1) +
            " to " +
            str(user_specified_time2) +
            ": " +
            str(average_time) +
            "\n")
        if (avg and not inst and not ano):
            return average_time

    if ano:
        [brady, tachy] = anomaly(
            peak_time, brady_threshold, brady_time, tachy_threshold, tachy_time)
        ret_file.write("Brady times: ")
        for k in range(0, len(brady)):
            ret_file.write(str(brady[k]) + " ")
        ret_file.write("\n Tachy times: ")
        for n in range(0, len(tachy)):
            ret_file.write(str(tachy[n]) + " ")
        if (ano and not inst and not avg):
            return brady, tachy

    ret_file.close()
    

if __name__ == '__main__':
   main('full_test.csv', inst=True)
