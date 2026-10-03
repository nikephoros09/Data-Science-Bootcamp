import pytest
from financial import fetch
import time

@pytest.fixture(autouse=True)
def sleep_between_tests():
    yield
    time.sleep(3)

def test_correct_res():
    result = fetch('MSFT', 'Total Revenue')
    assert isinstance(result, tuple)
    assert result[0] == 'Total Revenue'
    expected_sample = {'281,724,000', '281,724,000', '245,122,000', '211,915,000', '198,270,000'}
    returned_sample = (result[1:])
    assert expected_sample.issubset(returned_sample)

def test_if_tuple():
    result = fetch('MSFT', 'Total Revenue')
    assert isinstance(result, tuple)

def test_if_tickle_error():
    with pytest.raises(Exception):
        fetch('RANDOMTEXT', 'Total Revenue')

def test_if_col_error():
    with pytest.raises(Exception):
        fetch('MSFT', 'RANDOMTEXT')


    
