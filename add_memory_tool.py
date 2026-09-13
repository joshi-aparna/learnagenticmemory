from pathlib import Path
import json
from datetime import datetime
from ollama import embed

WORKSPACE = Path("urlshortener").resolve()
MEMORY_FILE = WORKSPACE / "memory.json"

EMBEDDING_MODEL = "embeddinggemma" 
def get_embedding(text: str) -> list[float]:
    response = embed( model=EMBEDDING_MODEL, input=text )
    return response["embeddings"][0]

def archival_memory_insert(memory: str) -> str:
    """
    Store information that may be useful in future sessions but does not need to be continuously visible in core memory.
    Use this for durable project knowledge such as:
    - architectural decisions
    - implementation decisions
    - important discoveries
    - completed milestones
    - unresolved issues
    - project progress

    Do not use it for transient conversation details.
    """

    if MEMORY_FILE.exists():
        memories = json.loads(MEMORY_FILE.read_text())
    else:
        memories = []

    next_id = max((m["id"] for m in memories), default=0) + 1

    new_memory = {
        "id": next_id,
        "memory": memory,
        "embedding": get_embedding(memory),
        "created": datetime.now().isoformat()
    }

    memories.append(new_memory)

    MEMORY_FILE.write_text(
        json.dumps(memories, indent=2)
    )

    return f"Memory {next_id} saved."