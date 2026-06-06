import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    """
    Safely write `content` to `file_path` under `working_directory`.

    Always returns a string:
      - Success: 'Successfully wrote to "{file_path}" ({len(content)} characters written)'
      - Error:   'Error: ...'
    """
    try:
        # 1. Absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # 2. Build normalized target file path
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # 3. Ensure target_path is within working_dir_abs
        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            return (
                f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            )

        # 4. If something already exists at target_path and it is a directory, error
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # 5. Ensure parent directories exist
        parent_dir = os.path.dirname(target_path)
        os.makedirs(parent_dir, exist_ok=True)

        # 6. Open file in write mode and overwrite contents
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"