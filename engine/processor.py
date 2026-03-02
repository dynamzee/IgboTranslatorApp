import difflib
from datetime import datetime
import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

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


def get_ai_fallback(text):
    try:
        prompt = f"Translate the following English text into a full, natural Igbo sentence: '{text}'. Output ONLY the Igbo translation."
        response = model.generate_content(prompt)
        translated_text = response.text.strip()
        return translated_text if len(translated_text) > 2 else "Ndo, I couldn't translate that properly."
    except Exception as e:
        return f"Ndo (Sorry), I couldn't reach the AI: {e}"


def translate_hybrid(text, translator_instance):
    result = translator_instance.translate(text)

    if not result or result.strip() == text.strip() or "not found" in result.lower():
        print(f"DEBUG: JSON failed for '{text}', calling Gemini...")  # Check Render logs for this!
        return get_ai_fallback(text)

    return result

def suggest_word(word, all_dictionary):
    suggestion = difflib.get_close_matches(word, all_dictionary, n=1, cutoff=0.7)
    return suggestion[0] if suggestion else None


