from engine.jsonloader import load_dictionaries
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def normalize_text_variations(text):
    variations = {
        "i’m": "i am", "don't": "do not", "can't": "cannot",
        "isn't": "is not", "aren't": "are not", "hasn't": "has not",
        "hadn't": "had not", "shan't": "shall not", "doesn't": "does not",
        "didn't": "did not", "i've": "i have"
    }
    words = text.lower().split()
    return " ".join([variations.get(w, w) for w in words])

class IgboTranslator:
    def __init__(self, paths):
        (self.all_json, self.reverse_words_phrases,
         self.simple_keys, self.reverse_simple_keys) = load_dictionaries(paths)

    def translate(self, text):
        original_text = text.strip().lower()
        text = normalize_text_variations(original_text)

        if original_text in self.all_json: return self.all_json[original_text]

        translation = []
        segmented_text = re.split(r'[,?.]', original_text)

        for segment in segmented_text:
            s = segment.strip()
            if not s: continue

            found = False
            if s in self.all_json:
                translation.append(self.all_json[s]); found = True
            elif s + "?" in self.all_json:
                translation.append(self.all_json[s + "?"]); found = True

            if not found:
                translation.append("not found")

        if "not found" in translation:
            return ""

        return ", ".join(translation)











