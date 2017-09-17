import pytest
import ***ECG_fun****
import csv

def test_for_bradycardia():
    # Test for the default value of bradycardia, and moving it

    assert hrm.main('test.csv') == "Bradycardia found at " + str(40)
    assert hrm.main('test.csv', 2000, 30) == "Bradycardia not found"


def test_for_tachycardia():
    # Test for the default value of tachycardia, and it moving

    assert hrm.main('test.csv') == "Tachycardia found at " + str(70)
    assert hrm.main('test.csv', 2000, 50, 120) == "Tachycardia not found"



