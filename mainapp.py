from flask import Flask, render_template, request, jsonify
from engine.translator import IgboTranslator
from flask_mail import Mail, Message
import os
import threading

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_OWNER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_TIMEOUT'] = 30

mail = Mail(app)

translator = IgboTranslator(paths={
    "all_json": "my_data/igbo_phrases_dict.json",
    "reverse_words_phrases": "my_data/igbo_words_dict.json",
    "simple_keys": "my_data/igbo_phrases_dict.json",
    "reverse_simple_keys": "my_data/igbo_words_dict.json"
})

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            print("GMAIL SUCCESS: Email sent!")
        except Exception as e:
            print(f"GMAIL ERROR: {e}")

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
    admin_email = os.environ.get('EMAIL_OWNER')

    if not original or not user_input:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    msg = Message("New Igbo Translation Suggestion!",
                  sender=admin_email,
                  recipients=[admin_email])
    msg.body = f"Original: {original}\nCorrection: {user_input}"

    thread = threading.Thread(target=send_async_email, args=(app, msg))
    thread.start()

    return jsonify({"status": "success", "message": "Daalu! Suggestion received."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)












