from engine.processor import suggest_word
from engine.jsonloader import simplify_text, load_dictionaries
import spacy
import re

nlp = spacy.load("en_core_web_sm")


def normalize_text_variations(text):
    variations = {
        "i'm": "i am",
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
    normalized_words = [variations.get(w, w) for w in words]
    return " ".join(normalized_words)


class IgboTranslator:
    def __init__(self, paths):
        (
            self.all_json,
            self.reverse_words_phrases,
            self.simple_keys,
            self.reverse_simple_keys
        ) = load_dictionaries(paths)

    def translate(self, text):
        original_text = text.strip().lower()
        text = normalize_text_variations(original_text)

        if original_text in self.all_json:
            return self.all_json[original_text]
        if original_text in self.reverse_words_phrases:
            return self.reverse_words_phrases[original_text]

        translation = []
        segmented_text = re.split(r'[,?.]', original_text)

        for segment in segmented_text:
            separated_segments = segment.strip()
            if not separated_segments: continue

            found = False
            normalized_segment = normalize_text_variations(separated_segments)
            simple_segment = simplify_text(separated_segments)

            if separated_segments in self.all_json:
                translation.append(self.all_json[separated_segments]); found = True
            elif normalized_segment in self.all_json:
                translation.append(self.all_json[normalized_segment]); found = True
            elif simple_segment in self.simple_keys:
                translation.append(self.all_json[self.simple_keys[simple_segment]]); found = True
            elif separated_segments in self.reverse_words_phrases:
                translation.append(self.reverse_words_phrases[separated_segments]); found = True
            elif simple_segment in self.reverse_simple_keys:
                translation.append(self.reverse_words_phrases[self.reverse_simple_keys[simple_segment]]); found = True

            if not found:
                with_question = f"{separated_segments}?"
                if with_question in self.all_json:
                    translation.append(self.all_json[with_question]);
                    found = True

            if not found:
                doc = nlp(separated_segments)
                lemmas = [token.lemma_ for token in doc if not token.is_punct]
                for key in self.all_json.keys():
                    if key in separated_segments or any(lemma in key for lemma in lemmas if len(lemma) > 3):
                        translation.append(self.all_json[key])
                        found = True
                        break

            if not found:
                translation.append(f"[{separated_segments}?]")

        if any("[" not in part for part in translation):
            return ", ".join(translation)

        simple_input = simplify_text(text)

        suggestion_in_igbo = suggest_word(simple_input, self.reverse_simple_keys.keys())
        if suggestion_in_igbo:
            matched = self.reverse_simple_keys[suggestion_in_igbo]
            return f"Did you mean '{matched}'? → {self.reverse_words_phrases[matched]}"

        suggestion_in_english = suggest_word(simple_input, self.simple_keys.keys())
        if suggestion_in_english:
            matched = self.simple_keys[suggestion_in_english]
            return f"Did you mean '{matched}'? → {self.all_json[matched]}"

        return "Ndo, I couldn't find that word."






