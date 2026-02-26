from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
import random
import subprocess
import requests

QUESTIONS_FILE = "questions.json"

app = Flask(__name__)
app.secret_key = "secret123"

DB_FILE = "user_database.json"

# ----------------- USER DATABASE FUNCTIONS -----------------

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ----------------- Math-QUESTIONS -----------------


MathQUESTIONS = {
    "7": {   # ← Grade 7 questions only
        "Integers": [
            {
                "question": "What is -5 + 8?",
                "choices": ["3", "-3", "13", "-13"],
                "answer": "3",
                "explanation": "Subtract 5 from 8 and keep the sign of the bigger number."
            },
            {
                "question": "What is -3 x 4?",
                "choices": ["-12", "12", "-7", "7"],   
                "answer": "-12",
                "explanation": "Negative times positive gives a negative result."
            }
        ],
        "Fractions": [
            {
                "question": "What is 3/4 + 1/4?",
                "choices": ["1", "3/8", "4/8", "2"],
                "answer": "1",
                "explanation": "Same denominator: 4/4 = 1."
            },
            {
                "question": "What is 1/2 * 1/3?",
                "choices": ["1/6", "1/5", "1/3", "1/2"],
                "answer": "1/6",
                "explanation": "Multiply numerators and denominators: (1*1)/(2*3) = 1/6."
            }
        ],
        "Decimals": [
            {
                "question": "What is 0.5 + 0.25?",
                "choices": ["0.75", "0.85", "1.0", "0.65"],
                "answer": "0.75",
                "explanation": "Add the decimal values directly."
            },
            {
                "question": "What is 0.6 * 0.2?",
                "choices": ["0.12", "0.02", "0.8", "0.3"],
                "answer": "0.12",
                "explanation": "Multiply the decimal values directly."
            }
        ],
        "square and square roots": [
            {
                "question": "find the square of 182",
                "choices": ["33124", "33124", "33124", "33124"],
                "answer": "33124",
                "explanation": "182 * 182 = 33124."
            },
            {
                "question": "find the square root of 182",
                "choices": ["13.49", "12.49", "14.49", "15.49"],
                "answer": "13.49",
                "explanation": "The square root of 182 is approximately 13.49."
            }
        ],
        "Algebra": [
            {
                "question": "Solve for x: 2x + 3 = 7",
                "choices": ["x = 2", "x = 5", "x = 1", "x = 3"],
                "answer": "x = 2",
                "explanation": "Subtract 3 then divide by 2."
            },
            {
                "question": "The length of a rectangle is 3p-4 and width is p+ 24. Find the area and perimeter of the rectangle",
                "choices": ["Area: 3p^2 + 68p - 96, Perimeter: 8p + 40", "Area: 3p^2 + 68p - 96, Perimeter: 6p + 20", "Area: 3p^2 + 68p - 96, Perimeter: 6p + 40", "Area: 3p^2 + 68p - 96, Perimeter: 8p + 20"],
                "answer": "Area: 3p^2 + 68p - 96, Perimeter: 8p + 40",
                "explanation": "Area = length * width, Perimeter = 2(length +   width)."
            },
            {
                "question": "The sides of a tringle are 2x + 3, x - 1, and 3x - 2. If the perimeter is 24, find the value of x.",
                "choices": ["x = 5", "x = 4", "x = 6", "x = 3"],
                "answer": "x = 5",
                "explanation": "Set up the equation: (2x + 3) + (x - 1) + (3x - 2) = 24, then solve for x."
            }
                     
        ],
        "Measurement":[
            {
                "question": "Convert 5 kilometers to meters.",
                "choices": ["5000 meters", "500 meters", "50 meters", "0.5 meters"],
                "answer": "5000 meters",
                "explanation": "1 kilometer = 1000 meters, so 5 kilometers = 5 * 1000 = 5000 meters."
            },
            {
                "question": "Convert 2500 milliliters to liters.",
                "choices": ["2.5 liters", "25 liters", "0.25 liters", "250 liters"],
                "answer": "2.5 liters",
                "explanation": "1 liter = 1000 milliliters, so 2500 milliliters = 2500 / 1000 = 2.5 liters."
            },
            {
                "question": "Convert 3 hours to minutes.",
                "choices": ["180 minutes", "30 minutes", "300 minutes", "60 minutes"],
                "answer": "180 minutes",
                "explanation": "1 hour = 60 minutes, so 3 hours = 3 * 60 = 180 minutes."
            },
            {
                "question": "if the length of a triangle is 5cm and the width is 12cm, find the area of the triangle",
                "choices": ["30 cm²", "60 cm²", "90 cm²", "120 cm²"],
                "answer": "30 cm²",
                "explanation": "Area of a triangle = (base * height) / 2, so Area = (5 cm * 12 cm) / 2 = 30 cm²."
            },
            {
                "question": " find the area the parallelogram if the diagonal is 16cm and length is 10cm",
                "choices": ["80 cm²", "160 cm²", "40 cm²", "20 cm²"],
                "answer": "80 cm²",
                "explanation": "Area of a parallelogram = base * height. If the diagonal is 16 cm and the length is 10 cm, assuming the height is 8 cm (from Pythagorean theorem), then Area = 10 cm * 8 cm = 80 cm²."
            }
        ]
    },

    "8": {
    "Integers": [
        {
            "question": "What is -12 + 5?",
            "choices": ["-7", "7", "-17", "17"],
            "answer": "-7",
            "explanation": "Adding 5 to -12 moves 5 steps toward zero: -7."
        },
        {
            "question": "What is (-4) × (-6)?",
            "choices": ["-24", "24", "-10", "10"],
            "answer": "24",
            "explanation": "Negative times negative gives a positive."
        }
    ],
    "Fractions": [
        {
            "question": "What is 2/3 + 1/6?",
            "choices": ["5/6", "3/9", "1/2", "2/9"],
            "answer": "5/6",
            "explanation": "Convert to same denominator: 2/3 = 4/6, so 4/6 + 1/6 = 5/6."
        },
        {
            "question": "What is 3/5 ÷ 1/2?",
            "choices": ["6/5", "3/10", "5/6", "1/5"],
            "answer": "6/5",
            "explanation": "Dividing by 1/2 is the same as multiplying by 2: 3/5 × 2 = 6/5."
        }
    ],
    "Decimals": [
        {
            "question": "What is 1.2 + 0.35?",
            "choices": ["1.55", "1.45", "1.25", "1.65"],
            "answer": "1.55",
            "explanation": "Line up decimals and add: 1.20 + 0.35 = 1.55."
        },
        {
            "question": "What is 0.8 × 0.5?",
            "choices": ["0.4", "4", "0.05", "0.8"],
            "answer": "0.4",
            "explanation": "Multiply normally: 8 × 5 = 40, then place decimals → 0.4."
        }
    ],
    "Squares and Square Roots": [
        {
            "question": "What is the square of 15?",
            "choices": ["225", "30", "45", "215"],
            "answer": "225",
            "explanation": "15 × 15 = 225."
        },
        {
            "question": "What is √144?",
            "choices": ["10", "11", "12", "14"],
            "answer": "12",
            "explanation": "12 × 12 = 144."
        }
    ],
    "Algebra": [
        {
            "question": "Solve for x: 3x + 5 = 20",
            "choices": ["x = 5", "x = 3", "x = 15", "x = 10"],
            "answer": "x = 5",
            "explanation": "Subtract 5: 3x = 15, then divide by 3: x = 5."
        },
        {
            "question": "Simplify: 2x + 3x - x",
            "choices": ["4x", "6x", "5x", "3x"],
            "answer": "4x",
            "explanation": "2x + 3x - x = (2 + 3 - 1)x = 4x."
        }
    ],
    "Measurement": [
        {
            "question": "Convert 2.5 km to meters.",
            "choices": ["2500 m", "25 m", "250 m", "25000 m"],
            "answer": "2500 m",
            "explanation": "1 km = 1000 m, so 2.5 × 1000 = 2500 m."
        },
        {
            "question": "Find the area of a rectangle with length 8 cm and width 5 cm.",
            "choices": ["40 cm²", "26 cm²", "13 cm²", "80 cm²"],
            "answer": "40 cm²",
            "explanation": "Area = length * width = 8 * 5 = 40 cm²."
        }
    ]
},

"9": {
    "Integers": [
        {
            "question": "What is -18 ÷ 3?",
            "choices": ["-6", "6", "-15", "15"],
            "answer": "-6",
            "explanation": "Negative divided by positive is negative: -18 ÷ 3 = -6."
        },
        {
            "question": "What is -7 - (-10)?",
            "choices": ["3", "-17", "-3", "17"],
            "answer": "3",
            "explanation": "Subtracting a negative is adding: -7 + 10 = 3."
        }
    ],
    "Fractions": [
        {
            "question": "What is 5/6 - 1/3?",
            "choices": ["1/2", "4/6", "2/3", "1/3"],
            "answer": "1/2",
            "explanation": "1/3 = 2/6, so 5/6 - 2/6 = 3/6 = 1/2."
        },
        {
            "question": "What is 4/5 * 10?",
            "choices": ["8", "2", "40", "5"],
            "answer": "8",
            "explanation": "4/5 * 10 = 40/5 = 8."
        }
    ],
    "Decimals": [
        {
            "question": "What is 2.4 ÷ 0.6?",
            "choices": ["4", "0.4", "1.8", "3"],
            "answer": "4",
            "explanation": "2.4 ÷ 0.6 = 24 ÷ 6 = 4."
        },
        {
            "question": "What is 1.75 + 2.5?",
            "choices": ["4.25", "3.25", "4.15", "3.75"],
            "answer": "4.25",
            "explanation": "1.75 + 2.50 = 4.25."
        }
    ],
    "Squares and Square Roots": [
        {
            "question": "What is the square of 20?",
            "choices": ["400", "40", "200", "800"],
            "answer": "400",
            "explanation": "20 * 20 = 400."
        },
        {
            "question": "What is √225?",
            "choices": ["15", "14", "25", "10"],
            "answer": "15",
            "explanation": "15 * 15 = 225."
        }
    ],
    "Algebra": [
        {
            "question": "Solve for x: 5x - 10 = 15",
            "choices": ["x = 5", "x = 3", "x = 25", "x = 1"],
            "answer": "x = 5",
            "explanation": "Add 10: 5x = 25, divide by 5: x = 5."
        },
        {
            "question": "Expand: (x + 3)(x + 2)",
            "choices": ["x² + 5x + 6", "x² + 6x + 5", "x² + 5x + 5", "x² + x + 6"],
            "answer": "x² + 5x + 6",
            "explanation": "FOIL: x² + 2x + 3x + 6 = x² + 5x + 6."
        }
    ],
    "Measurement": [
        {
            "question": "Find the area of a triangle with base 10 cm and height 6 cm.",
            "choices": ["30 cm²", "60 cm²", "16 cm²", "20 cm²"],
            "answer": "30 cm²",
            "explanation": "Area = 1/2 * base * height = 1/2 * 10 * 6 = 30."
        },
        {
            "question": "Convert 3.5 liters to milliliters.",
            "choices": ["3500 ml", "35 ml", "300 ml", "350 ml"],
            "answer": "3500 ml",
            "explanation": "1 liter = 1000 ml, so 3.5 * 1000 = 3500 ml."
        }
    ]
}

}
print("MathQUESTIONS loaded:", MathQUESTIONS.keys())



