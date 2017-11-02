import numpy
import pandas

# CONVERT_INPUT_TIME_TO_SECONDS = 1;

""" This global variable is used to convert input timescale into seconds. Base value of 1000 assumes milliseconds, where time (ms) / convert_input_time_to_seconds = time (s)
    Adjust variable as necessary to ensure time in seconds
"""


class HrmData:
    """This is a HRM class

       __init__ finds the peaks and sets the initial parameters
       instantHr finds the instantaneous hr at a given time
       averageHr finds the average hr over a period of time
       anomalyHr determines if there is brady/tachy and where they occurred

       Attributes:
            times             (list): list of times that a peak occurs
            instantaneous_hr   (list): list of all instantaneous hr computed
            instant_hr_target    (int): the instantaneous hr closest to the target time
            average_hr         (int): the last average hr computed
            anomaly_hr        (list): list of times the anomalies occurred
            brady_times       (list): times in which brady occurred
            tachy_times       (list): times in which tachy occurred
            units              (int): the data is given in ms or sec for ms put 1000
                                        for sec put 1
            err              (value): the error that is propagated up
            errBool        (boolean): error boolean for it it has error

    """

    def __init__(
            self,
            filename,
            begin_time=0,
            end_time=10,
            brady_time=5,
            brady_thresh=60,
            tachy_time=5,
            tachy_thresh=100,
            units=1):
        """Function that initializes values for the whole function

            Finds the peak that corresponds to given time, if there
            is not a perfect match, it will pick the closest peak after
            the given time

            :param self: the hrm object
            :param filename: csv file where the ECG data will be stored
            :param begin_time (ms): time for instHr and 1st time for avg
            :param end_time (ms): time where the avgHr will end
            :param brady_time (sec): time brady has to last to be considered brady
            :param brady_thresh (bpm): HR at which below is brady
            :param tachy_time (sec): time tachy has to last to be considered tachy
            :param tachy_thresh (bpm): HR at which above is tachy
            :param units (int): the data is given in ms or sec, put 1000 for ms and 1 for sec
            :rtype: heart rate at the specified time (beats/min)

        """
        self.file = filename
        self.begin_time = begin_time
        self.end_time = end_time
        self.brady_time = brady_time
        self.brady_thresh = brady_thresh
        self.tachy_time = tachy_time
        self.tachy_thresh = tachy_thresh
        self.units = units
        self.errBool = False

        [peak_times, err] = self.peak_detection()
        self.err = err

        self.time = peak_times
        self.find_instant_hr(begin_time)
        self.find_average_hr(begin_time, end_time)
        self.find_anomaly_hr(
            brady_time,
            brady_thresh,
            tachy_time,
            tachy_thresh)

        print(self.brady_tf[29])
        print(self.tachy_tf)

    def file_checker(self, filename, names):
        """Function that checks the file has the right types
            for ECG_data

            :param self: the hrm object
            :param filename: csv file that contains the ecg data
            :param names: header to help pandas work
            :rtype: Boolean for if there is an error

        """

        try:
            df = pandas.read_csv(
                filename, header=None, names=names, converters={
                    "times": float, "voltages": float})
            err_Bool = False
            err = null
            return err_Bool
        except ValueError as err:
            err_Bool = True
            return err_Bool, err

    def threshold(self, voltages, avg_voltage):
        """Function for finding peaks above threshold

            :param self: the hrm object
            :param voltage: a list of voltages from csv file
            :param avg_voltage: Threshold voltage for peaks
            :rtype: list of peaks above threshold
        """

        # Multiply by 2 for a guesstimation of appropriate threshold
        thresh_voltage = abs(avg_voltage) * 2
        peaks = numpy.where(voltages >= thresh_voltage)
        peaks1 = peaks[0]
        peaks2 = peaks1.tolist()

        return peaks2

    def peak_detection(self):
        """Function that finds all the peaks in an ecg and returns them

            :param self: the hrm object
            :rtype: list of peaks (ms)
        """

        # Initialized with zero so that it could iterate through the array properly
        # It was the greatest solution to this challenging dilemna
        peak_times = [0]
        times = numpy.empty
        voltages = numpy.empty

        names = ["times", "voltages"]
        [data_error, err] = self.file_checker(self.file, names)
        if (data_error):
            print("Non-Numeric Value Entered")
            self.errBool = True
            return peak_times, err
        else:
            ecg_data = pandas.read_csv(
                self.file, header=None, names=names, converters={
                    "times": float, "voltages": float})
            times = ecg_data.times.values
            voltages = ecg_data.voltages.values

        # Create Threshold
        avg_voltage = numpy.average(voltages)
        peaks = self.threshold(voltages, avg_voltage)

        first_peak = 0.0
        second_peak = 0.0
        for i in range(1, len(peaks) - 1):
            if (voltages[peaks[i]] >= voltages[peaks[i - 1]]) and \
                    (voltages[peaks[i]] >= voltages[peaks[i + 1]]):
                recent_val = peak_times[len(peak_times) - 1]
                peak_times.append(times[peaks[i]])
                if (len(peak_times) == 2):
                    first_peak = times[peaks[i]]
                if (len(peak_times) ==
                        3 and times[peaks[i]] - recent_val >= 0.1):
                    second_peak = times[peaks[i]]
                elif (len(peak_times) == 3 and times[peaks[i]] - recent_val <= 0.1):
                    peak_times.pop()
                if (times[peaks[i]] - recent_val <=
                        0.5 * (second_peak - first_peak)):
                    peak_times.pop()
        peak_times.pop(0)
        # print(len(peak_times))
        # print(peak_times)

        return peak_times, err

    # @property
    # def find_instant_hr(self):
    #     """Property of the hrm class

    #         :param self: the hrm object
    #         :rtype: the instantaneous heartrate (beats/min)

    #      """

    #    return self.instantaneous_hr and self.instant_hr_target

    # @instantaneous_hr.setter
    def find_instant_hr(self, target_time=0):
        """Function that finds the heart rate at an instant time

            Finds the peak that corresponds to given time, if there
            is not a perfect match, it will pick the closest peak after
            the given time

            :param self: the hrm object
            :param targetTime (ms): time specified by the user
            :rtype: heart rate at the specified time (beats/min)

        """
        self.instantaneous_hr = []  # instantiate list of instantaneous hr

        if target_time > self.time[len(self.time) - 1]:
            raise ValueError('target time is out of range of detected peaks')

        specified_time = 0 #marker for if target time is found
        for x in range(1, len(self.time)):
            temp_dt = self.time[x] - self.time[x - 1]
            temp = (60 / temp_dt) * self.units
            self.instantaneous_hr.append(temp)
            if x == 1:
                self.instantaneous_hr.append(temp)
            if specified_time == 0 & x >= target_time:
                specified_time = 1
                self.instant_hr_target = temp


    # @property
    # def find_average_hr(self):
    #     """Property of the hrm class

    #         :param self: the hrm object
    #         :rtype: the average heart rate (beats/min)

    #     """
    #     return self.average_hr

    # @average_hr.setter
    def find_average_hr(self, begin_time=0, end_time=10):
        """Function that finds the average heart rate over a user specified time

            Like the instant function,
            the peak is chosen from the peak directly after
            the user specified time

            :param self: the hrm object
            :param begin_time (ms): The user specified time at which the avg starts
            :param end_time (ms): User specified time at which the avg ends
            :rtype: Average heart rate over user specified time (beats/min)

        """
        if begin_time >= end_time:
            raise ValueError('Begin time is before end time')
        if self.time[len(self.time) - 1] < end_time:
            raise ValueError('End time occurs outside of range of csv file')
        if self.time[len(self.time) - 1] < begin_time:
            raise ValueError('Begin time occurs outside of range of csv file')

        begin = 0
        end = 0

        # Start at index 1 because checking the j-1 index (to get the 0 pos)
        for j in range(1, len(self.time)):
            if (self.time[j - 1] / self.units == begin_time):
                begin = j - 1
            elif (begin_time == 0):
                begin = 0
            elif (self.time[j - 1] / self.units < begin_time) and \
                    (self.time[j] / self.units > begin_time):
                begin = j
            if (self.time[j - 1] / self.units == end_time):
                end = j - 1
            elif (self.time[j - 1] / self.units < end_time) and \
                    (self.time[j] / self.units > end_time):
                end = j
        time_count = 0

        # Start at begin+1 because checking k-1 index
        # End at end+1 because range function is not inclusive for the last
        # index
        for k in range(begin + 1, end + 1):
            time_count = time_count + \
                (self.time[k] - self.time[k - 1]) / self.units

        div = end - begin
        if div == 0:
            raise ValueError('Begin and End time are too close')

        time_avg = time_count / div
        avg = 60 / time_avg
        self.average_hr = avg

    # @property
    # def find_anomaly_hr(self):
    #     """Property of the hrm class

    #         :param self: the hrm object
    #         :rtype: list of times for bradycardia and tachycardia

    #    """
    #    return [self.brady_times, self.tachy_times]

    # @anomaly_hr.setter
    def find_anomaly_hr(
            self,
            brady_time=5,
            brady_thresh=60,
            tachy_time=5,
            tachy_thresh=100):
        """Function for finding if there is bradycardia or tachycardia

            The parameters are all configurable.

            :param self: the hrm object
            :param brady_thresh (bpm): The threshold for bradycardia, if a
                heart rate is below this, it is considered bradycardia
            :param brady_time (ms): the length of time the low heart rate has
                to last in order to be considered bradycardia
            :param tachy_thresh (bpm): The threshold for tachycardia, if a
                heart rate is above this, it is considered tachycardia
            :param tachy_time (ms): the length of time the high heart rate has
                to last in order to be considered tachycardia
            :rtype: two lists which hold the when bradycardias first occured
                and when tahcycardias first occured (sec)

        """

        brady_detected = 0  # flag for brady detected
        tachy_detected = 0  # flag for tachy detected
        self.brady_times = []  # Instantiate list for bradycardia times
        self.tachy_times = []  # Instantiate list for tachycardia times

        self.brady_tf = [] #Instantiate list for bradycardia true/false beats
        self.tachy_tf = [] #Instantiate list for tachycardia true/false beats

        for l in range(1, len(self.time)):  # loop through all times
            # check if last two heartbeats time under brady thresh
            if (60 *
                self.units /
                (self.time[l] -
                 self.time[l -
                           1])) < brady_thresh and brady_detected == 0:
                # brady_detected is start time of bradycardia
                brady_detected = self.time[l]
            elif (brady_detected != 0) and (60 * self.units / (self.time[l] - self.time[l - 1]) > brady_thresh):
                if self.time[l] - brady_detected > brady_time / self.units:
                    self.brady_times.append(brady_detected / self.units)
                brady_detected = 0

            myTrue = 'true'.strip('\'')
            myFalse = 'false'.strip('\'')
            if ((60 * self.units / (self.time[l] - self.time[l - 1])) <= brady_thresh):
                self.brady_tf.append(myTrue)
            if ((60 * self.units / (self.time[l] - self.time[l - 1])) > brady_thresh):
                self.brady_tf.append(myFalse)
            if ((60 * self.units / (self.time[l] - self.time[l - 1])) >= tachy_thresh):
                self.tachy_tf.append(myTrue)
            if ((60 * self.units / (self.time[l] - self.time[l - 1])) < tachy_thresh):
                self.tachy_tf.append(myFalse)
            if ((60 *
                self.units /
                (self.time[l] -
                 self.time[l -
                           1])) > tachy_thresh and tachy_detected == 0):
                tachy_detected = self.time[l - 1]
            elif (tachy_detected != 0) and (60 * self.units / (self.time[l] - self.time[l - 1]) < tachy_thresh):
                if (self.time[l] - tachy_detected) > (tachy_time / self.units):
                    self.tachy_times.append(tachy_detected / self.units)
                tachy_detected = 0
        self.anomaly_hr = [self.brady_times, self.tachy_times]
        self.anomaly_tf = [self.brady_tf, self.tachy_tf]
