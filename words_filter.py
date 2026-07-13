import sys
from word_class import Word
from enum import Enum
from collections import defaultdict
import math

# SETTINGS
SHOW_STATS: bool = True
REMOVE_ACCENTS: bool = True
MIN_WORD_LENGTH: int = 4
MAX_WORD_LENGTH: int = 10
DENY_ONLY_CAPS: bool = True
DENY_ONLY_CONSONANTS: bool = True
DENY_ONLY_SAME_LETTER: bool = False
DENY_CONTAINS_DIGIT: bool = True
DENY_CONTAINS_SPECIAL_CHARACTER: bool = True

invalid_words_by_reason: defaultdict = defaultdict(list)
valid_words: set[str] = set()


class DenyReason(Enum):
    TOO_SHORT = "TOO SHORT"
    TOO_LONG = "TOO LONG "
    ONLY_CAPS = "ONLY CAPS"
    ONLY_CONSONANTS = "ONLY CONSONANTS"
    ONLY_SAME_LETTER = "ONLY SAME LETTER"
    CONTAINS_DIGIT = "CONTAINS DIGIT"
    CONTAINS_SPECIAL_CHARACTER = "CONTAINS SPECIAL CHARACTER"


def main() -> None: 

    # Handle wrong usage
    if not 3 <= len(sys.argv) <= 4:
        print("Usage: python words_filter.py [source_filepath] [target_filepath] [line_limit]")
        sys.exit()

    # Apply word limit / handle wrong usage
    line_limit = math.inf
    if len(sys.argv) == 4:
        try:
            line_limit = int(sys.argv[3])
        except:
            print("Usage: python words_filter.py [source_filepath] [target_filepath] [line_limit]")
            sys.exit()

    # Get filepaths from CLI
    source_filepath: str = sys.argv[1]
    target_filepath: str = sys.argv[2]

    # Get unique lines from source file
    unique_lines: set[str] = get_unique_lines_from_file(source_filepath)
    num_unique_lines = len(unique_lines)

    # Loop over unique lines
    num_lines_handled: int = 0
    for line in unique_lines:

        # Stop at word limit
        if num_lines_handled >= line_limit:
            break

        num_lines_handled += 1

        # Show progress every 25000 lines
        if num_lines_handled % 25000 == 0 or num_lines_handled == num_unique_lines:
            progress_percentage = round((num_lines_handled / num_unique_lines) * 100, 2)
            print(f"{progress_percentage}%", end="\r")

        handle_word(Word(line.strip()))

    write_list_to_file(sorted(valid_words), target_filepath)
    write_to_log()

    if SHOW_STATS:
        print("------------------")
        show_totals(num_lines_handled)
        print("------------------")
        show_num_invalid_strings_per_reason()


def handle_word(word: Word) -> None:
    word.strip_special_characters()

    substrings = word.get_substrings()

    if len(substrings) > 1:
        for substring in word.get_substrings():
            handle_word(Word(substring))
        return


    if REMOVE_ACCENTS:
        word.remove_accents()

    if word.length() < MIN_WORD_LENGTH:
        log_invalid_word(word, DenyReason.TOO_SHORT)
        return
    
    elif word.length() > MAX_WORD_LENGTH:
        log_invalid_word(word, DenyReason.TOO_LONG)
        return

    elif DENY_ONLY_CAPS and word.is_only_caps():
        log_invalid_word(word, DenyReason.ONLY_CAPS)
        return

    elif DENY_ONLY_CONSONANTS and word.is_only_consonants():
        log_invalid_word(word, DenyReason.ONLY_CONSONANTS)
        return

    elif DENY_ONLY_SAME_LETTER and word.is_only_same_letter():
        log_invalid_word(word, DenyReason.ONLY_SAME_LETTER)
        return

    elif DENY_CONTAINS_DIGIT and word.contains_digit():
        log_invalid_word(word, DenyReason.CONTAINS_DIGIT)
        return

    elif DENY_CONTAINS_SPECIAL_CHARACTER and word.contains_special_character():
        log_invalid_word(word, DenyReason.CONTAINS_SPECIAL_CHARACTER)
        return

    # SUCCESS! Word is valid!
    valid_words.add(word.string + "\n") # Add \n for fast writelines() later

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


def show_totals(num_lines_handled) -> None:
    print(f"Lines handled: {format_large_int(num_lines_handled)}")
    print(f"Valid words found: {format_large_int(len(valid_words))}")


def format_large_int(number: int, sep: str = ".") -> str:
    return f"{number:,}".replace(",", ".")


def show_num_invalid_strings_per_reason() -> None:
    for reason in invalid_words_by_reason:
        num_invalid_strings: int = len(invalid_words_by_reason[reason])
        print(f"INVALID [{reason.value}]: {format_large_int(num_invalid_strings)} words")


def log_invalid_word(word: Word, reason: DenyReason) -> None:
    invalid_words_by_reason[reason].append(word.string)


def write_to_log() -> None:
    with open("log.txt", "w", encoding="utf-8") as log:
        for reason in invalid_words_by_reason:
            log.write(
                "----------------------------------------------------------------------------\n"
            )
            log.write(f"{reason.value} ({len(invalid_words_by_reason[reason])} words) \n")
            log.write(
                "----------------------------------------------------------------------------\n"
            )
            for word in invalid_words_by_reason[reason]:
                log.write(word + "\n")
            log.write("\n")


if __name__ == "__main__":
    main()
