import pytest
import hrm_class

def test_for_instantaneous_class():
    """Unit test for checking instantaneous functionality
        checks for out of bounds and default heart rate
    
        :param None
        :rtype: Assertions

    """

    myHrm = hrm_class.HrmData('full_test.csv')

    assert myHrm.find_instant_hr() == 80

    with pytest.raises(ValueError):
        myHrm.find_instant_hr(250)
