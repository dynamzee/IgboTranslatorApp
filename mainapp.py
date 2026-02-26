from flask import Flask, render_template, request, jsonify
from engine.translator import IgboTranslator
from engine.suggestion_feedback import your_suggestion_or_correction

app = Flask(__name__)

translator = IgboTranslator(paths={
    "all_json": "my_data/igbo_phrases_dict.json",
    "reverse_words_phrases": "my_data/igbo_words_dict.json",
    "simple_keys": "my_data/igbo_phrases_dict.json",
    "reverse_simple_keys": "my_data/igbo_words_dict.json"
})


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
    your_suggestion_or_correction(
        data['original'],
        data['user_input'],
        data.get('type', 'correction')
    )
    return jsonify({"status": "success", "message": "Daalu!"})


if __name__ == '__main__':
    app.run(debug=True)


