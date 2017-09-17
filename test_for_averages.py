import pytest
import pytest_pep8
import hrm
import full_test

def test_average():
    assert hrm.main(full_test, avg = True)==80;
    assert hrm.main(full_test, avg = True)==120;
    assert hrm.main(full_test, avg = False)==40;