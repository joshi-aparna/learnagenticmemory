from pathlib import Path
import json
from datetime import datetime

def update_memory(memory_id: int, memory: str) -> str:
    """
    Update an existing long-term memory by its ID.
    """
    WORKSPACE = Path("urlshortener").resolve()
    MEMORY_FILE = WORKSPACE / "memory.json"

    if not MEMORY_FILE.exists():
        return "No memories stored."

    memories = json.loads(MEMORY_FILE.read_text())

    for item in memories:
        if item["id"] == memory_id:
            item["memory"] = memory
            item["updated"] = datetime.now().isoformat()

            MEMORY_FILE.write_text(
                json.dumps(memories, indent=2)
            )

            return f"Memory {memory_id} updated."

    return f"Memory {memory_id} not found."