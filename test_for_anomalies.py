import pytest
import hrm
import instant_test
import full_test

def test_for_gtone_brady():
    # Test for if function can find more than one brady site

    assert hrm.main('full_test.csv', ano = True) 


def test_for_tachycardia():
    # Test for the default value of tachycardia, and it moving

    assert hrm.main('instant_test.csv', ano = True) \
            == "Tachycardia found at " + str(75)
    assert hrm.main('instant_test.csv', tachy_threshold = 120, \
            ano = True) == "Tachycardia not found"

def test_for_gtone_tachy():
    # Test for if the function can find more than one tachy site

    assert hrm.main('full_test.csv', ano = True) \
            == "Tachycardia found at " + str(75) + ", " + str(165)


