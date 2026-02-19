from engine.jsonloader import simplify_text
from engine.processor import suggest_word

class IgboTranslator:
    def __init__(self, dict_path):
        from engine.jsonloader import load_dictionaries
        self.all_json, self.rev_data, self.simple_keys, self.rev_simple_keys = load_dictionaries(dict_path)

    def translate(self, text):
        text = text.strip().lower()
        simple_input = simplify_text(text)

        # 1. Exact Match Check
        if text in self.all_json: return self.all_json[text]
        if text in self.rev_data: return self.rev_data[text]

        # 2. Simplified Match (Ignoring accents)
        if simple_input in self.simple_keys:
            return self.all_json[self.simple_keys[simple_input]]
        if simple_input in self.rev_simple_keys:
            return self.rev_data[self.rev_simple_keys[simple_input]]

        # 3. Fuzzy Suggestion
        sugg_igbo = suggest_word(simple_input, self.simple_keys.keys())
        if sugg_igbo:
            orig = self.simple_keys[sugg_igbo]
            return f"Did you mean '{orig}'? → {self.rev_data.get(orig)}"

        sugg_eng = suggest_word(simple_input, self.rev_simple_keys.keys())
        if sugg_eng:
            orig = self.rev_simple_keys[sugg_eng]
            return f"Did you mean '{orig}'? → {self.all_json.get(orig)}"

        return "Ndo, I couldn't find that word."