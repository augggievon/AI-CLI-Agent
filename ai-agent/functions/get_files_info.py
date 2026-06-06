# tools/files.py

import os


def get_files_info(working_directory: str, directory: str) -> str:
    """
    Validate that `directory` is a safe subdirectory of `working_directory`.

    Always returns a string:
      - Success: 'Success: "{directory}" is within the working directory'
      - Error:   'Error: ...'
    """
    try:
        # 1. Absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # 2. Build normalized target directory path (treat `directory` as relative)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # 3. Ensure target_dir is within working_dir_abs using commonpath [web:214][web:219]
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
        
        lines = []

        for i in os.listdir(target_dir):
            full_path = os.path.join(target_dir, i)
            is_dir = os.path.isdir(full_path)
            size = os.path.getsize(full_path)

            entry={

                "name": name,
                "size": size,
                "is_dir": is_dir
            }
            

            lines = f"- {name}: file size: {size} bytes: is_dir: {is_dir}"

            lines.append(entry)

            result = "\n".join(lines)
            return result



        # 5. If everything is valid, return success string
        return f'Success: "{directory}" is within the working directory'
    
    

    except Exception as e:
        # Any unexpected errors become error strings for the LLM to handle
        return f"Error: {e}"
    
        