# app/ingestion/embeddings.py
"""
OpenAI embedding utilities with safety guards for empty inputs.
"""

import os
import time
from typing import List
import numpy as np
from openai import OpenAI, RateLimitError

def get_openai_embeddings(texts: List[str], model: str = "text-embedding-3-small") -> np.ndarray:
    """
    Get embeddings from OpenAI API with guards for empty strings and rate limits.
    """
    # 1. Guard against empty input list
    if not texts:
        return np.array([], dtype=np.float32)

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in the environment.")

    client = OpenAI(api_key=api_key, base_url=base_url)
    all_embeddings = []
    batch_size = 20 
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        
        # 2. Clean the batch: Replace empty strings with a single space " " 
        # OpenAI cannot embed a completely empty string "".
        safe_batch = [t if t.strip() else " " for t in batch]
        
        try:
            response = client.embeddings.create(
                input=safe_batch,
                model=model
            )
            
            # Extract and verify we actually got data back
            if not response.data:
                continue
                
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)
            
            time.sleep(0.5) # Gentle throttling
            
        except RateLimitError:
            print("Rate limit hit. Sleeping for 10s...")
            time.sleep(10)
            # Retry this batch by adjusting the loop index
            i -= batch_size 
            continue
        except Exception as e:
            print(f"Unexpected error during embedding: {e}")
            raise

    # 3. Final check before conversion to avoid the Axis 0 error
    if not all_embeddings:
        # Return an empty 2D array compatible with vector store shapes
        # Assuming model dimension is 1536 for text-embedding-3-small
        return np.empty((0, 1536), dtype=np.float32)

    return np.array(all_embeddings, dtype=np.float32)