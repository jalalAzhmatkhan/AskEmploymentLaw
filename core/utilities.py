import re
from urllib.parse import urlparse

import bcrypt

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

def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.

    :param password: The plaintext password to hash.
    :return: A hashed password as a string.
    """
    if not isinstance(password, str) or not password:
        raise ValueError("Password must be a non-empty string.")

    # Convert the password to bytes
    password_bytes = password.encode('utf-8')
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a hashed password.

    :param password: The plaintext password to verify.
    :param hashed_password: The hashed password to compare with.
    :return: True if the password matches, False otherwise.
    """
    if not isinstance(password, str) or not isinstance(hashed_password, str):
        raise ValueError("verify_password: Both password and hashed_password must be strings.")

    # Convert inputs to bytes
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    # Verify the password
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)
