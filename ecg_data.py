import numpy
import pandas

class Ecg_data:
    'This is a class'

    def __init__(self, filename, begin_time = 0, end_time = 10,bradyT = 5,bradyThresh = 60, \
            tachyT = 5,tachyThresh = 100):
        # put peak detection here
        data = pandas.read_csv('testfile.txt', converters={"times": float, "voltages": float})
        voltages = data.voltages.values
        finalTimes = [0]
        avgvoltage = numpy.average(voltages)

        threshvoltage = avgvoltage * 2

        peaks = numpy.where(voltages >= threshvoltage)
        peaks1 = peaks[0]
        peaks2 = peaks1.tolist()
        boxcar = []
        for i in range(1, len(peaks2) - 1):
            if (voltages[peaks2[i]] >= voltages[peaks2[i - 1]]) and (voltages[peaks2[i]] >= voltages[peaks2[i + 1]]):
                recentval = finalTimes[len(finalTimes) - 1]
                finalTimes.append(peaks2[i])
                if (peaks2[i] - recentval <= 50):
                    finalTimes.pop()
        finalTimes.pop(0)

        self.times = finalTimes
        self.inst  = self.instantHr(avgT1)
        self.avg   = self.averageHR(begin_time,end_time)
        self.ano   = self.anomalyHr(bradyT, bradyThresh, tachyT, tachyThresh)

    def instantHr(self, avgT1):
        for x in range(0, len(self.time)):
            if self.time[x] > avgT1:
                instant_dt = self.time[x+1] - self.time[x]
                break

        return (60 / instant_dt)*100

    def averageHr(self,begin_time,end_time):
            for j in range(1, len(self.time)):
                if (self.time[j-1]/1000 == begin_time):
                    begin = j-1
                elif (self.time[j-1]/1000 < begin_time and self.time[j]/1000 > begin_time):
                    begin = j
                if (self.time[j-1]/1000 == end_time):
                    end = j-1
                elif (self.time[j-1]/1000 < end_time) and (self.time[j]/1000 > end_time):
                    end = 1
            time_count = 0

            for k in range(begin+1, end+1):
                time_count = time_count + (self.time[k] - self.time[k-1])/1000

            div = end - begin

            time_avg = time_count / div
            return 60 / time_avg


    def anomalyHr(self,bradyT,bradyThresh,tachyT,tachyThresh):
        dying_slow = 0
        dying_fast = 0
        bradyTimes = []
        tachyTimes = []
        counter = 0
        for l in range(1, len(self.time)):
            if 600000/(self.time[l]-self.time[l-1]) < bradyThresh and dying_slow == 0:
                dying_slow = self.time[l-1]
            elif dying_slow != 0 and 60000/ (self.time[l]-self.time[l-1]) > bradyThresh:
                if self.time[l] - dying_slow > self.bradyT:
                    bradyTimes.append(dying_slow/1000)
                dying_slow = 0
            if 60000/ (self.time[l]-self.time[l-1]) < tachyThresh and dying_fast == 0:
                dying_fast = self.time[l-1]
            elif dying_fast != 0 and 60000/ (self.time[l]-self.time[l-1]) < tachyThresh:
                if self.time[l] - dying_fast > tachyT:
                    tachyTimes.append(dying_fast/1000)
                dying_fast = 0

        return bradyTimes, tachyTimes