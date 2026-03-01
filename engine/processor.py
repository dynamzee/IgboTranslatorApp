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
        prompt = f"Translate this to natural Igbo, keeping the cultural vibe: {text}. Return ONLY the translation."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Ndo (Sorry), I couldn't reach the AI: {e}"

def translate_hybrid(text, translator_instance):
    result = translator_instance.translate(text)

    if "not found" in result.lower() or result == text:
        return get_ai_fallback(text)

    return result

def suggest_word(word, all_dictionary):
    suggestion = difflib.get_close_matches(word, all_dictionary, n=1, cutoff=0.7)
    return suggestion[0] if suggestion else None


