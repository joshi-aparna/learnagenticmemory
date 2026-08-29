from ollama import chat
from read_file_tool import read_file
from write_file_tool import write_file
from execute_python_tool import execute_file
model="gemma4:e4b"
agent_workspace_path = "workspace"

messages=[
        {
            "role": "user",
            "content": "write a python file to add two numbers and a unit test file to test the code. Execute the unit test file to validate the code."
        }
    ]
while True:

    response = chat(
        model=model,
        messages=messages,
        tools=[read_file, write_file, execute_file]
    )
    print(response.message)
    messages.append(response.message)
    if not response.message.tool_calls: 
        print(response.message.content) 
        break
    for tool_call in response.message.tool_calls:
        name = tool_call.function.name 
        arguments = tool_call.function.arguments 
        # Execute the requested tool 
        if name == "read_file": 
            result = read_file(**arguments) 
        elif name == "write_file": 
            result = write_file(**arguments) 
        elif name == "execute_file": 
            result = execute_file(**arguments) 
        else: 
            result = f"ERROR: unknown tool: {name}"
        messages.append({ "role": "tool", "content": result })
    print(response.message)