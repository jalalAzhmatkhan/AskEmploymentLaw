import logging
from uuid import uuid4

from sqlalchemy.sql import text
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from core.configs import settings
from core.db_connection import database
from core.logger import logger

@retry(
    stop=stop_after_attempt(settings.DATABASE_CONNECTION_MAX_TRIES),
    wait=wait_fixed(settings.DATABASE_CONNECTION_WAIT_SEC),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init_db_connection() -> None:
    """
    Function to check Database Connection
    :return: boolean whether the connection is successful or not
    """

    try:
        db = database.SessionLocal()
        test_sql = "SELECT 1"
        db.execute(text(test_sql))
        logger.info("init_db_connection: Connected to the DB successfully.")
        print("init_db_connection: Connected to the DB successfully.")
    except Exception as e:
        req_id = str(uuid4()).replace("-", "")
        logger.error(f"init_db_connection: {req_id} Error: {e}")
        raise e

if __name__ == '__main__':
    logger.info("init_db_connection: Initializing DB connection.")
    print("init_db_connection: Initializing DB connection.")
    init_db_connection()
