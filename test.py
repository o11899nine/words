import re

def split_multiple(string: str) -> list[str]:
    return [w for w in re.split(r'[_\s-]+', string) if w]

print(split_multiple("konijn en koffie"))