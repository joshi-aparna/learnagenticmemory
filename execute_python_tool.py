from pathlib import Path
import subprocess
import sys

WORKSPACE = Path("workspace").resolve()
def execute_file(filename: str,  arguments: list[str] = []) -> str:
    """ Execute a Python file from the agent workspace. Only pass the python file name with arguments to the file """
    print(f"executing {filename}")
    path = (WORKSPACE / filename).resolve()
    if not path.is_relative_to(WORKSPACE):
        return "ERROR: file not found in the workspace."
    if not path.is_file():
        return f"ERROR: file does not exist: {filename}"
    # Only Python files may be executed 
    if path.suffix.lower() != ".py": 
        return "ERROR: execute only supports Python files."
    result = subprocess.run( [sys.executable, str(path), *arguments], capture_output=True, text=True )
    print(result.stdout + result.stderr)
    return result.stdout + result.stderr