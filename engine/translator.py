from engine.processor import suggest_word
from engine.jsonloader import simplify_text, load_dictionaries
import spacy

nlp = spacy.load("en_core_web_sm")


def smart_translator(user_input, all_json, reverse_words_phrases, simple_keys, reverse_simple_keys):
    user_input = user_input.strip().lower()

    if user_input in all_json: return all_json[user_input]

    if user_input in reverse_words_phrases: return reverse_words_phrases[user_input]

    doc = nlp(user_input)

    return "imeela, we don't have this one yet."

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
