import json
import unicodedata
import difflib
from datetime import datetime

def simplify_text(text: str) -> str:
    nkowa = unicodedata.normalize("NFD", text)
    nkowa = "".join(char for char in nkowa if unicodedata.category(char) != "Mn")
    return nkowa.lower()

def suggest_word(word: str, dictionary_keys):
    return difflib.get_close_matches(word, dictionary_keys, n=1, cutoff=0.6)

now = datetime.now()

with open("my_data/igbo_words_dict.json", "r", encoding="utf-8") as file:
    igbo_words_dict = json.load(file)
    reverse_igbo_words_dict = {}
    for eng, igbo in igbo_words_dict.items():
        reverse_igbo_words_dict.setdefault(igbo, []).append(eng)
    simple_igbo_keys = {simplify_text(v): v for v in igbo_words_dict.values()}
    reverse_simple_igbo_keys = {simplify_text(k): k for k in reverse_igbo_words_dict.keys()}

if now.hour < 12:
    print("Ututu oma, onye nke anyi. Anyi nabatara gi nnoor nke oma.")
elif now.hour < 16:
    print("Ehihie oma, onye nke anyi. Anyi nabatara gi nnoor nke oma.")
elif now.hour < 18:
    print("Mgbede oma, onye nke anyi. Anyi nabatara gi nnoor nke oma.")
else:
    print("Anyasi oma, onye nke anyi. Anyi nabatara gi nnoor nke oma.")

print("<* WELCOME TO DYNA's IGBO TRANSLATOR APP *>")

translate = input("Enter the word/phrase/sentence you want to translate: ").strip().lower()
simple_input = simplify_text(translate)

if translate in igbo_words_dict:
    print(f"Here is the translation: {igbo_words_dict[translate]}")
    exit()

if translate in reverse_igbo_words_dict:
    print(f"Here is the translation: {reverse_igbo_words_dict[translate]}")
    exit()

if simple_input in simple_igbo_keys:
    original = simple_igbo_keys[simple_input]
    print(f"Here is the translation: {igbo_words_dict[original]}")
    exit()

if simple_input in reverse_simple_igbo_keys:
    original = reverse_simple_igbo_keys[simple_input]
    print(f"Here is the translation: {reverse_igbo_words_dict[original]}")
    exit()

suggestion_in_igbo = suggest_word(simple_input, simple_igbo_keys.keys())
if suggestion_in_igbo:
    guess = suggestion_in_igbo[0]
    original_igbo = simple_igbo_keys[guess]
    translation = reverse_igbo_words_dict.get(original_igbo)
    if translation:
        print(f"Did you mean '{original_igbo}'? → {translation}")
        exit()

suggestion_in_english = suggest_word(simple_input, reverse_simple_igbo_keys.keys())
if suggestion_in_english:
    guess = suggestion_in_english[0]
    original_eng = reverse_simple_igbo_keys[guess]
    translation = igbo_words_dict.get(original_eng)
    if translation:
        print(f"Did you mean '{original_eng}'? → {translation}")
        exit()

print("Ndo, I couldn't find that word.")



