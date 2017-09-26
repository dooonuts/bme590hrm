import pytest
import hrm

def test_for_anomalies():
    """ Unit test for the anomaly function
        in hrm

        :param None
        :rtype: Assertions
    """
    # Test for if function can find more than one brady site

    [bradyTimes, tachyTimes] = hrm.main('full_test.csv', 0, 30, 50, 120, 10, 10, ano = True)
    print (bradyTimes)
    print (tachyTimes)
    assert bradyTimes[0] == 30
    assert tachyTimes[0] == 75
    assert bradyTimes[1] == 150
    assert tachyTimes[1] == 195

    # Test for if cant find any
    [bradyNone, tachyNone] = hrm.main('full_test.csv',0,30,30,120,10,20, ano = True)
    assert bradyTimes == []
    assert tachyTimes == []


