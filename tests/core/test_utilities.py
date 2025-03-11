from datetime import date

from constants.tests.utilities import (
    ASSERTED_BASE_URL_1,
    ASSERTED_BASE_URL_2,
    ASSERTED_BASE_URL_3,
    ASSERTED_DATE_1,
    ASSERTED_DATE_2,
    ASSERTED_MONTH_1,
    ASSERTED_MONTH_2,
    ASSERTED_SNAKE_CASE_1,
    ASSERTED_SNAKE_CASE_2,
    ASSERTED_SNAKE_CASE_3,
    ASSERTED_SNAKE_CASE_4,
    ASSERTED_SNAKE_CASE_5,
    ASSERTED_YEAR_1,
    ASSERTED_YEAR_2,
    SNAKE_CASE_1,
    SNAKE_CASE_2,
    SNAKE_CASE_3,
    SNAKE_CASE_4,
    SNAKE_CASE_5,
    TEST_INDONESIAN_DATE_1,
    TEST_INDONESIAN_DATE_2,
    TEST_URL_1,
    TEST_URL_2,
    TEST_URL_3,
)
from core.utilities import camel_to_snake, get_base_url, parse_indonesian_date

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

def test_parse_indonesian_date():
    """
    Function to test Indonesian string date to date obj Python
    :return:
    """
    parsed_test_1 = parse_indonesian_date(TEST_INDONESIAN_DATE_1)
    parsed_test_2 = parse_indonesian_date(TEST_INDONESIAN_DATE_2)

    assert isinstance(parsed_test_1, date), "Wrong data type."
    assert parsed_test_1.year == ASSERTED_YEAR_1, "Wrong year."
    assert parsed_test_1.month == ASSERTED_MONTH_1, "Wrong month."
    assert parsed_test_1.day == ASSERTED_DATE_1, "Wrong date."
    assert isinstance(parsed_test_2, date), "Wrong data type."
    assert parsed_test_2.year != ASSERTED_YEAR_1, "Wrong year."
    assert str(parsed_test_2.year) == str(ASSERTED_YEAR_2), "Wrong year."
    assert parsed_test_2.month == ASSERTED_MONTH_2, "Wrong month."
    assert parsed_test_2.day == ASSERTED_DATE_2, "Wrong date."
