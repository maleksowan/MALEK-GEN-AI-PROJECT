🎓 Student FAQ Chatbot — Python + Flask + OpenAI (Demo)

A small Generative AI backend project:

Backend: Python (Flask)

Frontend: HTML + CSS + JS (single-page web UI)

Chatbot: server-side call to OpenAI Chat Completions API

Knowledge base: local text file (FAQs)

Logging & analysis: CSV + Pandas + Matplotlib

1) Requirements

Python 3.10+

pip (Python package manager)

Internet connection (OpenAI API)

Python libraries:

flask, flask-cors

openai

python-dotenv

pandas, matplotlib

2) Setup (local)

Clone the repository

Create virtual environment and activate it

Install dependencies:

pip install -r requirements.txt

Copy env file:

Copy .env.example → .env

Put your OpenAI API key in .env

IMPORTANT: keep your OpenAI key server-side
Never expose it in HTML or JavaScript.

3) Run

Start the Flask server:

python app.py

Open in browser:

http://127.0.0.1:5000

4) Pages & API

/ → Student FAQ Chatbot UI

/chat → chatbot API endpoint (POST)

Example request:
{ "question": "What is the attendance policy?" }

Notes

The chatbot answers only based on the provided knowledge base.

Questions outside the knowledge base are politely rejected.

All interactions are logged for evaluation and analysis.

The system demonstrates agent-like behaviour through controlled retrieval.