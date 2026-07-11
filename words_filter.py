import sys
import word_class
from enum import Enum
from collections import defaultdict
from unidecode import unidecode
import os
import math

unique_words: set = set()
invalid_words: defaultdict = defaultdict(list)
num_words: int = 0
num_valid_words: int = 0
num_invalid_words: int = 0


class DenyReason(Enum):
    NOT_ALPHA = "NOT ALPHA"
    ALL_CAPS = "ALL CAPS"
    ALL_CONSONANTS = "ALL CONSONANTS"
    SINGLE_LETTER = "SINGLE LETTER"
    DUPLICATE = "DUPLICATE"
    ALL_SAME_LETTER = "ALL SAME LETTER"


def main() -> None:
    global num_words
    global num_valid_words

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

    # 1. Read lines once into memory so we can get the length AND loop over them
    with open(source_filepath, "r", encoding="utf-8") as source_file:
        words = source_file.readlines()

    source_file_length: int = len(words)

    with open(target_filepath, "w", encoding="utf-8") as target_file:
        for word in words:

            # Stop at word limit
            if num_words >= word_limit:
                break

            # Show progress
            num_words += 1
            progress_percentage = round((num_words / source_file_length) * 100, 2)
            print(f"{progress_percentage}%")

            # Clean word: strip word and remove accents
            word = unidecode(word.strip())

            # Skip empty lines
            if not word:
                continue

            # Skip duplicates
            if word in unique_words:
                log_invalid_word(word, DenyReason.DUPLICATE)
                continue

            # Add word to unique_words for duplicate checking
            unique_words.add(word)

            # Skip single-letter words
            if len(word) == 1:
                log_invalid_word(word, DenyReason.SINGLE_LETTER)
                continue

            # Skip words with non-alpha characters
            if not word.isalpha():
                log_invalid_word(word, DenyReason.NOT_ALPHA)
                continue

            # Skip words in all caps (abbreviations probably)
            if word.isupper():
                log_invalid_word(word, DenyReason.ALL_CAPS)
                continue

            # Skip words that are all consonants
            if is_all_consonants(word):
                log_invalid_word(word, DenyReason.ALL_CONSONANTS)
                continue

            # Skip words that consists of all the same letter ('aa' or 'bbb')
            if is_all_same_letter(word):
                log_invalid_word(word, DenyReason.ALL_SAME_LETTER)
                continue

            # SUCCESS! Word is valid!
            num_valid_words += 1
            unique_words.add(word)
            target_file.write(word + "\n")

    print("------------------")
    show_totals()
    print("------------------")
    show_num_invalid_words_per_reason()

    write_to_log()


def is_all_same_letter(word: str) -> bool:
    for i in range(len(word) - 1):
        if word[i] != word[i + 1]:
            return False
    return True


def clear_terminal() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def show_totals() -> None:
    print(f"Total words: {format_large_int(num_words)}")
    print(f"Valid words: {format_large_int(num_valid_words)}")
    print(f"Invalid words: {format_large_int(num_invalid_words)}")


def format_large_int(number: int) -> str:
    return f"{number:,}".replace(",", ".")


def show_num_invalid_words_per_reason() -> None:
    for reason in invalid_words:
        num_invalid_words: int = len(invalid_words[reason])
        print(f"INVALID [{reason.value}]: {format_large_int(num_invalid_words)} words")


def log_invalid_word(word: str, reason: DenyReason) -> None:
    global num_invalid_words
    invalid_words[reason].append(word)
    num_invalid_words += 1


def write_to_log() -> None:
    with open("log.txt", "w", encoding="utf-8") as log:
        for reason in invalid_words:
            log.write(
                "----------------------------------------------------------------------------\n"
            )
            log.write(f"{reason.value} ({len(invalid_words[reason])} words) \n")
            log.write(
                "----------------------------------------------------------------------------\n"
            )
            for word in invalid_words[reason]:
                log.write(word + "\n")
            log.write("\n")


def is_all_consonants(word: str) -> bool:
    if not word:
        return False

    consonants = set("bcdfghjklmnpqrstvwxyz")
    return all(character in consonants for character in word.lower())


if __name__ == "__main__":
    main()
