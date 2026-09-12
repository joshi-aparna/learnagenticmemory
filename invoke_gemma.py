from ollama import chat
from read_file_tool import read_file
from write_file_tool import write_file
from execute_python_tool import execute_file
from add_memory_tool import archival_memory_insert
from update_memory_tool import archival_memory_update
from delete_memory_tool import delete_memory
from search_memory_tool import archival_memory_search
from core_memory_tool import core_memory_append, core_memory_replace, load_core_memory

model="gemma4:e4b"
prompt = """
Do you know my name? What do you know about me?
"""

def build_system_prompt():
    core_memory = load_core_memory()
    system_prompt = f"""
You are a stateful agent with access to tools and persistent memory.

CORE MEMORY
Core memory is always included in your context. It contains compact, high-value information that should remain readily available across sessions, such as important project goals, stable architectural decisions, user preferences, constraints, and important current project state.

Keep core memory concise. Update it when important information changes. Prefer replacing or updating existing information rather than creating duplicates.

ARCHIVAL MEMORY
Archival memory is persistent but is not automatically included in your context. It contains information that may be useful in future sessions but does not need to remain continuously visible, such as implementation decisions and their rationale, discoveries, completed milestones, unresolved questions, and historical project context.

Search archival memory when the current task may depend on information established previously but not available in your current context.

MEMORY MANAGEMENT
You are responsible for deciding what information should be remembered and where it should be stored.

Do not store transient conversation details or information unlikely to be useful later.

When completing meaningful project work, consider whether important information should be persisted for future sessions.

Use core memory for information that is frequently relevant. Use archival memory for information that is useful but does not need to be continuously visible.

When possible, update an existing memory rather than creating a duplicate.

ENVIRONMENT
Use read_file, write_file, and execute to inspect, modify, and test files when needed.
CORE MEMORY
{chr(10).join(core_memory)}

Complete the user's task using the available tools. Do not claim something was done unless you have actually done it.
"""
    return system_prompt


messages=[
    {

            "role": "system",
            "content": build_system_prompt()
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
while True:

    response = chat(
        model=model,
        messages=messages,
        tools=[read_file, write_file, execute_file, archival_memory_insert, archival_memory_search, archival_memory_update, delete_memory, core_memory_replace, core_memory_append]
    )
    print(response.message)
    messages.append(response.message)
    if not response.message.tool_calls: 
        write_file("log.txt", "prompt=" + prompt + "\nmessages=" + str(messages) + "\n response =" + response.message.content)
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
        elif name == "archival_memory_insert":
            result = archival_memory_insert(**arguments)
        elif name == "archival_memory_search":
            result = archival_memory_search(**arguments)
        elif name == "archival_memory_update":
            result = archival_memory_update(**arguments)
        elif name == "delete_memory":
            result = delete_memory(**arguments)
        elif name == "core_memory_append":
            result = core_memory_append(**arguments)
        elif name == "core_memory_replace":
            result = core_memory_replace(**arguments)
        else: 
            result = f"ERROR: unknown tool: {name}"
        messages.append({ "role": "tool", "content": result })
    print(response.message)