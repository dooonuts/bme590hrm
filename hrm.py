#HRM

import pytest
import pytest_pep8
import numpy

def peakDetector(ecg_data):
    """Insert function here"""

    with open(ecg_data) as csvfile:
        heartreader = csv.DictReader(csvfile)
    


def instant(time, peak):
    """Insert function here"""

def average(time, peak):
    """Insert function here"""

def anomaly(time, peak):
    """Insert function here"""

def main(ecg_data, user_specified_time, brady_threshold = 50, tachy_threshold = 100, \
         int = False, avg = False, ano = False):

    """Insert function here"""

    ecg_dict = peakDetector(ecg_data)
    
