def read_file(filename: str) -> str:
    agent_workspace_path = "workspace"
    print(f"reading file: {filename}")
    file_path = f"{workspace_path}/{filename}" 

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        content = "File not found"

    # Eventually you'll write this to your memory store.
    return content