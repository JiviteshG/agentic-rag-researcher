# app/ingestion/index_weaviate.py
import os, uuid, time
from typing import List, Dict
from tqdm import tqdm
import weaviate
from weaviate.classes.config import Property, DataType
from weaviate.classes.init import Auth
from app.config import config
from app.ingestion.embeddings import get_openai_embeddings

def get_weaviate_client() -> weaviate.WeaviateClient:
    w_conf = config.weaviate
    # Double check the URL has https://
    url = w_conf.url if w_conf.url.startswith("http") else f"https://{w_conf.url}"
    return weaviate.connect_to_weaviate_cloud(
        cluster_url=url,
        auth_credentials=Auth.api_key(w_conf.api_key)
    )

def ensure_schema(client: weaviate.WeaviateClient) -> None:
    w_conf = config.weaviate
    if w_conf.class_name in client.collections.list_all():
        client.collections.delete(w_conf.class_name)
    
    # We only define 3 core properties to keep it as simple as possible
    client.collections.create(
        name=w_conf.class_name,
        vectorizer_config=None,
        properties=[
            Property(name="paper_id", data_type=DataType.TEXT),
            Property(name="title", data_type=DataType.TEXT),
            Property(name="chunk_text", data_type=DataType.TEXT),
        ],
    )

def index_chunks(client: weaviate.WeaviateClient, chunks: List[Dict]) -> None:
    w_conf = config.weaviate
    collection = client.collections.get(w_conf.class_name)
    
    # PROOF OF CONNECTION: Print version and hostname
    meta = client.get_meta()
    print(f"📡 Connected to: {meta.get('hostname')} (v{meta.get('version')})")

    for i in tqdm(range(0, len(chunks), 20)):
        batch = chunks[i : i + 20]
        vectors = get_openai_embeddings([c["chunk_text"] for c in batch])
        
        for chunk, vector in zip(batch, vectors):
            # We ONLY send the properties defined in ensure_schema
            collection.data.insert(
                properties={
                    "paper_id": str(chunk.get("paper_id", "N/A")),
                    "title": str(chunk.get("title", "Untitled")),
                    "chunk_text": str(chunk.get("chunk_text", "")),
                },
                vector=vector.tolist(),
                uuid=uuid.uuid4()
            )

    time.sleep(3)
    count = collection.aggregate.over_all(total_count=True).total_count
    print(f"\n✅ Final Server Count: {count}")