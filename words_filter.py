import sys
from word_class import Word
from enum import Enum
from collections import defaultdict
import os
import math

invalid_strings_by_reason: defaultdict = defaultdict(list)
valid_strings: set[str] = set()

num_lines_handled: int = 0
num_lines: int = 0
num_invalid_strings: int = 0

# Settings
SORT_ALPHABETICAL: bool = True

STRIP_SPECIAL_CHARACTERS: bool = True
REMOVE_ACCENTS: bool = False

MIN_WORD_LENGTH: int = 1
DENY_ONLY_CAPS: bool = False
DENY_ONLY_CONSONANTS: bool = False
DENY_ONLY_SAME_LETTER: bool = False
DENY_CONTAINS_DIGIT: bool = False

class DenyReason(Enum):
    TOO_SHORT = "TOO SHORT"
    ONLY_CAPS = "ONLY CAPS"
    ONLY_CONSONANTS = "ONLY CONSONANTS"
    ONLY_SAME_LETTER = "ONLY SAME LETTER"
    CONTAINS_DIGIT = "CONTAINS DIGIT"


def main() -> None:
    global num_lines_handled
   

    if not 3 <= len(sys.argv) <= 4:
        print(
            "Usage: python words_filter.py [source_filepath] [target_filepath] [word_limit]"
        )
        sys.exit()

    source_filepath: str = sys.argv[1]
    target_filepath: str = sys.argv[2]
    word_limit = math.inf

    if len(sys.argv) == 4:
        try:
            word_limit = int(sys.argv[3])
        except:
            print(
                "Usage: python words_filter.py [source_filepath] [target_filepath] [word_limit]"
            )
            sys.exit()

    unique_lines: set[str] = get_unique_lines_from_file(source_filepath)
    num_lines = len(unique_lines)


    for line in unique_lines:

        # Stop at word limit
        if num_lines_handled >= word_limit:
            break

        # Show progress
        num_lines_handled += 1
        progress_percentage = round((num_lines_handled / num_lines) * 100, 2)
        print(f"{progress_percentage}%", end="\r")

        word = Word(line.strip())

        if STRIP_SPECIAL_CHARACTERS:
            word.strip_special_characters()

        if REMOVE_ACCENTS:
            word.remove_accents()

        if word.length() < MIN_WORD_LENGTH:
            log_invalid_word(word, DenyReason.TOO_SHORT)
            continue

        if DENY_ONLY_CAPS and word.is_only_caps():
            log_invalid_word(word, DenyReason.ONLY_CAPS)
            continue

        if DENY_ONLY_CONSONANTS and word.is_only_consonants():
            log_invalid_word(word, DenyReason.ONLY_CONSONANTS)
            continue

        if DENY_ONLY_SAME_LETTER and word.is_only_same_letter():
            log_invalid_word(word, DenyReason.ONLY_SAME_LETTER)
            continue

        if DENY_CONTAINS_DIGIT and word.contains_digit():
            log_invalid_word(word, DenyReason.CONTAINS_DIGIT)
            continue

        # SUCCESS! Word is valid!
        valid_strings.add(word.string + "\n") # Add \n for fast writelines() later

    if SORT_ALPHABETICAL:
        valid_strings = sorted(valid_strings)
    else:
        valid_strings = list(valid_strings)
        
    write_list_to_file(sorted(valid_strings), target_filepath)
    print("------------------")
    show_totals()
    print("------------------")
    show_num_invalid_strings_per_reason()

    write_to_log()


def write_list_to_file(list: list, filepath: str) -> None:
    print(f"Writing set to '{filepath}' ...")
    with open(filepath, "w", encoding="utf-8") as file:
        file.writelines(list)
    print("Done!")


def get_unique_lines_from_file(filepath: str) -> set[str]:
    # Read all lines
    print(f"Reading lines from '{filepath}' ...")
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()
    print(f"'{filepath}' contains {format_large_int(len(lines))} lines.")

    # Extract unique lines
    print(f"Extracting unique lines ...")
    unique_lines = set(lines)
    print(f"Done! {format_large_int(len(unique_lines))} unique lines found.")

    return unique_lines


def show_totals() -> None:
    print(f"Lines handled: {format_large_int(num_lines_handled)}")
    print(f"Valid words found: {format_large_int(len(valid_strings))}")


def format_large_int(number: int, sep: str = ".") -> str:
    return f"{number:,}".replace(",", ".")


def show_num_invalid_strings_per_reason() -> None:
    for reason in invalid_strings_by_reason:
        num_invalid_strings: int = len(invalid_strings_by_reason[reason])
        print(f"INVALID [{reason.value}]: {format_large_int(num_invalid_strings)} words")


def log_invalid_word(word: Word, reason: DenyReason) -> None:
    global num_invalid_strings
    invalid_strings_by_reason[reason].append(word.string)
    num_invalid_strings += 1


def write_to_log() -> None:
    with open("log.txt", "w", encoding="utf-8") as log:
        for reason in invalid_strings_by_reason:
            log.write(
                "----------------------------------------------------------------------------\n"
            )
            log.write(f"{reason.value} ({len(invalid_strings_by_reason[reason])} words) \n")
            log.write(
                "----------------------------------------------------------------------------\n"
            )
            for word in invalid_strings_by_reason[reason]:
                log.write(word + "\n")
            log.write("\n")


if __name__ == "__main__":
    main()
