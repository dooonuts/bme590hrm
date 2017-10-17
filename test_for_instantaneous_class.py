import pytest
import hrm_class

def test_for_instantaneous_class():
    """Unit test for checking instantaneous functionality
        checks for out of bounds and default heart rate
    
        :param None
        :rtype: Assertions

    """

    myHrm = hrm_class.HrmData('test_data/test_data2.csv')

    assert myHrm.find_instant_hr() == 69

    with pytest.raises(ValueError):
        myHrm.find_instant_hr(30)
