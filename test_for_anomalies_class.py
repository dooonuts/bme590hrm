import pytest
import ecg_data

def test_for_anomalies_class():
    """Unit test for anomaly method in ecg_data
        class based approach

        Testing for multiple times

    """

    myObject = Ecg_data('fulltest.csv')
    [bradyTimes, taachyTimes] = a.anomalyHr()
    print (bradyTimes)
    print (tachyTimes)

    assert round(bradyTimes[0],0)==30
    assert round(tachyTimes[0],0)==75
    assert round(bradyTimes[1],0)==150
    assert round(tachyTimes[1],0)==195
