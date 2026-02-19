from engine.translator import IgboTranslator
from engine.processor import get_greeting

def run_app():
    all_json = ["my_data/igbo_phrases_dict.json", "my_data/igbo_words_dict.json"]

    translator = IgboTranslator(all_json)

    print(get_greeting())
    print("<* WELCOME TO DYNA's IGBO TRANSLATOR APP *>")

    user_input = input("Enter the word/phrase to translate: ").strip().lower()
    result = translator.translate(user_input)

    print(f"translation: {result}")

if __name__ == "__main__":
    run_app()

