import os

from config import MAX_CHARS  # make sure config.py defines MAX_CHARS = 10000


def get_file_content(working_directory: str, file_path: str) -> str:
    """
    Read a file inside the working_directory with safety checks and truncation.

    Always returns a string:
      - On success: the file contents (possibly with a truncation note appended)
      - On error:   'Error: ...'
    """
    try:
        # 1. Absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # 2. Build normalized target file path (treat file_path as relative)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # 3. Ensure target_path is within working_dir_abs using commonpath
        valid_target = (
            os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        )

        if not valid_target:
            return (
                f'Error: Cannot read "{file_path}" as it is outside the '
                f"permitted working directory"
            )

        # 4. Ensure target_path is actually a regular file
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # 5. Open and read up to MAX_CHARS characters
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
            # Try to read one more character to detect truncation
            extra = f.read(1)

        if extra == "":
            # Not truncated
            return content
        else:
            # File has more data than MAX_CHARS
            content += (
                f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            )
            return content

    except Exception as e:
        # Any unexpected errors become error strings for the LLM to handle
        return f"Error: {e}"