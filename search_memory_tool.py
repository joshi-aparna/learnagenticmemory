from pathlib import Path
import json
import numpy as np
from add_memory_tool import get_embedding

def cosine_similarity(a: list[float], b: list[float]) -> float:
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def archival_memory_search(query: str) -> str:
    """
    Search archival memory for information relevant to the query.
    """
    WORKSPACE = Path("urlshortener").resolve()
    MEMORY_FILE = WORKSPACE / "memory.json"
    if not MEMORY_FILE.exists():
        return "No memories stored."
    print("searching memory for:" + query)
    memories = json.loads(MEMORY_FILE.read_text())

    query_embedding = get_embedding(query.lower()) 
    scored_memories = [] 
    for memory in memories: 
        score = cosine_similarity( query_embedding, memory["embedding"] ) 
        scored_memories.append( (score, memory) ) 
        scored_memories.sort( key=lambda x: x[0], reverse=True ) 
    results = [] 
    for score, memory in scored_memories[:3]: 
        results.append({ "id": memory["id"], "memory": memory["memory"], "similarity": round(float(score), 3) })
    answer = json.dumps(results, indent=2)
    print(answer)
    return answer