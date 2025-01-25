from sqlalchemy.orm import Session

from constants import general as general_constants
from constants.services import init_db_data as init_db_data_constants
from core.db_connection import database
from core.configs import settings
from core.utilities import hash_password
from repositories import crud_tbl_document_type, crud_tbl_roles, crud_tbl_users
from schemas import DocumentTypeSchema, RolesSchema, UsersSchema

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
        document_types = [
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

        for document_type in document_types:
            if not crud_tbl_document_type.get_by_type(self.db, document_type["document_type"]):
                crud_tbl_document_type.insert(self.db, document_type)

        print("insert_document_types: Document types inserted.")

    def insert_data(self):
        """
        Insert data into the database
        """
        self.insert_document_types()
        self.insert_roles()
        self.insert_roles()

    def insert_roles(self):
        """
        Insert roles into the database
        """
        superadmin_role_schema = RolesSchema(
            role_name=init_db_data_constants.ROLE_SUPERADMIN,
        )
        existing_superadmin_role = crud_tbl_roles.get_by_role_name(self.db, superadmin_role_schema["role_name"])
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
        exist_super_user = crud_tbl_users.get_by_email(self.db, superadmin_schema["email"])
        if not exist_super_user:
            exist_super_user = crud_tbl_users.insert(self.db, superadmin_schema)

        print("insert_users: Superadmin account created.")



initialize_data = Initialize_Data(database)
