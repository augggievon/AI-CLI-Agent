# functions/call_functions.py

from collections.abc import Callable
from typing import Any

from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .run_python_file import run_python_file
from .write_to_files import write_file

available_functions = [
    {
        "type": "function",
        "function": {
            "name": "get_files_info",
            "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_file_content",
            "description": "Reads and returns the contents of a file relative to the working directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to read, relative to the working directory",
                    },
                },
                "required": ["file_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_python_file",
            "description": "Executes a Python file relative to the working directory, with optional arguments",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the Python file to execute, relative to the working directory",
                    },
                    "args": {
                        "type": "array",
                        "description": "Optional list of string arguments to pass to the Python file",
                        "items": {"type": "string"},
                    },
                },
                "required": ["file_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes or overwrites a file relative to the working directory with the provided content",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to write, relative to the working directory",
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the specified file",
                    },
                },
                "required": ["file_path", "content"],
            },
        },
    },
]

function_map: dict[str, Callable[..., str]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(
    function_name: str,
    raw_args: dict[str, Any] | None,
    verbose: bool = False,
) -> dict[str, Any]:
    function_name = function_name or ""

    if verbose:
        print(f"Calling function: {function_name}({raw_args or {}})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in function_map:
        return {"error": f"Unknown function: {function_name}"}

    args: dict[str, Any] = dict(raw_args) if raw_args else {}
    args["working_directory"] = "./calculator"

    func = function_map[function_name]
    try:
        result = func(**args)
        return {"result": result}
    except Exception as e:
        return {"error": f"Exception while calling {function_name}: {e}"}