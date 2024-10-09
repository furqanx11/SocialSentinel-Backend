from elasticsearch import Elasticsearch
from datetime import datetime
from app.schemas.detection_schema import FlaggedPost, FlaggedComment, FlaggedMessage

es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])

# Check connection
if not es.ping():
    raise ValueError("Connection to Elasticsearch failed")
