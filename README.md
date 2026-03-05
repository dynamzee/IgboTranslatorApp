DYNA's TRANSLATOR APP is a full-stack English-to-Igbo translation platform built to preserve and promote the Igbo language. This isn't just a "find and replace" tool; it’s a culturally aware application that greets users natively based on the time of day and invites them to be part of the language-building process.

**Special Features:**
 Time-Based Cultural Greetings: Dynamically welcomes users with time-appropriate Igbo greetings (Ututu oma, Ehihie oma, Mgbede oma, Anyasi oma).

 Hybrid AI Translation Engine: The app first consults custom JSON dictionaries created by me for 100% cultural accuracy. If a match isn't found, it seamlessly fails over to the gemini-2.5-flash API to provide a natural, conversational translation.

 Real-Time Slack Feedback Loop: Integrated with Slack Webhooks and Python threading to receive users' suggestions, feedbacks and corrections instantly on mobile without slowing down the UI.

 Mobile-Optimized Interface: A custom standard CSS layout designed for a seamless, full-screen experience on both iPhone and Android devices.

 Intelligent Suggestion Engine: Uses fuzzy string matching to help users find the right words even when they make typos.

## APP/SLACK NOTIFICATION SCREENSHOT:

|       Translator App Screenshot        |                 Slack Notification Screenshot                 |
|:--------------------------------------:|:-------------------------------------------------------------:|
| ![App Screenshot](app_screenshot.jpeg) | ![Slack Notification Screenshot](slack_notis_screenshot.jpeg) |

> **NOTE:**: The screenshot on the left shows my app user interface, while the right shows the "swift" feedback loop in my dedicated `#backend-development\dyna_translator_app` channel.

  **The Technical Stack:**
Building this required overcoming significant some challenges, including system-level configurations.

Core Technologies:
Backend: Python (Flask) | Frontend & Styling: HTML and CSS.

NLP & AI (Google Gemini):
google-generativeai: Powering the Gemini-2.5-flash fallback engine.

spacy: For advanced language processing.

difflib: For the suggest_word (did you mean?) fuzzy matching logic.

unicodedata: For handling Igbo diacritics and character normalization.

Infrastructure: Hosted on Render with environment variable security for API keys: (GEMINI_API_KEY, SLACK_WEBHOOK_URL) and also secret files for my custom JSON dictionaries.

Microsoft VisualStudioSetup for spaCy:
Windows C++ Build Tools: To get spacy running locally, I had to navigate the complex installation of Microsoft Visual C++ Redistributables, ensuring the system could compile the necessary language headers.

Asynchronous Operations: Implemented threading to handle Slack notifications as background tasks, ensuring the app remains swift.

Clean Data Architecture: Managed custom JSON dictionaries for phrases and reverse-word lookups.

Hybrid Logic: Developed a custom priority-based translation flow: custom json dictionaries → fuzzy matching → AI fallback.

 Why this matters to me?
Igbo Language is my heritage, and I'm aiming to promote the culture in the way I can by building this translator app that embodies me and also getting to know how translator apps works.

 A nabatara m unu nnoo nke oma. (You are very welcome.)













