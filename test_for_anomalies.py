import pytest
import hrm
import instant_test
import full_test

def test_for_anomalies():
    # Test for if function can find more than one brady site

    [bradyTimes, tachyTimes] = hrm.main('full_test.csv', 50, 10, 120, 10, ano = True) 
    assert bradyTimes[0] == 30
    assert tachyTimes[0] == 75
    assert bradyTimes[1] == 150
    assert tachyTimes[1] == 195

    # Test for if cant find any
    [bradyNone, tachyNone] = hrm.main('full_test.csv',30,10,120,20, ano = True)
    assert bradyTimes == []
    assert tachyTimes == []