Pre_techQuestions = {
    "7": {
    "Workshop Safety": [
        {
            "question": "What is workshop safety?",
            "choices": [
                "Observing rules to prevent accidents",
                "Working without supervision",
                "Using tools quickly",
                "Avoiding all machines"
            ],
            "answer": "Observing rules to prevent accidents",
            "explanation": "Workshop safety involves following rules and precautions to prevent injuries."
        },
        {
            "question": "Which of the following is personal protective equipment (PPE)?",
            "choices": [
                "Goggles",
                "Notebook",
                "Chair",
                "Ruler"
            ],
            "answer": "Goggles",
            "explanation": "Goggles protect the eyes from dust and flying particles."
        }
    ],

    "Tools and Equipment": [
        {
            "question": "What is the function of a claw hammer?",
            "choices": [
                "Driving and removing nails",
                "Measuring length",
                "Cutting metal",
                "Holding wood"
            ],
            "answer": "Driving and removing nails",
            "explanation": "A claw hammer is used to drive nails in and pull them out."
        },
        {
            "question": "Which tool is used to check a right angle?",
            "choices": [
                "Try square",
                "Spanner",
                "File",
                "Chisel"
            ],
            "answer": "Try square",
            "explanation": "A try square checks 90° angles."
        }
    ],

    "Materials Technology": [
        {
            "question": "What is seasoning of timber?",
            "choices": [
                "Drying timber to remove moisture",
                "Painting timber",
                "Burning timber",
                "Polishing timber"
            ],
            "answer": "Drying timber to remove moisture",
            "explanation": "Seasoning removes moisture to make timber stronger and more durable."
        },
        {
            "question": "Which metal is lightweight and resists corrosion?",
            "choices": [
                "Aluminium",
                "Iron",
                "Steel",
                "Copper"
            ],
            "answer": "Aluminium",
            "explanation": "Aluminium is light and does not rust easily."
        }
    ],

    "Technical Drawing": [
        {
            "question": "What is a T-square used for?",
            "choices": [
                "Drawing horizontal lines",
                "Cutting paper",
                "Measuring angles",
                "Sharpening pencils"
            ],
            "answer": "Drawing horizontal lines",
            "explanation": "A T-square helps draw straight horizontal lines."
        },
        {
            "question": "What does a 1:2 scale mean?",
            "choices": [
                "Drawing is half the real size",
                "Drawing is double the real size",
                "Drawing equals real size",
                "Drawing is one-fourth size"
            ],
            "answer": "Drawing is half the real size",
            "explanation": "1:2 means the drawing is reduced to half the actual size."
        }
    ],

    "Basic Electricity": [
        {
            "question": "Which material is a conductor of electricity?",
            "choices": [
                "Copper",
                "Rubber",
                "Plastic",
                "Wood"
            ],
            "answer": "Copper",
            "explanation": "Copper allows electric current to pass through easily."
        },
        {
            "question": "What is the function of a fuse?",
            "choices": [
                "Protect appliances from excess current",
                "Store electricity",
                "Increase voltage",
                "Light a bulb"
            ],
            "answer": "Protect appliances from excess current",
            "explanation": "A fuse melts when current is too high to prevent damage."
        }
    ],

    "Entrepreneurship": [
        {
            "question": "Who is an entrepreneur?",
            "choices": [
                "A person who starts and runs a business",
                "A teacher",
                "A customer",
                "An employee only"
            ],
            "answer": "A person who starts and runs a business",
            "explanation": "An entrepreneur creates and manages a business."
        },
        {
            "question": "What is profit?",
            "choices": [
                "Money gained after expenses",
                "Money lost",
                "Total sales only",
                "Money borrowed"
            ],
            "answer": "Money gained after expenses",
            "explanation": "Profit is what remains after subtracting expenses from income."
        }
    ]
}
}

