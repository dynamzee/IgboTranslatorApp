import json
import os
from datetime import datetime

FEEDBACK_SUGGESTION_FILE = 'engine/community_data.json'

def your_suggestion_or_correction(original_text, user_input, feedback_type="correction"):

    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": feedback_type,
        "original": original_text,
        "provided_by_user": user_input,
        "status": "unreviewed"
    }

    if os.path.exists(FEEDBACK_SUGGESTION_FILE):
        try:
            with open(FEEDBACK_SUGGESTION_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    data.append(entry)

    with open(FEEDBACK_SUGGESTION_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return True

