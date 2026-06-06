import os
import subprocess


def run_python_file(
    working_directory: str,
    file_path: str,
    args: list[str] | None = None,
) -> str:
    """
    Execute a Python file under `working_directory` with optional args.

    Always returns a string:
      - Success-like info about exit code and output
      - Error: ...   for any validation or runtime error
    """
    try:
        # 1. Resolve working directory and target file path
        working_dir_abs = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # 2. Ensure file is inside the working directory
        if os.path.commonpath([working_dir_abs, absolute_file_path]) != working_dir_abs:
            return (
                f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            )

        # 3. Ensure the target exists and is a regular file
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # 4. Ensure it is a Python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # 5. Build the command
        command = ["python", absolute_file_path]
        if args:
            command.extend(args)

        # 6. Run the subprocess
        completed = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # 7. Build output string
        parts: list[str] = []

        if completed.returncode != 0:
            parts.append(f"Process exited with code {completed.returncode}")

        stdout = completed.stdout or ""
        stderr = completed.stderr or ""

        if not stdout and not stderr:
            parts.append("No output produced")
        else:
            if stdout:
                parts.append(f"STDOUT:\n{stdout}")
            if stderr:
                parts.append(f"STDERR:\n{stderr}")

        return "\n".join(parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"