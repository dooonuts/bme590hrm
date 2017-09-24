import pytest
import pytest-pep8
import hrm


def test_for_instantaneous():
    #Test for evaluating instantaneous heart rate
    assert hrm.main('full_test.csv') == 80

    # Test for out of bounds error
    with pytest.raises(ValueError):
        hrm.main('full_test.csv', 250000)  
