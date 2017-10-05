import pytest
import ecg_data

def test_for_average_class():
    """Unit test for checking average in ecg_data

    testing default and range

    """

    myObject = Ecg_data('full_test.csv')

    assert round(myObject.averageHr('full_test.csv',avg = True), 0) == 78;

    assert round(myObject.averageHr('full_test.csv',30,45,avg=True),0)==42;

def test_outofrange_average_class():
    """Unit test for checking ValueErrors
    """
    # test for start time out of range
    with pytest.raises(ValueError):
        myObject.averageHr('full_test.csv',250,avg=True)

    # test for end time out of range 
    with pytest.raises(ValueError):
        myObject.averageHr('full_test.csv',0,250,avg=True)

    #test for start time after end time
    with pytest.raises(ValueError):
        myObject.averageHr('full_test.csv',300,250,avg=True)



