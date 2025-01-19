from constants.tests.utilities import (
    ASSERTED_SNAKE_CASE_1,
    ASSERTED_SNAKE_CASE_2,
    ASSERTED_SNAKE_CASE_3,
    ASSERTED_SNAKE_CASE_4,
    ASSERTED_SNAKE_CASE_5,
    SNAKE_CASE_1,
    SNAKE_CASE_2,
    SNAKE_CASE_3,
    SNAKE_CASE_4,
    SNAKE_CASE_5
)
from core.utilities import camel_to_snake

def test_camel_to_snake():
    """
    Function to test Camel_to_Snake function on Utilities
    :return:
    """
    assert camel_to_snake(SNAKE_CASE_1).lower() == ASSERTED_SNAKE_CASE_1
    assert camel_to_snake(SNAKE_CASE_2).lower() == ASSERTED_SNAKE_CASE_2
    assert camel_to_snake(SNAKE_CASE_3).lower() == ASSERTED_SNAKE_CASE_3
    assert camel_to_snake(SNAKE_CASE_4).lower() == ASSERTED_SNAKE_CASE_4
    assert camel_to_snake(SNAKE_CASE_5).lower() == ASSERTED_SNAKE_CASE_5