# ----------------- LOGIN -----------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = load_users()
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["user"] = username
            session["grade"] = users[username]["grade"]
            session["score"] = 0
            session["points"] = 0
            session["level"] = 1
            return redirect(url_for("dashboard"))

        return render_template("login.html", error="Wrong username or password")

    return render_template("login.html")

# ----------------- REGISTER -----------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users = load_users()
        username = request.form["username"]
        password = request.form["password"]
        grade = request.form["grade"]
        level = 1

        if username in users:
            return render_template("register.html", error="Username already exists")

        users[username] = {"password": password, "grade": grade, "level": level}
        save_users(users)

        return redirect(url_for("login"))

    return render_template("register.html")

# ----------------- DASHBOARD -----------------

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    points = session.get("points", 0)
    score = session.get("score", 0)
    level = points // 100 + 1

    return render_template(
        "dashboard.html",
        username=session.get("user"),
        grade=session.get("grade"),
        score=score,
        points=points,
        level=level
    )

# ----------------- ADD POINTS (AJAX) -----------------

@app.route("/add_points", methods=["POST"])
def add_points():
    data = request.json
    add = data.get("points", 0)
    session["points"] = session.get("points", 0) + add
    return jsonify({"points": session["points"]})

# ================================ MATH MAIN PAGE ========================================

