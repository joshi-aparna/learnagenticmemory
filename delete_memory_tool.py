from pathlib import Path
import json
from datetime import datetime

WORKSPACE = Path("urlshortener").resolve()
MEMORY_FILE = WORKSPACE / "memory.json"
def delete_memory(memory_id: int) -> str:
    """
    Delete an existing long-term memory by its ID.
    """

    if not MEMORY_FILE.exists():
        return "No memories stored."

    memories = json.loads(MEMORY_FILE.read_text())

    remaining = [
        m for m in memories
        if m["id"] != memory_id
    ]

    if len(remaining) == len(memories):
        return f"Memory {memory_id} not found."

    MEMORY_FILE.write_text(
        json.dumps(remaining, indent=2)
    )

    return f"Memory {memory_id} deleted."