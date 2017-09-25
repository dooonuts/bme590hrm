import pytest
import pep8
import hrm

def test_average():
    """ Unit test for checking average fun in hrm
        
        :param None
        :rtype: Assertions
    """

    # Test for default values of average
    assert hrm.main('full_test.cs', avg = True)==80;

    # Test for range 
    assert hrm.main('full_test.csv', 30, 45, avg = True)==50;

def test_outofrange_average():
    """ Unit test for checking ValueErrors in avg fun of hrm

        :param None
        :rtype: Errors
    """

    # Test for the beginning is out of range
    with pytest.raises(ValueError):
        hrm.main('full_test.csv', 250002, avg = True)

    # Test for ending out of range
    with pytest.raises(ValueError):
        hrm.main('full_test.csv', 0, 2500002, avg=True)

    # Test for if begin time is after end time
    with pytest.raises(ValueError):
        hrm.main('full_test.csv', 300, 250, avg=True)
