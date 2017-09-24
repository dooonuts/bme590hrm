import pytest
import pytest-pep8
import hrm

def test_average():
    """
        Unit test for checking basic functionality
        of the average function in hrm

        :param None
        :rtype: Assertions
    """

    # Test for default values of average
    assert hrm.main(full_test, avg = True)==80;

    # Test for range 
    assert hrm.main(full_test, 30, 45, avg = True)==50;

def test_outofrange_average():
    """
        Unit test for checking ValueErrors in
        the average function in hrm

        :param None
        :rtype: Errors
    """

    # Test for the beginning is out of range
    with pytest.raises(ValueError):
        hrm.main(full_test, 250002, avg = True)

    # Test for ending out of range
    with pytest.raises(ValueError):
        hrm.main(full_test, 0, 2500002, avg=True)
    
    # Test for if begin time is after end time
    with pytest.raises(ValueError):
        hrm.main(full_test, 300, 250, avg=True)
