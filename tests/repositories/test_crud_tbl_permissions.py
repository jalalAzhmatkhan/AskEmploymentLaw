from core.db_connection import database
from repositories import crud_tbl_permissions
from schemas import PermissionsSchema, PermissionsUpdateSchema

def test_crud_tbl_permissions():
    """Unit test for CRUD Tbl_Permissions"""
    db = database.SessionLocal()

    # Insertion Test
    test_case_permission_1 = "Test Permission 1"
    test_case_permission_desc_1 = "Test Description 1"
    inserted_data = PermissionsSchema(
        permission_name=test_case_permission_1,
        permission_description=test_case_permission_desc_1
    )
    created_permission = crud_tbl_permissions.create(db=db, obj_in=inserted_data)

    assert created_permission is not None, "Test case 1: Data not created."
    assert isinstance(created_permission.id, int), "Test case 1: Permission ID is not an integer."
    assert isinstance(created_permission.permission_name, str), "Test case 1: Permission name is not a string."
    assert isinstance(created_permission.permission_description, str), "Test case 1: Permission description is not a string."
    assert created_permission.permission_name == test_case_permission_1, "Test case 1: Permission name mismatch."
    assert created_permission.permission_description == test_case_permission_desc_1, "Test case 1: Permission description mismatch."

    # Get by Name
    get_by_permission_name = crud_tbl_permissions.get_by_name(db=db, name=test_case_permission_1)
    assert get_by_permission_name is not None, "Test case 2: Permission not found."
    assert isinstance(get_by_permission_name.id, int), "Test case 2: Permission ID is not an integer."
    assert isinstance(get_by_permission_name.permission_name, str), "Test case 2: Permission name is not a string."
    assert isinstance(get_by_permission_name.permission_description, str), "Test case 2: Permission description is not a string."
    assert get_by_permission_name.permission_name == test_case_permission_1, "Test case 2: Permission name mismatch."

    # Update test
    updated_permission_name = "Test Permission 2"
    test_update_permission = PermissionsUpdateSchema(
        permission_name=updated_permission_name
    )
    updated_permission = crud_tbl_permissions.update(db=db, db_obj=created_permission, obj_in=test_update_permission)
    assert updated_permission is not None, "Test case 3: Permission not updated."
    assert updated_permission.permission_name == updated_permission_name, "Test case 3: Permission name mismatch."
    assert updated_permission.permission_description == test_case_permission_desc_1, "Test case 3: Permission description mismatch."

    # Get by Like Name
    like_name = "Test Permission"
    found_permissions = crud_tbl_permissions.get_by_like_name(db=db, name=like_name)
    assert isinstance(found_permissions, list), "Test case 4: Permission list not returned."
    assert len(found_permissions) > 0, "Test case 4: Permission list is empty."
    assert like_name in found_permissions[0].permission_name, "Test case 4: Permission name mismatch."

    # Get all name to Dict
    name_to_dict_list = crud_tbl_permissions.get_all_name_to_dict(db=db)
    assert isinstance(name_to_dict_list, dict), "Test case 5: Permission list not returned."
    assert len(name_to_dict_list) > 0, "Test case 5: Permission list is empty."

    # Delete
    crud_tbl_permissions.delete_by_id(db=db, id=created_permission.id)
