import pytest
import hrm_class

def test_for_instantaneous_class():
    """Unit test for checking instantaneous functionality
        checks for out of bounds and default heart rate
    
        :param None
        :rtype: Assertions

    """

    myHrm = hrm_class.Hrm_data('full_test.csv')

    assert myHrm.instantHr() == 80

    with pytest.raises(ValueError):
        myHrm.instantHr(250)
