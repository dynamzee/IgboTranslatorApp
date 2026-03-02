import difflib
from datetime import datetime
from google import genai
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

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
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"Translate to sharp, natural Igbo: '{text}'. Return ONLY the translation."
        )
        if response and response.text:
            return response.text.strip()
        return "Ndo, API returned no text."
    except Exception as e:
        return f"API Error: {str(e)[:50]}"

def translate_hybrid(text, translator_instance):
    result = translator_instance.translate(text)

    if not result or result.strip() == text.strip() or "not found" in result.lower():
        return get_ai_fallback(text)

    return result

def suggest_word(word, all_dictionary):
    suggestion = difflib.get_close_matches(word, all_dictionary, n=1, cutoff=0.95)
    return suggestion[0] if suggestion else None