@app.route("/math")
def math_page():
    if "user" not in session:
        return redirect(url_for("login"))

    grade = session.get("grade")
    topics = MathQUESTIONS.get(grade, {}).keys()

    return render_template(
        "math.html",
        grade=grade,
        topics=topics
    )

# ----------------- MATH TOPICS PAGE -----------------

@app.route("/math/<grade>/topics")
def math_topics(grade):
    if "user" not in session:
        return redirect(url_for("login"))

    # Make sure grade is string
    grade = str(grade)

    if grade not in MathQUESTIONS:
        return "Grade not found", 404

    topics = list(MathQUESTIONS[grade].keys())

    return render_template(
        "math.html",
        grade=grade,
        topics=topics
    )




# ----------------- MATH PRACTICE PAGE -----------------

@app.route("/mathpractice/<grade>/<topic>")
def math_practice(grade, topic):

    if "user" not in session:
        return redirect(url_for("login"))

    topic_questions = MathQUESTIONS.get(str(grade), {}).get(topic, [])

    if not topic_questions:
        return "No questions found for this topic", 404

    # Reset session score when entering topic
    session["score"] = 0

    return render_template(
        "mathpractice.html",
        grade=grade,
        topic=topic
    )

@app.route("/mathpractice/<grade>/<topic>/get_question")
def get_math_question(grade, topic):

    fetch_external_patterns(topic)
    skill = random.choice(list(QUESTION_BLUEPRINT.keys()))
    question = generate_question_from_skill(skill)

    return jsonify(question)



