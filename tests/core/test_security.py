from datetime import datetime, timedelta
from jose import jwt, JWTError
import pytest

from constants.core import security as security_constants
from core.security import create_access_token, hash_password, verify_password
from tests import faker

def test_create_access_token():
    """
    A unit test function to test Access Token generation token
    :return:
    """
    role_ids_test_case_1 = [1]
    permissions_test_case_1 = ["read", "write"]
    subject_test_case_1 = faker.email()
    expires_delta_test_case_1 = timedelta(minutes=1)

    token_test_case_1 = create_access_token(
        role_ids_test_case_1,
        permissions_test_case_1,
        subject_test_case_1,
        expires_delta_test_case_1,
        "abc12345DeF!",
    )

    assert isinstance(token_test_case_1, str), "The generated token should be a string"
    assert len(token_test_case_1) > 0, "The generated token should not be empty"

    try:
        decoded_token_test_case_1 = jwt.decode(
            token_test_case_1,
            "abc12345DeF!",
            algorithms=[security_constants.ENCODING_ALGORITHM]
        )
        assert decoded_token_test_case_1["sub"] == subject_test_case_1, "Subject mismatch."
        assert decoded_token_test_case_1["role_ids"] == role_ids_test_case_1, "Role IDs mismatch."
        assert decoded_token_test_case_1["scopes"] == permissions_test_case_1, "Permissions mismatch."
        assert isinstance(decoded_token_test_case_1["exp"], float), "Expiration should be an integer."

        exp_time = datetime.utcfromtimestamp(decoded_token_test_case_1["exp"])
        assert exp_time > datetime.utcnow(), "Token should not be expired"
    except JWTError as e:
        print(f"test_create_access_token: {e}")
        pytest.fail("test_create_access_token: JWT Decoding failed")

def test_hash_password():
    """ Unit test for Hashing a Password """
    password_test_case_1 = "Test12345!"
    password_test_case_2 = "Admin1234!2!"
    password_test_case_3 = "Test12345!"
    hashed_password_test_case_1 = hash_password(password_test_case_1)
    hashed_password_test_case_2 = hash_password(password_test_case_2)
    hashed_password_test_case_3 = hash_password(password_test_case_3)

    assert hashed_password_test_case_1 != password_test_case_1
    assert isinstance(hashed_password_test_case_1, str), "Hashed password should be a string."
    assert len(hashed_password_test_case_1)>0, "Hashed password should not be an empty string."
    assert hashed_password_test_case_2 != password_test_case_2
    assert isinstance(hashed_password_test_case_2, str), "Hashed password should be a string."
    assert len(hashed_password_test_case_2) > 0, "Hashed password should not be an empty string."
    assert hashed_password_test_case_1 != hashed_password_test_case_2
    assert hashed_password_test_case_1 != hashed_password_test_case_3

def test_verify_password():
    """ Unit test for verifying password """
    password_test_case_1 = "Test12345!"
    password_test_case_2 = "Admin1234!2!"
    password_test_case_3 = "Test12345!"
    hashed_password_test_case_1 = hash_password(password_test_case_1)
    hashed_password_test_case_2 = hash_password(password_test_case_2)
    hashed_password_test_case_3 = hash_password(password_test_case_3)

    assert isinstance(verify_password(password_test_case_1, hashed_password_test_case_2), bool)
    assert verify_password(password_test_case_1, hashed_password_test_case_1) == True
    assert verify_password(password_test_case_2, hashed_password_test_case_2) == True
    assert verify_password(password_test_case_3, hashed_password_test_case_3) == True
    assert verify_password(password_test_case_1, hashed_password_test_case_2) == False
    assert verify_password(password_test_case_1, hashed_password_test_case_3) == True
    assert verify_password(password_test_case_2, hashed_password_test_case_3) == False
