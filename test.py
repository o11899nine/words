def is_all_same_letter(word: str) -> bool:
    for i in range(len(word) - 1):
        if word[i] != word[i + 1]:
            return False
    return True

print(is_all_same_letter("aaaaaaaaaaab"))