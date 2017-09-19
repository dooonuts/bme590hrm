import pytest
import pytest_pep8
import hrm

def test_average():

    # Test for default values of average
    assert hrm.main(full_test, avg = True)==80;

    # Test for range 
    assert hrm.main(full_test, 0, 1000, avg = True)==120;

def test_outofrange_average():

    # Test for the beginning is out of range
    with pytest.raises(ValueError):
        hrm.main(full_test, 250002, avg = True)

    # Test for ending out of range
    with pytest.raises(ValueError):
        hrm.main(full_test, 0, 2500002, avg=True)
    
    # Test for if begin time is after end time
    with pytest.raises(ValueError):
        hrm.main(full_test, 300, 250, avg=True)
