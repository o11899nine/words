from unidecode import unidecode
import re

class Word:
    def __init__(self, string: str):
        self.string: str = string

    def strip_special_characters(self) -> None:
        self.string = self.string.strip("!\",#$%&?@_£'*-+./()")

    def remove_accents(self) -> None:
        self.string = unidecode(self.string)

    def is_only_caps(self) -> bool:
        return self.string.isupper()

    def is_only_consonants(self) -> bool:
        consonants = set("bcdfghjklmnpqrstvwxyz")
        return all(char in consonants for char in self.string.lower())

    def is_only_same_letter(self) -> bool:
        return all(char.lower() == self.string[0].lower() for char in self.string)

    def contains_digit(self) -> bool:
        return any(char.isdigit() for char in self.string)

    def length(self) -> int:
        return len(self.string)

    def contains_special_character(self) -> bool:
        return bool(re.search(r"[^a-zA-Z0-9]", self.string))
    
    def split_multiple(self) -> list[str]:
        return [w for w in re.split(r'[_\s\:\\\-\,\/]+', self.string) if w]
