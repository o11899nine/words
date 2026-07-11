import sys

def main() -> None:

    if len(sys.argv) != 3:
        print("Usage: python save_unique.py [source_filepath] [target_filepath]")
        sys.exit()

    source_filepath: str = sys.argv[1]
    target_filepath: str = sys.argv[2]

    unique_words_set: set = get_unique_words_from_file(source_filepath)
    print(f"{format_large_int(len(unique_words_set), '.')} unique words extracted.")


    save_words_to_file(sorted(unique_words_set), target_filepath)


def get_unique_words_from_file(filepath: str) -> set:
    with open(filepath, "r", encoding="utf-8") as file:
        all_words = file.readlines()

    total_words = len(all_words)
    print(f"Source file contains {format_large_int(total_words, '.')} total lines/words.")
    print(f"Extracting unique words from {filepath}...")

    # Convert the list to a set to remove duplicates
    return set(all_words)


def save_words_to_file(words: list[str], filepath: str) -> None:
    print(f"Writing sorted words to '{filepath}' ...")
    with open(filepath, "w", encoding="utf-8") as file:
        file.writelines(words)
    print("Done!")


def format_large_int(number: int, separator: str) -> str:
    return f"{number:,}".replace(",", separator)

if __name__ == "__main__":
    main()
