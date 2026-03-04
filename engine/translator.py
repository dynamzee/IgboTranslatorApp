import os
import spacy
import re
from engine.jsonloader import load_dictionaries

if os.environ.get("RENDER"):
    JSON_PHRASE_PATH = "igbo_phrases_dict.json"
    JSON_WORD_PATH = "igbo_words_dict.json"
else:
    JSON_PHRASE_PATH = "my_data/igbo_phrases_dict.json"
    JSON_WORD_PATH = "my_data/igbo_words_dict.json"

nlp = spacy.load("en_core_web_sm")

def normalize_text_variations(text):
    variations = {
        "i’m": "i am",
        "don't": "do not",
        "can't": "cannot",
        "isn't": "is not",
        "aren't": "are not",
        "hasn't": "has not",
        "hadn't": "had not",
        "shan't": "shall not",
        "doesn't": "does not",
        "didn't": "did not",
        "i've": "i have"
    }
    words = text.lower().split()
    return " ".join([variations.get(word, word) for word in words])

class IgboTranslator:
    def __init__(self):
        paths = [JSON_PHRASE_PATH, JSON_WORD_PATH]
        (self.my_json_dictionaries, self.reverse_words_phrases,
         self.simple_keys, self.reverse_simple_keys) = load_dictionaries(paths)

    def translate(self, text):
        text = text.strip().lower()
        text = normalize_text_variations(text)

        if text in self.my_json_dictionaries:
            return self.my_json_dictionaries[text]

        translation = []
        custom_json_phrases = re.split(r'[,?.]', text)

        for phrases in custom_json_phrases:
            phrase = phrases.strip()
            if not phrase: continue

            phrases_found_in_custom_json_dictionaries = False
            if phrase in self.my_json_dictionaries:
                translation.append(self.my_json_dictionaries[phrase])
                phrases_found_in_custom_json_dictionaries = True
            elif phrase + "?" in self.my_json_dictionaries:
                translation.append(self.my_json_dictionaries[phrase + "?"])
                phrases_found_in_custom_json_dictionaries = True

            if not phrases_found_in_custom_json_dictionaries:
                translation.append("not found")

        if "not found" in translation:
            return ""

        return ", ".join(translation)

