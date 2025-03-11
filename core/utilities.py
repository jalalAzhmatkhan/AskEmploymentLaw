from datetime import datetime, date
import locale
import platform
import re
from typing import Optional
from urllib.parse import urlparse

from constants.general import (
    INDONESIAN_WINDOWS_LOCALE,
    INDONESIAN_LINUX_LOCALE,
    OS_WINDOWS,
)


def camel_to_snake(camel_case_string: str)->str:
    """
    Convert a CamelCase string to snake_case.

    Args:
        camel_case_string (str): The input CamelCase string.

    Returns:
        str: The converted snake_case string.
    """
    # Add underscores before each uppercase letter followed by lowercase or digits
    snake_str = re.sub(r'(?<=[a-z0-9])([A-Z])', r'_\1', camel_case_string)
    # Add underscores between digits and letters if not already separated
    snake_str = re.sub(r'([A-Za-z])(\d)', r'\1_\2', snake_str)
    snake_str = re.sub(r'(\d)([A-Za-z])', r'\1_\2', snake_str)
    return snake_str

def get_base_url(url: str)->str:
    """
    Function to get base URL
    :param url:
    :return:
    """
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

def parse_indonesian_date(
    datestr: str,
    date_format: Optional[str] = "%d %B %Y",
)->date:
    """
    Function to convert Indonesian date string to date object
    :param datestr:
    :param date_format:
    :return:
    """
    if platform.system() == OS_WINDOWS:
        locale.setlocale(locale.LC_TIME, INDONESIAN_WINDOWS_LOCALE)  # Windows locale
    else:
        locale.setlocale(locale.LC_TIME, INDONESIAN_LINUX_LOCALE)  # Linux/MacOS locale

    return datetime.strptime(datestr, date_format).date()
