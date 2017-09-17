import pytest
import hrm.py
import csv

def test_for_instantaneous():
    #Test for evaluating instantaneous heart rate

    assert hrm.mail('full_test.csv') == "Instantaneous HR: " + str(80)