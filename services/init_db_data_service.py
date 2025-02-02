from sqlalchemy.orm import Session

from constants import general as general_constants
from constants.core import security as security_constants
from constants.services import init_db_data as init_db_data_constants
from core.db_connection import database
from core.configs import settings
from core.security import hash_password
from repositories import (
    crud_tbl_document_type,
    crud_tbl_permissions,
    crud_tbl_roles,
    crud_tbl_rolepermissions,
    crud_tbl_users,
    crud_tbl_userroles,
)
from schemas import (
    DocumentTypeSchema,
    RolesSchema,
    RolePermissionsSchema,
    PermissionsSchema,
    UserRoleSchema,
    UsersSchema,
)

class Initialize_Data:
    """
    Initialize Data class to insert data into the database
    for the first time
    """
    def __init__(self, db: Session):
        """
        Initialize the class
        Args:
            db: (Session) SQLAlchemy session
        """
        self.db = db

    def insert_document_types(self):
        """
        Insert document types into the database
        """
        document_types_list = [
            DocumentTypeSchema(
                document_type=general_constants.IN_PRES,
                document_extention=init_db_data_constants.DOCUMENT_EXTENTION_PDF
            ),
            DocumentTypeSchema(
                document_type=general_constants.KEP_PRES,
                document_extention=init_db_data_constants.DOCUMENT_EXTENTION_PDF
            ),
            DocumentTypeSchema(
                document_type=general_constants.PBL,
                document_extention=init_db_data_constants.DOCUMENT_EXTENTION_PDF
            ),
            DocumentTypeSchema(
                document_type=general_constants.PEN_PRES,
                document_extention=init_db_data_constants.DOCUMENT_EXTENTION_PDF
            ),
            DocumentTypeSchema(
                document_type=general_constants.PER_DA,
                document_extention=init_db_data_constants.DOCUMENT_EXTENTION_PDF
            ),
            DocumentTypeSchema(
                document_type=general_constants.PER_MEN,
                document_extention=init_db_data_constants.DOCUMENT_EXTENTION_PDF
            ),
            DocumentTypeSchema(
                document_type=general_constants.PER_PRES,
                document_extention=init_db_data_constants.DOCUMENT_EXTENTION_PDF
            ),
            DocumentTypeSchema(
                document_type=general_constants.PPPUU,
                document_extention=init_db_data_constants.DOCUMENT_EXTENTION_PDF
            ),
            DocumentTypeSchema(
                document_type=general_constants.PP,
                document_extention=init_db_data_constants.DOCUMENT_EXTENTION_PDF
            ),
            DocumentTypeSchema(
                document_type=general_constants.TAP_MPR,
                document_extention=init_db_data_constants.DOCUMENT_EXTENTION_PDF
            ),
            DocumentTypeSchema(
                document_type=general_constants.UU,
                document_extention=init_db_data_constants.DOCUMENT_EXTENTION_PDF
            ),
            DocumentTypeSchema(
                document_type=general_constants.UU_DARURAT,
                document_extention=init_db_data_constants.DOCUMENT_EXTENTION_PDF
            ),
        ]
        existing_document_types = crud_tbl_document_type.get_all(self.db)
        existing_document_types_only = [doctype.document_type for doctype in existing_document_types]

        counter = 0
        for document_type in document_types_list:
            if document_type.document_type not in existing_document_types_only:
                crud_tbl_document_type.insert(self.db, document_type)
                counter += 1

        print(f"insert_document_types: {counter} new Document types inserted.")

    def insert_data(self):
        """
        Insert data into the database
        """
        self.insert_document_types()
        self.insert_roles()
        self.insert_permissions()
        self.insert_initial_role_permissions_map()
        self.insert_users()
        self.insert_user_role_mapping()
        print("All initial data have been inserted.")

    def insert_initial_role_permissions_map(self):
        """
        Insert initial role permissions map into the database
        """
        superadmin_role = crud_tbl_roles.get_by_role_name(self.db, init_db_data_constants.ROLE_SUPERADMIN)
        if superadmin_role:
            all_permissions = crud_tbl_permissions.get_all(self.db)
            all_permission_ids = [all_permission.id for all_permission in all_permissions]
            existing_mappings = crud_tbl_rolepermissions.get_by_role_id(self.db, superadmin_role.id)
            existing_permission_ids = [existing_mapping.permission_id for existing_mapping in existing_mappings]
            not_yet_added_permission_ids = [not_yet_added_permission for not_yet_added_permission in
                                            all_permission_ids if not_yet_added_permission not
                                            in existing_permission_ids]
            bulk_insert_schema = [
                RolePermissionsSchema(
                    role_id=superadmin_role.id,
                    permission_id=inserted_permission_id,
                )
                for inserted_permission_id in not_yet_added_permission_ids
            ]
            print(f"insert_initial_role_permissions_map: Inserting {len(bulk_insert_schema)} new mapping...")
            crud_tbl_rolepermissions.bulk_insert(self.db, bulk_insert_schema)
            print("insert_initial_role_permissions_map: Superadmin role permissions map inserted.")
        else:
            print("insert_initial_role_permissions_map: Superadmin role not found.")

    def insert_permissions(self):
        """
        Insert permissions into the database
        :return:
        """
        permissions = [
            PermissionsSchema(
                permission_name=security_constants.PERMISSION_READ_ME,
                permission_description=security_constants.PERMISSION_READ_ME_DESC,
            ),
            PermissionsSchema(
                permission_name=security_constants.PERMISSION_WRITE_ME,
                permission_description=security_constants.PERMISSION_WRITE_ME_DESC,
            ),
            PermissionsSchema(
                permission_name=security_constants.PERMISSION_UPDATE_ME,
                permission_description=security_constants.PERMISSION_UPDATE_ME_DESC,
            ),
            PermissionsSchema(
                permission_name=security_constants.PERMISSION_DELETE_ME,
                permission_description=security_constants.PERMISSION_DELETE_ME_DESC,
            ),
            PermissionsSchema(
                permission_name=security_constants.PERMISSION_READ_DOC_TYPES,
                permission_description=security_constants.PERMISSION_READ_DOC_TYPES_DESC,
            ),
            PermissionsSchema(
                permission_name=security_constants.PERMISSION_WRITE_DOC_TYPES,
                permission_description=security_constants.PERMISSION_WRITE_DOC_TYPES_DESC,
            ),
            PermissionsSchema(
                permission_name=security_constants.PERMISSION_UPDATE_DOC_TYPES,
                permission_description=security_constants.PERMISSION_UPDATE_DOC_TYPES_DESC,
            ),
            PermissionsSchema(
                permission_name=security_constants.PERMISSION_DELETE_DOC_TYPES,
                permission_description=security_constants.PERMISSION_DELETE_DOC_TYPES_DESC,
            ),
            PermissionsSchema(
                permission_name=security_constants.PERMISSION_READ_ALL_ROLES,
                permission_description=security_constants.PERMISSION_READ_ALL_ROLES_DESC,
            ),
            PermissionsSchema(
                permission_name=security_constants.PERMISSION_READ_ROLES_ME,
                permission_description=security_constants.PERMISSION_READ_ROLES_ME_DESC,
            ),
            PermissionsSchema(
                permission_name=security_constants.PERMISSION_READ_ROLES_USER,
                permission_description=security_constants.PERMISSION_READ_ROLES_USER_DESC,
            ),
            PermissionsSchema(
                permission_name=security_constants.PERMISSION_WRITE_ROLES,
                permission_description=security_constants.PERMISSION_WRITE_ROLES_DESC,
            ),
            PermissionsSchema(
                permission_name=security_constants.PERMISSION_UPDATE_ROLES,
                permission_description=security_constants.PERMISSION_UPDATE_ROLES_DESC,
            ),
            PermissionsSchema(
                permission_name=security_constants.PERMISSION_DELETE_ROLES,
                permission_description=security_constants.PERMISSION_DELETE_ROLES_DESC,
            ),
        ]
        existing_permissions = crud_tbl_permissions.get_all(self.db)
        existing_permission_names = [
            existing_permission.permission_name for existing_permission in existing_permissions
        ]
        not_yet_added_permissions = [permission for permission in permissions
                                     if permission.permission_name not in existing_permission_names]
        if len(not_yet_added_permissions) > 0:
            crud_tbl_permissions.bulk_insert(self.db, not_yet_added_permissions)
            print(f"insert_permissions: {len(not_yet_added_permissions)} new permissions inserted.")

    def insert_roles(self):
        """
        Insert roles into the database
        """
        superadmin_role_schema = RolesSchema(
            role_name=init_db_data_constants.ROLE_SUPERADMIN,
        )
        existing_superadmin_role = crud_tbl_roles.get_by_role_name(self.db, superadmin_role_schema.role_name)
        if not existing_superadmin_role:
            crud_tbl_roles.insert(self.db, superadmin_role_schema)

        print("insert_roles: Roles inserted.")

    def insert_users(self):
        """
        Insert users into the database
        """
        # create a superadmin account
        superadmin_schema = UsersSchema(
            full_name=settings.FIRST_SUPERADMIN_NAME,
            email=settings.FIRST_SUPERADMIN_EMAIL,
            hashed_password=hash_password(
                settings.FIRST_SUPERADMIN_PASSWORD
            ),
            is_active=True
        )
        exist_super_user = crud_tbl_users.get_by_email(self.db, superadmin_schema.email)
        if not exist_super_user:
            crud_tbl_users.insert(self.db, superadmin_schema)

        print("insert_users: Superadmin account created.")

    def insert_user_role_mapping(self):
        """
        Insert initial user-role mappings
        """
        superadmin_user = crud_tbl_users.get_by_email(self.db, settings.FIRST_SUPERADMIN_EMAIL)
        superadmin_role = crud_tbl_roles.get_by_role_name(self.db, init_db_data_constants.ROLE_SUPERADMIN)
        if superadmin_user and superadmin_role:
            existing_mappings = crud_tbl_userroles.get_by_user_id_and_role_id(
                self.db,
                superadmin_user.id,
                superadmin_role.id
            )
            if not existing_mappings:
                crud_tbl_userroles.insert(
                    self.db,
                    UserRoleSchema(
                        user_id=superadmin_user.id,
                        role_id=superadmin_role.id,
                    )
                )
                print("Super Admin has been assigned with its respective role.")

initialize_data = Initialize_Data(database.SessionLocal())

if __name__ == "__main__":
    initialize_data.insert_data()
