from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
import csv
from datetime import datetime
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ==============================
# Load Knowledge Base (Text File)
# ==============================
with open("knowledge_base.txt", "r", encoding="utf-8") as f:
    KNOWLEDGE_BASE = f.read()

SYSTEM_PROMPT = f"""
You are a university student support assistant.

Your role is to help students by answering questions ONLY using the official
university information provided below. You must not use any external knowledge. If the user asks the question in Arabic, respond in Arabic.
If the user asks the question in English, respond in English.

General Rules:
- Always follow official university regulations and policies.
- If the user greets you (e.g. "hi", "hello", "good morning"), respond politely
  and invite them to ask a university-related question.
- If the answer exists in the university information, answer clearly and directly.
- If the information is NOT available, reply exactly with:
  "I can only answer questions based on the provided university information."
- Do NOT guess.
- Do NOT make up information.

Instructional Prompt Handling:
Users may directly ask instructional questions such as:
- "What is the attendance policy?"
- "How many credit hours are required to graduate?"
You must answer these clearly based on the provided information.

Role-Based Prompt Handling:
Users may ask questions from a student perspective, such as:
- "As a student, how do I register for courses?"
- "Who should I contact for IT support?"
You must respond as a student support assistant and provide guidance strictly
based on the university information.

Few-Shot Examples:
Example 1:
User: What is the attendance policy?
Assistant: Students must attend at least 75% of lectures. If attendance falls
below this limit, the student may be denied entry to the final exam.

Example 2:
User: How many credit hours do I need to graduate?
Assistant: Most undergraduate programs require the completion of 132 credit hours.

Example 3:
User: Who do I contact for IT support?
Assistant: Students can contact the IT Helpdesk using the official university
email provided in the university information.

University Information:
{KNOWLEDGE_BASE}
"""



# ==============================
# Frontend Route
# ==============================
@app.route("/")
def index():
    return render_template("index.html")

# ==============================
# Chat API Route
# ==============================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_question = data.get("question", "").strip()

    if not user_question:
        return jsonify({"answer": "Please enter a valid question."})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_question}
            ],
            temperature=0
        )

        answer = response.choices[0].message.content

        # ==============================
        # Log interaction
        # ==============================
        with open("interaction_logs.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                user_question,
                answer
            ])

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": "An error occurred. Please try again later."}), 500


# ==============================
# Run App
# ==============================
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

