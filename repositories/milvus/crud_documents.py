from typing import List, Optional

from pymilvus import (
    Collection,
    DataType,
    FieldSchema,
    Function,
    FunctionType
)

from core.configs import settings
from repositories.milvus.crud_base_milvus import MilvusCRUD
from schemas import MilvusDocumentsSchema

class CRUDDocuments(MilvusCRUD):
    """
    CRUD for Documents collection on Milvus
    """
    def __init__(
        self,
        host: str,
        port: str,
        username: str,
        password: str,
        delete_insert_collection: bool = False
    ):
        super().__init__(host, port, username, password)
        self.collection_name = "documents"
        analyzer_params = {
            "tokenizer": "standard",
        }
        document_fields = [
            FieldSchema(
                name="id",
                dtype=DataType.INT64,
                is_primary=True,
                auto_id=True
            ),
            FieldSchema(
                name="uploaded_document_id",
                dtype=DataType.INT32,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=60535,
                enable_analyzer=True,
                analyzer_params=analyzer_params,
            ),
            FieldSchema(
                name="dense_embedding",
                dtype=DataType.FLOAT_VECTOR,
                dim=1024
            ),
            FieldSchema(
                name="sparse_embedding",
                dtype=DataType.SPARSE_FLOAT_VECTOR,
            )
        ]
        text_to_bm_25 = Function(
            name="text_to_bm25",
            input_field_names="text",
            output_field_names="sparse_embedding",
            function_type=FunctionType.BM25
        )
        index_parameters = [
            {
                "field_name": "dense_embedding",
                "index_params": {
                    "index_type": "IVF_SQ8",
                    "metric_type": "COSINE",
                }
            },
            {
                "field_name": "sparse_embedding",
                "index_params": {
                    "index_type": "SPARSE_INVERTED_INDEX",
                    "metric_type": "BM25",
                }
            }
        ]
        if delete_insert_collection:
            self.delete_collection(self.collection_name)
        self.create_collection(
            collection_name=self.collection_name,
            fields=document_fields,
            index_params=index_parameters,
            added_functions=[text_to_bm_25],
        )

    def insert_vector(
        self,
        inserted_document: MilvusDocumentsSchema
    )->Optional[int]:
        """
        Function to insert a document into the collection
        :param inserted_document:
        :return:
        """
        collection = Collection(self.collection_name)
        result = collection.insert([
            inserted_document.uploaded_document_id,
            inserted_document.text,
            inserted_document.dense_embedding,
            inserted_document.sparse_embedding
        ])
        return result.primary_keys[0] if len(result.primary_keys) > 0 else None

    def bulk_insert_vector(
        self,
        inserted_documents: List[MilvusDocumentsSchema]
    )->List[int]:
        """
        Function to insert multiple documents into the collection
        :param inserted_documents:
        :return:
        """
        collection = Collection(self.collection_name)
        results = collection.insert(
            data=[doc.model_dump(mode='json') for doc in inserted_documents]
        )
        return results.primary_keys


crud_documents_milvus = CRUDDocuments(
    host=settings.VECTOR_DB_HOST,
    port=settings.VECTOR_DB_PORT,
    username=settings.VECTOR_DB_USERNAME,
    password=settings.VECTOR_DB_PASSWORD,
    delete_insert_collection=False,
)
