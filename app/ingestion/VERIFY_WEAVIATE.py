import weaviate
import os
from dotenv import load_dotenv

load_dotenv()

# Ensure the URL has https://
url = os.getenv("WEAVIATE_URL")
if not url.startswith("https://"):
    url = f"https://{url}"

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=url,
    auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WEAVIATE_API_KEY"))
)

try:
    # This meta call proves we are connected to the specific Cloud instance
    meta = client.get_meta()
    print(f"✅ Connected to Weaviate version: {meta['version']}")
    
    # Check if PaperChunk exists
    if client.collections.exists("PaperChunk"):
        col = client.collections.get("PaperChunk")
        print(f"📊 Collection 'PaperChunk' found. Count: {col.aggregate.over_all(total_count=True).total_count}")
    else:
        print("❌ Collection not found on this endpoint.")
finally:
    client.close()