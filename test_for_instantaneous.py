import pytest
import hrm


def test_for_instantaneous():
    """Unit test for checking instantaneous functionality

        Checks for out of bounds and default heart beat

        :param None
        :rtype: Assertions
    """
    # Test for evaluating instantaneous heart rate
    inst = hrm.main('full_test.csv',inst=True)
    assert round(inst,0) == 60

    # Test for out of bounds error
    with pytest.raises(ValueError):
        hrm.main('full_test.csv', 250000, inst=True)
