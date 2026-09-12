def write_file(filename: str, new_content:str) -> str:
    agent_workspace_path = "urlshortener"
    file_path = f"{agent_workspace_path}/{filename}"
    print(f"writing {filename}")
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(new_content)
            response = f"File {filename} replaced successfully"
    except PermissionError:
        response = f"Error: You do not have permission to write to '{filename}'."

    except FileNotFoundError:
        response = f"Error: The directory for '{filename}' does not exist."

    except Exception as e:
        response = f"An unexpected error occurred: {e}"
    print(response)
    return response;
    

