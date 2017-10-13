import numpy
import pandas

class hrm_data:
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
            bradyT=5,
            bradyThresh=60,
            tachyT=5,
            tachyThresh=100):
        """Function that initializes stuff for the whole function

            Finds the peak that corresponds to given time, if there
            is not a perfect match, it will pick the closest peak after
            the given time

            :param self: the hrm object
            :param targetTime: time specified by the user
            :rtype: heart rate at the specified time

        """

        peakTimes = [0]

        # put peak detection here
        names = ["times", "voltages"]
        dataerror = self.fileChecker(filename, names)
        if (dataerror):
            print("Non-Numeric Value Entered")
        else:
            ecg_data = pandas.read_csv(
                filename, header=None, names=names, converters={
                    "times": float, "voltages": float})

        times = ecg_data.times.values
        voltages = ecg_data.voltages.values

        # Create Threshold
        avgvoltage = numpy.average(voltages)
        threshvoltage = abs(avgvoltage) * 2

        peaks = numpy.where(voltages >= threshvoltage)
        peaks1 = peaks[0]
        peaks2 = peaks1.tolist()
        first_peak = 0.0
        second_peak = 0.0
        for i in range(1, len(peaks2) - 1):
            if (voltages[peaks2[i]] >= voltages[peaks2[i - 1]]) and \
                    (voltages[peaks2[i]] >= voltages[peaks2[i + 1]]):
                recentval = peakTimes[len(peakTimes) - 1]
                peakTimes.append(times[peaks2[i]])
                if (len(peakTimes) == 2):
                    first_peak = times[peaks2[i]]
                if (len(peakTimes) == 3):
                    second_peak = times[peaks2[i]]
                if (times[peaks2[i]] - recentval <= 0.5 * (second_peak - first_peak)):
                    peakTimes.pop()
        peakTimes.pop(0)
        print(len(peakTimes))
        print(peakTimes)

        self.time = peakTimes
        self.inst = self.instantHr(begin_time)
        self.avg = self.averageHr(begin_time, end_time)
        self.ano = self.anomalyHr(bradyT, bradyThresh, tachyT, tachyThresh)

    def fileChecker(self, filename, names):
        try:
            df = pandas.read_csv(
                filename, header=None, names=names, converters={
                    "times": float, "voltages": float})
            errBool = False
            return errBool
        except ValueError:
            errBool = True
            return errBool

    def instantHr(self, target_time=0):
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
        self.inst = inst

    def averageHr(self, begin_time=0, end_time=10):
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
        self.avg = avg

    def anomalyHr(self, bradyT=5, bradyThresh=60, tachyT=5, tachyThresh=100):
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

        self.ano = [self.bradyTimes, self.tachyTimes]
