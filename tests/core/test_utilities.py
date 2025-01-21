from constants.tests.utilities import (
    ASSERTED_BASE_URL_1,
    ASSERTED_BASE_URL_2,
    ASSERTED_BASE_URL_3,
    ASSERTED_SNAKE_CASE_1,
    ASSERTED_SNAKE_CASE_2,
    ASSERTED_SNAKE_CASE_3,
    ASSERTED_SNAKE_CASE_4,
    ASSERTED_SNAKE_CASE_5,
    SNAKE_CASE_1,
    SNAKE_CASE_2,
    SNAKE_CASE_3,
    SNAKE_CASE_4,
    SNAKE_CASE_5,
    TEST_URL_1,
    TEST_URL_2,
    TEST_URL_3,
)
from core.utilities import camel_to_snake, get_base_url

def test_camel_to_snake():
    """
    Function to test Camel_to_Snake function on Utilities
    :return:
    """
    assert camel_to_snake(SNAKE_CASE_1) == ASSERTED_SNAKE_CASE_1
    assert camel_to_snake(SNAKE_CASE_2) == ASSERTED_SNAKE_CASE_2
    assert camel_to_snake(SNAKE_CASE_3) == ASSERTED_SNAKE_CASE_3
    assert camel_to_snake(SNAKE_CASE_4) == ASSERTED_SNAKE_CASE_4
    assert camel_to_snake(SNAKE_CASE_5) == ASSERTED_SNAKE_CASE_5

def test_get_base_url():
    """
    Function to test get_base_url function on Utilities
    :return:
    """
    assert get_base_url(TEST_URL_1) == ASSERTED_BASE_URL_1
    assert get_base_url(TEST_URL_2) == ASSERTED_BASE_URL_2
    assert get_base_url(TEST_URL_3) == ASSERTED_BASE_URL_3
