from pymilvus import MilvusClient

from core.configs import settings

class VectorDBConnection():
    """
    A class to represent a connection to a vector database.
    """
    def __init__(self, vector_db_engine: str):
        self.vector_db_engine = vector_db_engine

    def milvus_connect(
        self,
        collection_name: str,
    )->MilvusClient:
        """Connect to Milvus"""
        client = MilvusClient(
            uri=f"{settings.VECTOR_DB_HOST}:{settings.VECTOR_DB_PORT}",
            token=f"{settings.VECTOR_DB_USERNAME}:{settings.VECTOR_DB_PASSWORD}",
        )
        return client

vector_db = VectorDBConnection(vector_db_engine=settings.VECTOR_DB_ENGINE)
