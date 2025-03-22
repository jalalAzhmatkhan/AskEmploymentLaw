from core.db_connection import database
from models import TblPermissions
from repositories import CRUDBase
from schemas import PermissionsSchema, PermissionsUpdateSchema

def test_crud_base():
    """
    Unit test CRUD Base
    :return:
    """
    crud_tbl_permission = CRUDBase[TblPermissions, PermissionsSchema, PermissionsUpdateSchema](TblPermissions)
    test_create_permission_name = "Test Permission 1"
    test_create_permission_desc = "Test Permission Description"
    test_case_create = PermissionsSchema(
        permission_name=test_create_permission_name,
        permission_description=test_create_permission_desc
    )
    db = database.SessionLocal()

    created_permission = crud_tbl_permission.create(db=db, obj_in=test_case_create)
    assert created_permission is not None, "Test case 1: Data not created."
    assert created_permission.id is not None, "Test case 1: Permission ID is not created."
    assert isinstance(created_permission.id, int), "Test case 1: Permission ID is not an integer."
    assert isinstance(created_permission.permission_name, str), "Test case 1: Permission name is not a string."
    assert isinstance(created_permission.permission_description, str), "Test case 1: Permission description is not a string."

    get_created_permission = crud_tbl_permission.get_by_id(db=db, id=created_permission.id)
    assert get_created_permission is not None, "Test case 2: Permission not found."
    assert get_created_permission.id == created_permission.id, "Test case 2: Permission ID mismatch."
    assert get_created_permission.permission_name == test_create_permission_name, "Test case 2: Permission name mismatch."
    assert get_created_permission.permission_description == test_create_permission_desc, "Test case 2: Permission description mismatch."

    update_permission_name = "Test Permission 2"
    update_permission_data = PermissionsUpdateSchema(
        permission_name = update_permission_name
    )
    updated_permission = crud_tbl_permission.update(
        db=db,
        db_obj=get_created_permission,
        obj_in=update_permission_data
    )
    assert updated_permission is not None, "Test case 3: Permission not updated."
    assert updated_permission.id == created_permission.id, "Test case 3: Permission ID mismatch."
    assert updated_permission.permission_name == update_permission_name, "Test case 3: Permission name mismatch."
    assert updated_permission.permission_description == test_create_permission_desc, "Test case 3: Permission description mismatch."

    crud_tbl_permission.delete_by_id(db=db, id=created_permission.id)
