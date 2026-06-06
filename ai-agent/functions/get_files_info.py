# tools/files.py

import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    """
    List files in `directory` under `working_directory`.

    Always returns a string:
      - Success: one line per entry: "- NAME: size: N bytes, is_dir: True/False"
      - Error:   'Error: ...'
    """
    try:
        # 1. Absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # 2. Build normalized target directory path (treat `directory` as relative)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # 3. Ensure target_dir is within working_dir_abs
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
        if not valid_target_dir:
            return (
                f'Error: Cannot list "{directory}" as it is outside the '
                f"permitted working directory"
            )

        # 4. Ensure target_dir is actually a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # 5. Build listing lines
        lines: list[str] = []
        for entry_name in os.listdir(target_dir):
            full_path = os.path.join(target_dir, entry_name)
            is_dir = os.path.isdir(full_path)
            try:
                size = os.path.getsize(full_path)
            except OSError:
                size = 0

            lines.append(
                f"- {entry_name}: size: {size} bytes, is_dir: {is_dir}"
            )

        # If directory is empty, still return something deterministic
        if not lines:
            return f'No entries found in "{directory}"'

        return "\n".join(lines)

    except Exception as e:
        # Any unexpected errors become error strings for the LLM to handle
        return f"Error: {e}"