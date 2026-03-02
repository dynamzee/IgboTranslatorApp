import json
import unicodedata

def simplify_text(text):
    nkowa = unicodedata.normalize("NFD", text)
    nkowa = "".join(char for char in nkowa if unicodedata.category(char) != "Mn")
    return nkowa.lower()


def load_dictionaries(path_list):
    all_json = {}

    for path in path_list:
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
                all_json.update(data)
        except FileNotFoundError:
            print(f"Warning: File not found at {path}")

    reverse_words_phrases = {}
    for eng, igbo in all_json.items():
        reverse_words_phrases.setdefault(igbo, []).append(eng)

    simple_keys = {simplify_text(v): v for v in all_json.values()}
    reverse_simple_keys = {simplify_text(k): k for k in reverse_words_phrases.keys()}

    return all_json, reverse_words_phrases, simple_keys, reverse_simple_keys

