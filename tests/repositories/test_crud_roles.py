from core.db_connection import database
from models import TblRoles
from repositories import crud_tbl_roles
from schemas import RolesSchema

def test_crud_roles():
    """Unit test for Tbl_Roles"""
    db = database.SessionLocal()

    # Test insert
    inserted_role_name = "Test Role 1"
    inserted_data = RolesSchema(role_name=inserted_role_name)
    created_role = crud_tbl_roles.create(db=db, obj_in=inserted_data)
    assert created_role is not None, "Test case 1: Data not created."
    assert created_role.id is not None, "Test case 1: Role ID is not created."
    assert isinstance(created_role.id, int), "Test case 1: Role ID is not an integer."
    assert isinstance(created_role.role_name, str), "Test case 1: Role name is not a string."

    # Get by Id
    get_created_role = crud_tbl_roles.get_by_id(db=db, id=created_role.id)
    assert get_created_role is not None, "Test case 2: Role not found."
    assert get_created_role.id == created_role.id, "Test case 2: Role ID mismatch."
    assert get_created_role.role_name == inserted_role_name, "Test case 2: Role name mismatch."
    assert isinstance(get_created_role.role_name, str), "Test case 2: Role name is not a string."

    # Get by Role Name
    get_by_role_name = crud_tbl_roles.get_by_role_name(db=db, role_name=inserted_role_name)
    assert get_by_role_name is not None, "Test case 3: Role not found."
    assert isinstance(get_by_role_name.role_name, str), "Test case 3: Role name is not a string."
    assert get_by_role_name.role_name == inserted_role_name, "Test case 3: Role name mismatch."

    # Get by Like Role Name
    like_name = "Test Role"
    get_by_like_role_name = crud_tbl_roles.get_by_like_role_name(db=db, role_name=like_name)
    assert isinstance(get_by_like_role_name, list), "Test case 4: Role not found."
    assert len(get_by_like_role_name) > 0, "Test case 4: Role not found."
    assert like_name in get_by_like_role_name[0].role_name, "Test case 4: Role name mismatch."

    # Bulk insert
    inserted_role_names = ["Test Role 2", "Test Role 3", "Test Role 4", "Test Role 5"]
    inserted_bulk_role_schema = [RolesSchema(role_name=name) for name in inserted_role_names]
    bulk_inserted_data = crud_tbl_roles.bulk_insert(db=db, obj_in=inserted_bulk_role_schema)
    bulk_inserted_names = [role.role_name for role in bulk_inserted_data]
    assert isinstance(bulk_inserted_data, list), "Test case 5: Bulk inserted data is not a list."
    assert "Test Role 2" in bulk_inserted_names, "Test case 5: Bulk inserted role name mismatch."
    assert "Test Role 3" in bulk_inserted_names, "Test case 5: Bulk inserted role name mismatch."

    # Delete by ID
    crud_tbl_roles.delete_by_id(db=db, id=created_role.id)
