
from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

questions = [
    {
        "id": 1,
        "question": "What is the greatest common factor of 12 and 15?",
        "answer": "3",
        "explanation": "Factors of 12: 1, 2, 3, 4, 6, 12. Factors of 15: 1, 3, 5, 15. GCF = 3.",
        "choices": ["1", "2", "3", "4"]
        
    }
]

@app.route("/")
def index():
    return render_template("game.html", questions=questions)

@app.route("/check", methods=["POST"])
def check():
    data = request.json
    score = 0
    feedback = []

    for q in questions:
        user_answer = data.get(str(q["id"]), "").strip()
        correct = q["answer"]

        if user_answer == correct:
            score += 10
        else:
            feedback.append({
                "question": q["question"],
                "your_answer": user_answer,
                "correct_answer": correct,
                "explanation": q["explanation"]
            })

    return jsonify({
        "score": score,
        "feedback": feedback
    })

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

levels = {
    "Level 1": {
        "badge": "🐢 Number Explorer",
        "questions": [
            {
                "id": 1,
                "section": "A",
                "question": "Find the square root of 81",
                "choices": ["7", "8", "9", "6"],
                "answer": "9",
                "explanation": "9 × 9 = 81, therefore √81 = 9."
            },
            {
                "id": 2,
                "section": "B",
                "question": "Find the LCM of 6 and 8",
                "answer": "24",
                "explanation": "Multiples of 6: 6,12,18,24. Multiples of 8: 8,16,24. LCM = 24."
            }
        ]
    },
    "Level 2": {
        "badge": "🦈 Algebra Warrior",
        "questions": [
            {
                "id": 3,
                "section": "A",
                "question": "Solve: x + 7 = 15",
                "choices": ["6", "7", "8", "9"],
                "answer": "8",
                "explanation": "x + 7 = 15 → x = 15 − 7 = 8."
            }
        ]
    }
}

@app.route("/")
def index():
    return render_template("game.html", levels=levels)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    score = 0
    lives = 3
    feedback = []
    badges = []

    for level_name, level in levels.items():
        correct_count = 0

        for q in level["questions"]:
            user_answer = data.get(str(q["id"]), "").strip()

            if user_answer == q["answer"]:
                score += 10
                correct_count += 1
            else:
                lives -= 1
                feedback.append({
                    "question": q["question"],
                    "your_answer": user_answer,
                    "correct_answer": q["answer"],
                    "explanation": q["explanation"]
                })

        if correct_count == len(level["questions"]):
            badges.append(level["badge"])

    return jsonify({
        "score": score,
        "lives": lives,
        "badges": badges,
        "feedback": feedback
    })

if __name__ == "__main__":
    app.run(debug=True)
boss_questions = {
    "Level 1": {
        "question": "A number is divisible by both 6 and 9. What is the smallest such number?",
        "answer": "18",
        "explanation": (
            "Find LCM of 6 and 9."
            "6 = 2 * 3"
            "9 = 3 * 3"
            "LCM = 2 * 3 * 3 = 18"
        )
    },
    "Level 2": {
        "question": "Solve: 3(2x - 4) = 18",
        "answer": "5",
        "explanation": (
            "Expand: 6x - 12 = 18"
            "6x = 30"
            "x = 5"
        )
    }
}
@app.route("/boss", methods=["POST"])
def boss():
    data = request.json
    level = data["level"]
    user_answer = data["answer"]

    boss = boss_questions[level]

    if user_answer == boss["answer"]:
        return jsonify({
            "success": True,
            "points": 30
        })
    else:
        return jsonify({
            "success": False,
            "explanation": boss["explanation"]
        })
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

questions = [
    # -------- SECTION A (MCQs) --------
    {
        "id": 1,
        "section": "A",
        "question": "What is the square root of 144?",
        "choices": ["10", "11", "12", "14"],
        "answer": "12",
        "explanation": "12 * 12 = 144, therefore √144 = 12."
    },
    {
        "id": 2,
        "section": "A",
        "question": "Which of the following is a prime number?",
        "choices": ["21", "15", "17", "27"],
        "answer": "17",
        "explanation": "17 has only two factors: 1 and 17."
    },

    # -------- SECTION B (OPEN QUESTIONS) --------
    {
        "id": 3,
        "section": "B",
        "question": "Solve: 2x + 6 = 14",
        "answer": "4",
        "explanation": "2x + 6 = 14 → 2x = 8 → x = 4."
    }
]

boss_question = {
    "question": "Find the LCM of 6 and 9",
    "answer": "18",
    "explanation": (
        "6 = 2 * 3\n"
        "9 = 3 * 3\n"
        "LCM = 2 * 3 * 3 = 18"
    )
}

@app.route("/")
def index():
    return render_template("game.html", questions=questions)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    score = 0
    feedback = []

    for q in questions:
        user_answer = data.get(str(q["id"]), "").strip()
        if user_answer == q["answer"]:
            score += 10
        else:
            feedback.append({
                "question": q["question"],
                "your_answer": user_answer,
                "correct_answer": q["answer"],
                "explanation": q["explanation"]
            })

    return jsonify({
        "score": score,
        "feedback": feedback
    })

@app.route("/boss", methods=["POST"])
def boss():
    data = request.json
    if data["answer"] == boss_question["answer"]:
        return jsonify({"success": True, "points": 30})
    else:
        return jsonify({
            "success": False,
            "explanation": boss_question["explanation"]
        })

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("front end.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    return jsonify({"status": "received", "data": data})

questions = [
    {"id": 1, "q": "2 + 3", "a": "5"},
    {"id": 2, "q": "4 * 2", "a": "8"}
]

@app.route("/")
def home():
    return render_template("front end.html", questions=questions)

if __name__ == "__main__":
    app.run(debug=True)


