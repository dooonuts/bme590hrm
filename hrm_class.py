import numpy
import pandas

class HrmData:
    """This is a HRM class

       __init__ finds the peaks and sets the initial parameters
       instantHr finds the instantaneous hr at a given time
       averageHr finds the average hr over a period of time
       anomalyHr determines if there is brady/tachy and where they occurred

       Attributes:
            times (list): list of times that a peak occurs
            inst   (int): the last instantaneous hr computed
            avg    (int): the last average hr computed
            ano   (list): list of times the anomalies occurred
            bradyTimes
            tachyTimes

    """

    def __init__(
            self,
            filename,
            begin_time=0,
            end_time=10,
            brady_time=5,
            brady_thresh=60,
            tachy_time=5,
            tachy_thresh=100):
        """Function that initializes values for the whole function

            Finds the peak that corresponds to given time, if there
            is not a perfect match, it will pick the closest peak after
            the given time

            :param self: the hrm object
            :param filename: csv file where the ECG data will be stored
            :param begin_time: time for instHr and 1st time for avg (ms)
            :param end_time: time where the avgHr will end (ms)
            :param bradyT: time brady has to last to be considered brady (ms)
            :param bradyThresh: HR at which below is brady (beats/min)
            :param tachyT: time tachy has to last to be considered tachy (ms)
            :param tachyThresh: HR at which above is tachy (beats/min)
            :rtype: heart rate at the specified time (beats/min)

        """
        self.file         = filename
        self.begin_time   = begin_time
        self.end_time     = end_time
        self.brady_time   = brady_time
        self.brady_thresh = brady_thresh
        self.tachy_time   = tachy_time
        self.tachy_thresh = tachy_thresh

        peak_times = peak_detection()

        self.time = peak_times
        self.find_instant_hr(begin_time)
        self.find_average_hr(begin_time, end_time)
        self.find_anomaly_hr(brady_time, brady_thresh, tachy_time, tachy_thresh)

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
                filename, header = None, names = names, converters = {
                    "times": float, "voltages": float})
            err_Bool = False
            return err_Bool
        except ValueError:
            err_Bool = True
            return err_Bool

    def peak_detection(self):
        """Function that finds all the peaks in an ecg and returns them

            :param self: the hrm object
            :rtype: list of peaks 
        """

        peak_times = [0]

        # put peak detection here
        names = ["times", "voltages"]
        data_error = self.file_checker(self.file, names)
        if (data_error):
            print("Non-Numeric Value Entered")
        else:
            ecg_data = pandas.read_csv(
                filename, header = None, names = names, converters = {
                    "times": float, "voltages": float})

        times = ecg_data.times.values
        voltages = ecg_data.voltages.values

        # Create Threshold
        avg_voltage = numpy.average(voltages)
        thresh_voltage = abs(avg_voltage) * 2

        peaks = numpy.where(voltages >= thresh_voltage)
        peaks1 = peaks[0]
        peaks2 = peaks1.tolist()
        first_peak = 0.0
        second_peak = 0.0
        for i in range(1, len(peaks2) - 1):
            if (voltages[peaks2[i]] >= voltages[peaks2[i - 1]]) and \
                    (voltages[peaks2[i]] >= voltages[peaks2[i + 1]]):
                recent_val = peak_times[len(peakTimes) - 1]
                peak_times.append(times[peaks2[i]])
                if (len(peak_times) == 2):
                    first_peak = times[peaks2[i]]
                if (len(peak_times) == 3):
                    second_peak = times[peaks2[i]]
                if (times[peaks2[i]] - recent_val <= 0.5 * (second_peak - first_peak)):
                    peak_times.pop()
        peak_times.pop(0)
        print(len(peak_times))
        print(peak_times)

        return peak_times


    def find_instant_hr(self, target_time = 0):
        """Function that finds the heart rate at an instant time

            Finds the peak that corresponds to given time, if there
            is not a perfect match, it will pick the closest peak after
            the given time

            :param self: the hrm object
            :param targetTime: time specified by the user
            :rtype: heart rate at the specified time

        """
        for x in range(0, len(self.time)):
            if self.time[x] > target_time:
                instant_dt = self.time[x + 1] - self.time[x]
                break

        inst = (60 / instant_dt) * 100
        self.instantaneousHr = inst

    def find_average_hr(self, begin_time=0, end_time=10):
        """Function that finds the average heart rate over a user specified time

            Like the instant function,
            the peak is chosen from the peak directly after
            the user specified time

            :param self: the hrm object
            :param begin_time: The user specified time at which the avg starts
            :param end_time: User specified time at which the avg ends
            :rtype: Average heart rate over user specified time

        """
        begin = 0
        end = 0

        for j in range(1, len(self.time)):
            if (self.time[j - 1] / 1000 == begin_time):
                begin = j - 1
            elif (self.time[j - 1] / 1000 < begin_time) and \
                    (self.time[j] / 1000 > begin_time):
                begin = j
            if (self.time[j - 1] / 1000 == end_time):
                end = j - 1
            elif (self.time[j - 1] / 1000 < end_time) and \
                    (self.time[j] / 1000 > end_time):
                end = j
        time_count = 0

        for k in range(begin + 1, end + 1):
            time_count = time_count + (self.time[k] - self.time[k - 1]) / 1000

        div = end - begin

        time_avg = time_count / div
        avg = 60 / time_avg
        self.averageHr = avg

    def find_anomaly_hr(self, bradyT=5, bradyThresh=60, tachyT=5, tachyThresh=100):
        """Function for finding if there is bradycardia or tachycardia

            The parameters are all configurable.

            :param self: the hrm object
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
        self.bradyTimes = []
        self.tachyTimes = []
        for l in range(1, len(self.time)):
            if 600000 / (self.time[l] - self.time[l - 1]) < bradyThresh \
                    and dying_slow == 0:
                dying_slow = self.time[l - 1]
            elif (dying_slow != 0) and \
                    (60000 / (self.time[l] - self.time[l - 1]) > bradyThresh):
                if self.time[l] - dying_slow > bradyT:
                    self.bradyTimes.append(dying_slow / 1000)
                dying_slow = 0
            if (60000 / (self.time[l] - self.time[l - 1])) < \
                    (self.tachyThresh and dying_fast == 0):
                dying_fast = self.time[l - 1]
            elif (dying_fast != 0) and \
                    (60000 / (self.time[l] - self.time[l - 1]) < tachyThresh):
                if self.time[l] - dying_fast > tachyT:
                    self.tachyTimes.append(dying_fast / 1000)
                dying_fast = 0

        self.anomalyHr = [self.bradyTimes, self.tachyTimes]
