import json

with open("nouns.json", "r") as source_file:
    with open("wordlist.txt", "a") as target_file:

        data = json.load(source_file)

        for word in data:
            print(word)

            target_file.write(word + "\n")
            conjugations = data[word]

            if isinstance(conjugations, list):
                for conjugation in conjugations:
                    target_file.write(conjugation + "\n")
            else:
                target_file.write(conjugations + "\n")
