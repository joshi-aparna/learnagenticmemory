from pathlib import Path

agent_workspace_path = "urlshortener"
file_path = f"{agent_workspace_path}/core_memory.txt"
CORE_MEMORY_FILE = Path(file_path)


def load_core_memory() -> list[str]:
    """Load the current core memory from disk."""

    if not CORE_MEMORY_FILE.exists():
        return []

    return CORE_MEMORY_FILE.read_text().splitlines()


def save_core_memory(core_memory: list[str]) -> None:
    """Save the complete core memory to disk."""

    CORE_MEMORY_FILE.write_text(
        "\n".join(core_memory)
    )


def core_memory_append(text: str) -> str:
    """Append information to the existing core memory."""

    core_memory = load_core_memory()

    core_memory.append(text)

    save_core_memory(core_memory)

    return "Core memory updated."


def core_memory_replace(
    old_text: str,
    new_text: str
) -> str:
    """Replace existing information in core memory."""

    core_memory = load_core_memory()

    if old_text not in core_memory:
        return f"ERROR: '{old_text}' not found in core memory."

    index = core_memory.index(old_text)
    core_memory[index] = new_text

    save_core_memory(core_memory)

    return "Core memory updated."