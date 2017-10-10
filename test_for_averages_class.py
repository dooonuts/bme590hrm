import pytest
import hrm_class

def test_for_average_class():
    """Unit test for checking average in ecg_data

    testing default and range

    """

    myHrm = hrm_class.Hrm_data('full_test.csv')

    assert round(myHrm.averageHr(), 0) == 78;

    assert round(myHrm.averageHr(20, 45),0)==42;

def test_outofrange_average_class():
    """Unit test for checking ValueErrors
    
    """
    # test for start time out of range
    with pytest.raises(ValueError):
        myHrm.averageHr(250)

    # test for end time out of range 
    with pytest.raises(ValueError):
        myHrm.averageHr(0, 250)

    #test for start time after end time
    with pytest.raises(ValueError):
        myHrm.averageHr(300, 250)



