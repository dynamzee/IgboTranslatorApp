from engine.jsonloader import simplify_text
from engine.processor import suggest_word
from engine.jsonloader import load_dictionaries

class IgboTranslator:
    def __init__(self, dict_path):
        self.all_json, self.reverse_words_phrases, self.simple_keys, self.reverse_simple_keys = load_dictionaries(dict_path)

    def translate(self, text):
        text = text.strip().lower()
        simple_input = simplify_text(text)

        if text in self.all_json: return self.all_json[text]
        if text in self.reverse_words_phrases: return self.reverse_words_phrases[text]

        if simple_input in self.simple_keys:
            return self.all_json[self.simple_keys[simple_input]]

        if simple_input in self.reverse_simple_keys:
            return self.reverse_words_phrases[self.reverse_simple_keys[simple_input]]

        suggestion_in_igbo = suggest_word(simple_input, self.simple_keys.keys())
        if suggestion_in_igbo:
            original = self.simple_keys[suggestion_in_igbo]
            return f"Did you mean '{original}'? → {self.reverse_words_phrases.get(original)}"

        suggestion_in_english = suggest_word(simple_input, self.reverse_simple_keys.keys())
        if suggestion_in_english:
            original = self.reverse_simple_keys[suggestion_in_english]
            return f"Did you mean '{original}'? → {self.all_json.get(original)}"

        return "Ndo, I couldn't find that word."
