from pathlib import Path
import json

def search_memory(query: str) -> str:
    """
    Search long-term memory for information relevant
    to the supplied query.
    """
    WORKSPACE = Path("urlshortener").resolve()
    MEMORY_FILE = WORKSPACE / "memory.json"
    if not MEMORY_FILE.exists():
        return "No memories stored."
    print("searching memory for:" + query)
    memories = json.loads(MEMORY_FILE.read_text())

    query_words = query.lower().split()

    matches = []

    for memory in memories:
        text = memory["memory"].lower()

        if any(word in text for word in query_words):
            matches.append(memory)

    if not matches:
        print("no relevant memories found")
        return "No relevant memories found."

    answer = json.dumps(matches, indent=2)
    print(answer)
    return answer