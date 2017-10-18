import pytest
import hrm_class

def test_for_instantaneous_class():
    """Unit test for checking instantaneous functionality
        checks for out of bounds and default heart rate
    
        :param None
        :rtype: Assertions

    """

    myHrm = hrm_class.HrmData('full_test.csv')

    round_Instantaneous = round(myHrm.instantaneous_hr,0)
    assert round_Instantaneous == 69


    with pytest.raises(ValueError):
        myHrm.find_instant_hr(30)
