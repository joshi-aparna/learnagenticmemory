from ollama import chat
from read_file_tool import read_file
from write_file_tool import write_file
from execute_python_tool import execute_file
from add_memory_tool import add_memory
from update_memory_tool import update_memory
from delete_memory_tool import delete_memory
from search_memory_tool import search_memory

model="gemma4:e4b"

messages=[
    {

            "role": "system",
            "content": """
You are an agent with access to long-term memory.

Before making assumptions about the user's preferences,
past decisions, or previously established choices,
use search_memory when that information could affect
the task.

Do not search memory when it is irrelevant.
"""
        },
        {
            "role": "user",
            "content": "Write code create a function that adds two numbers. Use my preferred programming language. Write unit tests. Run the unit tests to confirm that your function works."
        }
    ]
while True:

    response = chat(
        model=model,
        messages=messages,
        tools=[read_file, write_file, execute_file, add_memory, update_memory, search_memory, delete_memory]
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
        elif name == "add_memory":
            result = add_memory(**arguments)
        elif name == "update_memory":
            result = update_memory(**arguments)
        elif name == "search_memory":
            result = search_memory(**arguments)
        elif name == "delete_memory":
            result = delete_memory(**arguments)
        else: 
            result = f"ERROR: unknown tool: {name}"
        messages.append({ "role": "tool", "content": result })
    print(response.message)