import base64
from datetime import datetime, date
import hashlib
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
from core.logger import logger

def bytes_to_base64(
    input_file: bytes
)->Optional[str]:
    """Function to convert bytes to base64"""
    response = None
    try:
        response = base64.b64encode(input_file).decode('utf-8')
    except Exception as e:
        logger.error(f"bytes_to_base64: {e}")
    return response

def base64_to_bytes(
    input_base64: str
)->Optional[bytes]:
    """Function to convert base64 to bytes"""
    response = None
    try:
        response = base64.b64decode(input_base64)
    except Exception as e:
        logger.error(f"base64_to_bytes: {e}")
    return response

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

def hash_a_file(file, algorithm: str = 'sha256'):
    """Hashes the content of a file using the specified algorithm."""
    hash_func = hashlib.new(algorithm)
    for chunk in iter(lambda: file.read(4096), b""):
        hash_func.update(chunk)
    file.seek(0)  # Reset file pointer after hashing
    return hash_func.hexdigest()

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
