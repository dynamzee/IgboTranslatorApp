import difflib
from datetime import datetime

def suggest_word(word, all_dictionary):
    suggestion = difflib.get_close_matches(word, all_dictionary, n=1, cutoff=0.7)
    return suggestion[0] if suggestion else None

def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Ututu oma, onye nke anyi. Anyi nabatara gi nnoo nke oma."
    elif hour < 16:
        return "Ehihie oma, onye nke anyi. Anyi nabatara gi nnoo nke oma."
    elif hour < 18:
        return "Mgbede oma, onye nke anyi. Anyi nabatara gi nnoo nke oma."
    else:
        return "Anyasi oma, onye nke anyi. Anyi nabatara gi nnoo nke oma."

