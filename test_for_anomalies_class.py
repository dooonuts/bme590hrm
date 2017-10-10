import pytest
import ecg_data

def test_for_anomalies_class():
    """Unit test for anomaly method in ecg_data
        class based approach

        Testing for multiple times

    """

    myHrm = ecg_data.ECG_data('fulltest.csv')
    [bradyTimes, tachyTimes] = myHrm.anomalyHr()

    assert round(bradyTimes[0],0)==30
    assert round(tachyTimes[0],0)==75
    assert round(bradyTimes[1],0)==150
    assert round(tachyTimes[1],0)==195
