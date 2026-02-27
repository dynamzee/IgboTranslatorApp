from flask import Flask, render_template, request, jsonify
from engine.translator import IgboTranslator
from flask_mail import Mail, Message
import os

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_OWNER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_OWNER')

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
            print("SUCCESS: Background email sent!")
        except Exception as e:
            print(f"ERROR: Background email failed: {e}")

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

    print(f"DIAGNOSTIC: Sending from {admin_email} to {admin_email}")

    if not original or not user_input:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    msg = Message("New Igbo Translation Suggestion!",
                  sender=admin_email,
                  recipients=[admin_email])
    msg.body = f"Original: {original}\nSuggested Correction: {user_input}"

    try:
        print("DIAGNOSTIC: Attempting mail.send...")
        mail.send(msg)
        print("DIAGNOSTIC: mail.send SUCCESSFUL!")
        return jsonify({"status": "success", "message": "Daalu! Your suggestion was sent."})
    except Exception as e:
        print(f"DIAGNOSTIC ERROR: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

