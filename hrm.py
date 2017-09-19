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

def instant(time, peak):
    """Insert function here"""

def average(time, peak):
    """Insert function here"""

def anomaly(time, peak):
    """Insert function here"""

def main(ecg_data, user_specified_time1=0, user_specified_time2=2000, brady_threshold = 50, tachy_threshold = 100, \
         int = False, avg = False, ano = False):

    """Insert function here"""

    ecg_dict = peakDetector('full_test.csv')



if __name__ == '__main__':
    main('full_test.csv');