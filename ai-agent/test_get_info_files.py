from functions.get_files_info import get_files_info


def main() -> None:
    # 1) Current directory
    print('get_files_info("calculator", "."):')
    print("Result for current directory:")
    print(get_files_info("calculator", "."))
    print()  # blank line

    # 2) 'pkg' directory
    print('get_files_info("calculator", "pkg"):')
    print("Result for 'pkg' directory:")
    print(get_files_info("calculator", "pkg"))
    print()  # blank line

    # 3) '/bin' directory (should be an error)
    print('get_files_info("calculator", "/bin"):')
    print("Result for '/bin' directory:")
    print(get_files_info("calculator", "/bin"))
    print()  # blank line

    # 4) '../' directory (should be an error)
    print('get_files_info("calculator", "../"):')
    print("Result for '../' directory:")
    print(get_files_info("calculator", "../"))


if __name__ == "__main__":
    main()