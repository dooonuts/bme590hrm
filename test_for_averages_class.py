import pytest
import hrm_class

def test_for_average_class():
    """Unit test for checking average in ecg_data

        testing default and range
        
        :param None
        :rtype: Assertions

    """

    myHrm = hrm_class.HrmData('test_data/test_data2.csv')

    assert round(myHrm.average_hr, 0) == 67;

    myHrm.find_average_hr(10,20)
    assert round(myHrm.average_hr,0)==72;

def test_outofrange_average_class():
    """Unit test for checking ValueErrors
        
        :param None
        :rtype: Errors
    
    """

    myHrm = hrm_class.HrmData('test_data/test_data2.csv')

    # test for start time out of range
    with pytest.raises(ValueError):
        myHrm.find_average_hr(30)

    # test for end time out of range 
    with pytest.raises(ValueError):
        myHrm.find_average_hr(0, 30)

    # test for start time after end time
    with pytest.raises(ValueError):
        myHrm.find_average_hr(30, 25)



