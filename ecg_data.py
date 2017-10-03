class Ecg_data:
    'This is a class'

    def __init__(self, filename, avgT1 = 0, avgT2 = 10,bradyT = 5,bradyThresh = 60, \
            tachyT = 5,tachyThresh = 100):
        # put peak detection here
        self.times = #peak detection array
        self.inst  = instantHr(avgT1)
        self.avg   = averageHR(avgT1, avgT2)
        self.ano   = anomalyHr(bradyT, bradyThresh, tachyT, tachyThresh)

    def instantHr(self, avgT1):
        for x in range(0, len(self.time)):
            if self.time[x] > avgT1:
                instant_dt = self.time[x+1] - self.time[x]
                break
        self.inst = (60 / instant_dt)*100

    def averageHr(self,avgT1,avgT2):

    def anomalyHr(self,bradyT,bradyThresh,tachyT,tachyThresh):

