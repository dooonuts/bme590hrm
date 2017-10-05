class Ecg_data:
    'This is a class'

    def __init__(self, filename, begin_time = 0, end_time = 10,bradyT = 5,bradyThresh = 60, \
            tachyT = 5,tachyThresh = 100):
        # put peak detection here
        self.times = #peak detection array
        self.inst  = instantHr(avgT1)
        self.avg   = averageHR(begin_time,end_time)
        self.ano   = anomalyHr(bradyT, bradyThresh, tachyT, tachyThresh)

    def instantHr(self, avgT1):
        for x in range(0, len(self.time)):
            if self.time[x] > avgT1:
                instant_dt = self.time[x+1] - self.time[x]
                break
        self.inst = (60 / instant_dt)*100

    def averageHr(self,begin_time,end_time:
            for i in range(1, len(time)):
                if (time[i-1]/1000 == begin_time):
                    begin = i-1
                elif (time[i-1]/1000 < begin_time and time[i]/1000 > begin_time):
                    begin = i
                if (time[i-1]/1000 == end_time):
                    end = i-1
                elif (time[i-1]/1000 < end_time) and (time[i]/1000 > end_time):
                    end = 1
>>>>>>> e65cb5ce0edc47cdd26bf19f913fde25eb6a652b

            time_count = 0

            for k in range(begin+1, end+1):
                time_count = time_count + (time[k] - time[k-1])/1000

            div = end - begin

            time_avg = time_count / div
            return 60 / time_avg


    def anomalyHr(self,bradyT,bradyThresh,tachyT,tachyThresh):
        dying_slow = 0
        dying_fast = 0
        bradyTimes = []
        tachyTimes = []
        counter = 0
        for i in range(1, len(time)):
            if 600000/(time[i]-time[i-1]) < brady_thresh and dying_slow == 0:
                dying_slow = time[i-1]
            elif dying_slow != 0 and 60000/ (time[i]-time[i-1]) > brady_thresh:
                if time[i] - dying_slow > brady_time:
                    bradyTimes.append(dying_slow/1000)
                dying_slow = 0
            if 60000/ (time[i]-time[i-1]) < tachy_thresh and dying_fast == 0:
                dying_fast = time[i-1]
            elif dying_fast != 0 and 60000/ (time[i]-time[i-1]) < tachy_thresh:
                if time[i] - dying_fast > tachy_time:
                    tachyTimes.append(dying_fast/1000)
                dying_fast = 0

        return bradyTimes, tachyTimes
