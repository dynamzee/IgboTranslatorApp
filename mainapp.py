from flask import Flask, render_template, request, jsonify
from engine.translator import IgboTranslator
from engine.processor import get_greeting, translate_hybrid
import os
import requests
import threading

app = Flask(__name__)

translator = IgboTranslator()

def send_to_slack(original, user_input):
    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    if not webhook_url:
        print("ERROR: SLACK_WEBHOOK_URL WASN'T FOUND IN RENDER!")
        return

    payload = {
        "text": f"🚨 *FEEDBACK_CORRECTION_SUGGESTION!*\n*text_in_place:* {original}\n*info_from_user:* {user_input}"
    }

    try:
        response = requests.post(webhook_url, json=payload)
        print(f"SLACK STATUS: {response.status_code}")
    except Exception as e:
        print(f"SLACK ERROR: {e}")

@app.route('/')
def index():
    greeting = get_greeting()
    return render_template('index.html', greeting=greeting)

@app.route('/translate', methods=['POST'])
def translate():
    text = request.json.get('text', '')
    result = translate_hybrid(text, translator)
    return jsonify({"translation": result})

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    original = data.get('original')
    user_input = data.get('user_input')

    if not original or not user_input:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    thread = threading.Thread(target=send_to_slack, args=(original, user_input))
    thread.start()

    return jsonify({"status": "success", "message": "Daalu!😊 Your suggestion has been sent!."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)




