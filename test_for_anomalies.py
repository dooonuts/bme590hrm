import pytest
import hrm

def test_for_anomalies():
    """ Unit test for the anomaly function
        in hrm

        :param None
        :rtype: Assertions
    """
    # Test for if function can find more than one brady site

    [bradyTimes, tachyTimes] = hrm.main('full_test.csv', 50, 10000, 120, 10000, ano = True) 
    assert bradyTimes[0] == 30
    assert tachyTimes[0] == 75
    assert bradyTimes[1] == 150
    assert tachyTimes[1] == 195

    # Test for if cant find any
    [bradyNone, tachyNone] = hrm.main('full_test.csv',30,10000,120,20000, ano = True)
    assert bradyTimes == []
    assert tachyTimes == []


