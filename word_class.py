from unidecode import unidecode

class Word:
    def __init__(self, string: str):
        self.string: str = string

    def strip(self):
        self.string = self.string.strip()
        self.string = self.string.strip("!\",#$%&_£'*-+./")
    
    def remove_accents(self):
        self.string = unidecode(self.string)

    
