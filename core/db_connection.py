from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.configs import settings

class Database:
    """
    Database class to connect to the database
    """
    def __init__(self):
        self.engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_postgresql_db(self):
        """
        Get PostgreSQL database
        :return:
        """
        db_postgres = self.SessionLocal()
        try:
            yield db_postgres
        finally:
            db_postgres.close()

database = Database()
