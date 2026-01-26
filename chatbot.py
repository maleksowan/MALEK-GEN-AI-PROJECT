import os
import csv
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

# Load local knowledge base
def load_knowledge_base():
    with open("knowledge_base.txt", "r", encoding="utf-8") as file:
        return file.read()

KNOWLEDGE_BASE = load_knowledge_base()

# Initialize log file
LOG_FILE = "interaction_logs.csv"

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "user_question", "ai_answer"])

print("🎓 Student FAQ Chatbot")
print("Type 'exit' to quit.\n")

# Chat loop
while True:
    user_question = input("You: ")

    if user_question.lower() == "exit":
        print("Goodbye!")
        break

    prompt = f"""
You are a helpful university assistant.
Answer the user's question strictly using the information provided below.
If the answer is not found in the information, say:
"I can only answer questions based on the provided university information."

University Information:
{KNOWLEDGE_BASE}

Question:
{user_question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a factual university assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    answer = response.choices[0].message.content.strip()

    print(f"\nBot: {answer}\n")

    # Log interaction
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            user_question,
            answer
        ])
