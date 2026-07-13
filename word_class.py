from unidecode import unidecode

class Word:
    def __init__(self, string: str):
        self.string: str = string

    def strip_special_characters(self):
        self.string = self.string.strip("!\",#$%&_£'*-+./")

    def remove_accents(self):
        self.string = unidecode(self.string)

    def is_only_caps(self):
        return self.string.is_upper()

    def is_only_consonants(self):
        consonants = set("bcdfghjklmnpqrstvwxyz")
        return all(char in consonants for char in self.string.lower())

    def is_only_same_letter(self):
        return all(char.lower() == self.string[0].lower() for char in self.string)

    def contains_digit(self):
        return any(char.isdigit() for char in self.string)
    
    def length(self):
        return len(self.string)
