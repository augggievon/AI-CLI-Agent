from functions.get_file_content import get_file_content


def main() -> None:
    # 1) Large file truncation test
    result = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")
    print()  # blank line for readability

    # 2) Smaller file: main.py
    print('get_file_content("calculator", "main.py"):')
    result = get_file_content("calculator", "main.py")
    print(result)
    print()

    # 3) Smaller file: pkg/calculator.py
    print('get_file_content("calculator", "pkg/calculator.py"):')
    result = get_file_content("calculator", "pkg/calculator.py")
    print(result)
    print()

    # 4) Outside working directory: /bin/cat
    print('get_file_content("calculator", "/bin/cat"):')
    result = get_file_content("calculator", "/bin/cat")
    print(result)
    print()

    # 5) Nonexistent file: pkg/does_not_exist.py
    print('get_file_content("calculator", "pkg/does_not_exist.py"):')
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(result)


if __name__ == "__main__":
    main()