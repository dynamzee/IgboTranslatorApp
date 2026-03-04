import json
import unicodedata

def simplify_text(text):
    remove_diacritics = unicodedata.normalize("NFD", text)
    remove_diacritics = "".join(char for char in remove_diacritics if unicodedata.category(char) != "Mn")
    return remove_diacritics.lower()

def load_dictionaries(paths_list):
    my_json_dictionaries = {}

    for path in paths_list:
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
                my_json_dictionaries.update(data)
        except FileNotFoundError:
            print(f"WARNING: file not found at {path}.")

    reverse_words_phrases = {}
    for english, igbo in my_json_dictionaries.items():
        reverse_words_phrases.setdefault(igbo, []).append(english)

    simple_keys = {simplify_text(v): v for v in my_json_dictionaries.values()}
    reverse_simple_keys = {simplify_text(k): k for k in reverse_words_phrases.keys()}

    return my_json_dictionaries, reverse_words_phrases, simple_keys, reverse_simple_keys

