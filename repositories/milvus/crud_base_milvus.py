from typing import Union, Optional, List, Dict, Any

from pymilvus import (
    AnnSearchRequest,
    connections,
    Collection,
    CollectionSchema,
    FieldSchema,
    Function,
    RRFRanker,
    utility,
    WeightedRanker,
)

class MilvusCRUD:
    def __init__(
        self,
        host: str = "localhost",
        port: str = "19530",
        username: Optional[str] = None,
        password: Optional[str] = None
    ):
        """
        Initialize a connection to the Milvus server.
        """
        connections.connect(
            "default",
            host=host,
            port=port,
            token=f"{username}:{password}" if username and password else None)
        print(
            f"Connected to Milvus at {host}:{port}"
        )

    def create_collection(
        self,
        collection_name: str,
        index_params: List[Dict[str, Any]] = None,
        fields: List[FieldSchema] = None,
        added_functions: Optional[List[Function]] = None
    ):
        """
        Create a collection with the specified name and dimension.

        :param added_functions:
        :param collection_name: Name of the collection.
        :param index_params: Index parameters for the collection.
        :param fields: List of field schemas.
        """
        if utility.has_collection(collection_name):
            print(f"Collection {collection_name} already exists.")
            return

        # Create a collection schema
        schema = CollectionSchema(fields, description=f"{collection_name} schema")

        if added_functions:
            for function in added_functions:
                schema.add_function(function)

        # Create a collection
        collection = Collection(name=collection_name, schema=schema, consistency_level="Strong")  # type: ignore

        # Create an index, if specified
        if index_params:
            for index_param in index_params:
                collection.create_index(
                    field_name=index_param.get("field_name", ""),
                    index_params=index_param.get("index_params", {})
                )

        print(f"Collection {collection_name} created successfully.")

    def delete_collection(self, collection_name: str):
        """
        Delete a collection from Milvus.

        :param collection_name: Name of the collection.
        """
        if not utility.has_collection(collection_name):
            print(f"Collection {collection_name} does not exist.")
            return
        utility.drop_collection(collection_name)
        print(f"Collection {collection_name} dropped.")

    def insert_vectors_batched(
        self,
        collection_name: str,
        vectors: List[List[float]],
        batch_size: int = 1000
    ) -> List[int]:
        """
        Insert vectors into the specified collection.

        :param collection_name: Name of the collection.
        :param vectors: List of vectors to add.
        :param batch_size: Number of records to insert per batch.
        :return: List of inserted primary IDs.
        """
        collection = Collection(collection_name)
        ids = []

        # Batch insert vectors (if needed)
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            result = collection.insert([None, batch])  # None for auto-generated IDs
            ids.extend(result.primary_keys)
            print(f"Inserted batch {len(batch)} vectors.")

        return ids

    def search_vectors_knn(
        self,
        collection_name: str,
        query_vectors: List[List[float]],
        top_k: int = 10,
        search_params: Dict[str, Any] = None
    ):
        """
        Search for the closest vectors (kNN search) to the given query vectors.

        :param collection_name: Name of the collection.
        :param query_vectors: List of query vectors.
        :param top_k: Number of nearest neighbors to retrieve.
        :param search_params: Additional search parameters.
        :return: Search results.
        """
        collection = Collection(collection_name)
        collection.load()  # Ensure the collection is loaded into memory

        # Default search parameters
        if not search_params:
            search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

        results = collection.search(
            data=query_vectors,
            anns_field="vector",
            param=search_params,
            limit=top_k
        )

        return results

    def search_vectors_hybrid(
        self,
        collection_name: str,
        search_requests: List[AnnSearchRequest],
        ranker: Union[RRFRanker, WeightedRanker],
        results_limit: int = 3,
    ):
        """
        Search for the closest vectors using a hybrid search.
        :param collection_name:
        :param search_requests:
        :param ranker:
        :param results_limit:
        :return:
        """
        collection = Collection(collection_name)
        collection.load()  # Ensure the collection is loaded into memory

        results = collection.hybrid_search(
            reqs=search_requests,
            rerank=ranker,
            limit=results_limit,
        )

        return results

    def delete_by_id(self, collection_name: str, ids: List[int]):
        """
        Delete vectors from a collection using their primary IDs.

        :param collection_name: Name of the collection.
        :param ids: List of primary IDs to delete.
        """
        collection = Collection(collection_name)
        collection.delete(expr=f"id in {ids}")
        print(f"Deleted vectors with IDs: {ids}")

    def drop_collection(self, collection_name: str):
        """
        Drop (delete) a collection from Milvus.

        :param collection_name: Name of the collection.
        """
        if not utility.has_collection(collection_name):
            print(f"Collection {collection_name} does not exist.")
            return
        utility.drop_collection(collection_name)
        print(f"Collection {collection_name} dropped.")

    def list_collections(self) -> List[str]:
        """
        List all collections in Milvus.
        """
        return utility.list_collections()
