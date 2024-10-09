from elasticsearch import Elasticsearch
from datetime import datetime
from typing import Any, Dict, Optional
from app.exceptions.custom_exceptions import CustomValidationException

class ElasticsearchCRUD:
    def __init__(self, index_name: str):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
        self.index_name = index_name

        # Ensure index exists
        self.create_index()

    # Check if the index exists, if not create it
    def create_index(self):
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name)
            print(f"Index '{self.index_name}' created.")
        else:
            print(f"Index '{self.index_name}' already exists.")

    # Index a document
    def create(self, id: int, doc: Dict[str, Any]):
        try:
            self.es.index(index=self.index_name, id=id, body=doc)
        except Exception as e:
            raise CustomValidationException(status_code=400, detail=str(e))
        
    def get_all(self) -> list[Dict[str, Any]]:
        try:
            res = self.es.search(index=self.index_name, body={"query": {"match_all": {}}})
            return [hit['_source'] for hit in res['hits']['hits']]
        except Exception as e:
            raise CustomValidationException(status_code=400, detail=str(e))

    # Retrieve a document by ID
    def get(self, id: int) -> Optional[Dict[str, Any]]:
        try:
            res = self.es.get(index=self.index_name, id=id)
            return res['_source']
        except Exception:
            raise CustomValidationException(status_code=404, detail=f"Document with id {id} not found in {self.index_name}")

    # Update a document by ID
    def update(self, id: int, doc: Dict[str, Any]):
        try:
            self.es.update(index=self.index_name, id=id, body={"doc": doc})
        except Exception as e:
            raise CustomValidationException(status_code=400, detail=str(e))

    # Delete a document by ID
    def delete(self, id: int):
        try:
            self.es.delete(index=self.index_name, id=id)
        except Exception:
            raise CustomValidationException(status_code=404, detail=f"Document with id {id} not found in {self.index_name}")