# ----------------- GET RANDOM QUESTION (AJAX) -----------------

@app.route("/mathpractice/<grade>/<topic>/get_question")
def get_math_question(grade, topic):

    topic_questions = MathQUESTIONS.get(str(grade), {}).get(topic, [])

    if not topic_questions:
        return jsonify({"error": "No questions found"}), 404
    question = random.choice(topic_questions)

    return jsonify({
        "question": question["question"],
        "choices": question["choices"],
        "answer": question["answer"],
        "explanation": question.get("explanation", ""),
        "topic": topic
    })


# ----------------- FINISH TEST -----------------

@app.route("/mathpractice/<grade>/<topic>/finish", methods=["POST"])
def finish_test(grade, topic):

    data = request.get_json()
    percent = data.get("percent", 0)

    passed = percent >= 70

    return jsonify({
        "passed": passed,
        "percent": percent
    })

# ----------------- boss abattle route -----------------

#-----route to redirect to boss battle topic one-----

@app.route("/start_boss")
def start_boss():
    subprocess.Popen(["python", "boss battle 003.py"])
    return "Boss battle started!"

# ----------------- QUICK FIRE MODE -----------------

@app.route("/quickfire/<grade>")
def quick_fire(grade):

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("quickfire.html", grade=grade)



#=====================all ai funvtions========================


#-----question blueprint route------------

QUESTION_BLUEPRINT = {
    " negative_addition":{
        "operation": "add",
        "number_range": [-20, 0],
        "steps": 1
    },
    "multi_step":{
        "operation": "add_subtract",
        "number_range": [-50, 50],
        "steps": 2
    }
}

#--------online discovery-----------
import json

def fetch_external_patterns(topic):
    """
    Simulates fetching extra question patterns from an 'external knowledge server'.
    Merges new patterns into QUESTION_BLUEPRINT.
    """
    try:
        with open("external_knowledge.json") as f:
            external_data = json.load(f)
        
        topic_data = external_data.get(topic, {})

        for skill, pattern in topic_data.items():
            # Merge into blueprint
            QUESTION_BLUEPRINT[skill] = pattern

    except FileNotFoundError:
        print("External knowledge file not found")
    except Exception as e:
        print("Error loading external knowledge:", e)




# ------------generate--------------

def generate_question_from_skill(skill):
    pattern = QUESTION_BLUEPRINT.get(skill)
    if not pattern:
        return None

    op = pattern["operation"]
    low, high = pattern["number_range"]
    steps = pattern["steps"]

    # Example: simple random numbers for addition
    if op == "add":
        nums = [random.randint(low, high) for _ in range(steps)]
        question_text = " + ".join(map(str, nums))
        answer = sum(nums)
        return {
            "question": f"Solve: {question_text}",
            "choices": [answer, answer+1, answer-1, answer+2],
            "answer": answer
        }

    # You can expand for other operations


# ----------------- LOGOUT -----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ----------------- RUN -----------------

if __name__ == "__main__":
    app.run(debug=True)
