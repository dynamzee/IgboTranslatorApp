from flask import Flask, render_template, request, jsonify
from engine.translator import IgboTranslator
import os
import requests
import threading

app = Flask(__name__)

translator = IgboTranslator(paths={
    "all_json": "my_data/igbo_phrases_dict.json",
    "reverse_words_phrases": "my_data/igbo_words_dict.json",
    "simple_keys": "my_data/igbo_phrases_dict.json",
    "reverse_simple_keys": "my_data/igbo_words_dict.json"
})

def send_async_email(api_key, domain, admin_email, original, user_input):
    try:
        url = f"https://api.mailgun.net/v3/{domain}/messages"
        auth = ("api", api_key)
        data = {
            "from": f"Translator App <mailgun@{domain}>",
            "to": [admin_email],
            "subject": "New Igbo Translation Suggestion!",
            "text": f"Original: {original}\nCorrection: {user_input}"
        }
        response = requests.post(url, auth=auth, data=data)
        print(f"MAILGUN STATUS: {response.status_code}")
    except Exception as e:
        print(f"MAILGUN ERROR: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.json.get('text', '')
    result = translator.translate(text)
    return jsonify({"translation": result})

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    original = data.get('original')
    user_input = data.get('user_input')

    api_key = os.environ.get('MAILGUN_API_KEY')
    domain = os.environ.get('MAILGUN_DOMAIN')
    admin_email = os.environ.get('EMAIL_OWNER')

    if not original or not user_input:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    thread = threading.Thread(
        target=send_async_email,
        args=(api_key, domain, admin_email, original, user_input)
    )
    thread.start()

    return jsonify({"status": "success", "message": "Daalu! Suggestion received."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)



