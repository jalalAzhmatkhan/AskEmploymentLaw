from core.db_connection import database
from core.security import hash_password, verify_password
from repositories import crud_tbl_users
from schemas import UsersSchema
from tests.faker import faker

def test_get_by_email():
    """Unit test to Get User by Email"""
    db = database.SessionLocal()

    test_fullname = "test_username"
    test_email = faker.email()
    test_password = "test_password"
    test_new_user = UsersSchema(
        full_name=test_fullname,
        email=test_email,
        hashed_password=hash_password(test_password)
    )
    crud_tbl_users.create(db=db, obj_in=test_new_user)

    # get user
    found_user = crud_tbl_users.get_by_email(db=db, email=test_email)
    assert found_user is not None
    assert found_user.email == test_email
    assert found_user.full_name == test_fullname
    assert verify_password(test_password, found_user.hashed_password)

    # clean up
    crud_tbl_users.delete_by_id(db=db, id=found_user.id)
