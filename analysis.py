import pandas as pd
import matplotlib.pyplot as plt

# =========================
# Load interaction logs
# =========================
df = pd.read_csv("interaction_logs.csv")

# Basic cleaning
df.dropna(inplace=True)

# Rename columns (best practice)
df.rename(columns={
    "user_question": "question",
    "ai_answer": "answer"
}, inplace=True)

# =========================
# Improved Question Classification
# =========================
def classify_question(q):
    q = q.lower()

    if any(word in q for word in ["attendance", "attend", "lecture"]):
        return "Attendance"

    elif any(word in q for word in ["credit", "hour", "graduate"]):
        return "Credits"

    elif any(word in q for word in ["exam", "final", "midterm"]):
        return "Exams"

    elif any(word in q for word in ["grade", "grading", "gpa"]):
        return "Grading"

    elif any(word in q for word in ["register", "registration", "enroll"]):
        return "Registration"

    elif any(word in q for word in ["elearning", "portal", "password"]):
        return "eLearning"

    elif any(word in q for word in ["contact", "email", "phone", "office", "administration"]):
        return "University Info"

    elif any(word in q for word in ["hi", "hello", "hey"]):
        return "Greeting"

    else:
        return "Other"

df["question_type"] = df["question"].apply(classify_question)

# =========================
# 📊 Visualization 1: Question Type Frequency
# =========================
plt.figure()
df["question_type"].value_counts().plot(kind="bar")
plt.title("Frequency of Question Types")
plt.xlabel("Question Type")
plt.ylabel("Number of Questions")
plt.tight_layout()
plt.show()

# =========================
# 📊 Visualization 2: Answered vs Not Answered
# =========================
df["answer_status"] = df["answer"].apply(
    lambda x: "Not Answered"
    if "only answer questions based" in x.lower()
    else "Answered"
)

plt.figure()
df["answer_status"].value_counts().plot(
    kind="pie", autopct="%1.1f%%"
)
plt.title("Answered vs Unanswered Questions")
plt.ylabel("")
plt.tight_layout()
plt.show()
