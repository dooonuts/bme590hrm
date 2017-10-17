import pytest
import hrm


def test_average():
    """Unit test for checking average fun in hrm

        testing for default and range

        :param None
        :rtype: Assertions
    """

    # Test for default values of average
    assert round(hrm.main('test_data/test_data2.csv', avg=True), 0) == 78

    # Test for range
    assert round(hrm.main('test_data/test_data2.csv', 30, 45, avg=True), 0) == 42


def test_outofrange_average():
    """Unit test for checking ValueErrors in avg fun of hrm

        :param None
        :rtype: Errors
    """

    # Test for the beginning is out of range
    with pytest.raises(ValueError):
        hrm.main('test_data/test_data2.csv', 250, avg=True)

    # Test for ending out of range
    with pytest.raises(ValueError):
        hrm.main('test_data/test_data2.csv', 0, 250, avg=True)

    # Test for if begin time is after end time
    with pytest.raises(ValueError):
        hrm.main('test_data/test_data2.csv', 300, 250, avg=True)
