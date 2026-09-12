from pathlib import Path
import json
from datetime import datetime
WORKSPACE = Path("urlshortener").resolve()
MEMORY_FILE = WORKSPACE / "memory.json"


def add_memory(memory: str) -> str:
    """
    Save a useful piece of information for future conversations.
    """

    if MEMORY_FILE.exists():
        memories = json.loads(MEMORY_FILE.read_text())
    else:
        memories = []

    next_id = max((m["id"] for m in memories), default=0) + 1

    new_memory = {
        "id": next_id,
        "memory": memory,
        "created": datetime.now().isoformat()
    }

    memories.append(new_memory)

    MEMORY_FILE.write_text(
        json.dumps(memories, indent=2)
    )

    return f"Memory {next_id} saved."