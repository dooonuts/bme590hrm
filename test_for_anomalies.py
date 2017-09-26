import pytest
import hrm

def test_for_anomalies():
    """ Unit test for the anomaly function
        in hrm

        :param None
        :rtype: Assertions
    """
    # Test for if function can find more than one brady site

    [bradyTimes, tachyTimes] = hrm.main('full_test.csv', 0, 30, 50, 100, 10, 10, ano = True)
    print (bradyTimes)
    print (tachyTimes)
    assert round(bradyTimes[0], 0) == 30
    assert round(tachyTimes[0], 0) == 75
    assert round(bradyTimes[1], 0) == 150
    assert round(tachyTimes[1], 0) == 195

    # Test for if cant find any
    [bradyNone, tachyNone] = hrm.main('full_test.csv', 0, 30, 10, 120, 10, 10, ano = True)
    assert bradyTimes == []
    assert tachyTimes == []


