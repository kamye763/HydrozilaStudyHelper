from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
import random
import subprocess

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

#===================================Everything math========================


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
            },
            {
                "question": "What is -10 ÷ 2?",
                "choices": ["-5", "5", "-20", "20"],
                "answer": "-5",
                "explanation": "Negative divided by positive is negative."
            },
            {
                "question": "What is -6 - 4?",
                "choices": ["-10", "10", "-2", "2"],
                "answer": "-10",
                "explanation": "Subtracting a positive number from a negative number makes it more negative."
            },
            {
                "question": "What is -8 + (-3)?",
                "choices": ["-11", "11", "-5", "5"],
                "answer": "-11",
                "explanation": "Adding two negative numbers gives a more negative result."
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
            },
            {
                "question": "What is 2/5 ÷ 1/10?",
                "choices": ["4", "1/5", "5", "1/4"],
                "answer": "4",
                "explanation": "Dividing by a fraction is multiplying by its reciprocal: 2/5 * 10/1 = 20/5 = 4."

            },
            {
                "question": "What is 3/4 - 1/2?",
                "choices": ["1/4", "1/2", "1/8", "3/8"],
                "answer": "1/4",
                "explanation": "Convert to same denominator: 1/2 = 2/4, so 3/4 - 2/4 = 1/4."

            },
            {
                "question": "What is 5/6 + 1/3?",
                "choices": ["7/6", "1/2", "2/3", "1"],
                "answer": "7/6",
                "explanation": "Convert to same denominator: 1/3 = 2/6, so 5/6 + 2/6 = 7/6."
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
            },
            {
                "question": "what is 0.9 ÷ 0.3?",
                "choices": ["3", "0.3", "0.03", "30"],
                "answer": "3",
                "explanation": "0.9 ÷ 0.3 = 9 ÷ 3 = 3."
            },
            {
                "question": "What is 1.5 - 0.7?",
                "choices": ["0.8", "0.9", "1.0", "0.7"],
                "answer": "0.8",
                "explanation": "Subtract the decimal values directly."
            },
            {
                "question": "What is 2.3 + 1.4?",
                "choices": ["3.7", "3.5", "4.0", "3.0"],
                "answer": "3.7",
                "explanation": "Add the decimal values directly."
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
            },
            {
                "question": "find the square of 15",
                "choices": ["225", "225", "225", "225"],
                "answer": "225",
                "explanation": "15 * 15 = 225."
            },
            {
                "question": "find the square root of 144",
                "choices": ["12", "11", "14", "10"],
                "answer": "12",
                "explanation": "The square root of 144 is 12."
            },
            {
                "question": "find the square of 20",
                "choices": ["400", "40", "200", "800"],
                "answer": "400",
                "explanation": "20 * 20 = 400."
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
            },
            {
                "question": "The length of a rectangle is 3p-4 and width is p+ 24. Find the area and perimeter of the rectangle",
                "choices": ["Area: 3p^2 + 68p - 96, Perimeter: 8p + 40", "Area: 3p^2 + 68p - 96, Perimeter: 6p + 20", "Area: 3p^2 + 68p - 96, Perimeter: 6p + 40", "Area: 3p^2 + 68p - 96, Perimeter: 8p + 20"],
                "answer": "Area: 3p^2 + 68p - 96, Perimeter: 8p + 40",
                "explanation": "Area = length * width, Perimeter = 2(length +   width)."
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
        },
        {
            "question": "What is -15 ÷ (-3)?",
            "choices": ["5", "-5", "45", "-45"],
            "answer": "5",
            "explanation": "Negative divided by negative gives a positive."
        },
        {
            "question": "What is 1.5 - 0.7?",
            "choices": ["0.8", "0.9", "1.0", "0.7"],
            "answer": "0.8",
            "explanation": "Subtract the decimal values directly."
        },
        {
            "question": "What is 2.3 + 1.4?",
            "choices": ["3.7", "3.5", "4.0", "3.0"],
            "answer": "3.7",
            "explanation": "Add the decimal values directly."
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
        },
        {
            "question": "What is 4/7 - 2/7?",
            "choices": ["2/7", "6/7", "1/7", "3/7"],
            "answer": "2/7",
            "explanation": "Same denominator: 4/7 - 2/7 = 2/7."
        },
        {
            "question": "What is 5/8 + 1/4?",
            "choices": ["7/8", "3/8", "1/2", "9/8"],
            "answer": "7/8",
            "explanation": "Convert to same denominator: 1/4 = 2/8, so 5/8 + 2/8 = 7/8."
        },
        {
            "question": "What is 3/4 * 2?",
            "choices": ["3/2", "1", "5/4", "1/2"],
            "answer": "3/2",
            "explanation": "Multiply the fraction by the whole number: (3 * 2) / 4 = 6 / 4 = 3 / 2."
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
        },
        {
            "question": "What is 2.5 ÷ 0.5?",
            "choices": ["5", "0.5", "0.05", "25"],
            "answer": "5",
            "explanation": "Dividing by 0.5 is the same as multiplying by 2: 2.5 × 2 = 5."

        },
        {
            "question": "What is 3.6 - 1.1?",
            "choices": ["2.5", "2.7", "2.3", "2.6"],
            "answer": "2.5",
            "explanation": "Subtract the decimal values directly."
        },
        {
            "question": "What is 0.9 + 0.4?",
            "choices": ["1.3", "1.4", "1.2", "1.5"],
            "answer": "1.3",
            "explanation": "Add the decimal values directly."
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
        },
        {
            "question": "What is the square of 7?",
            "choices": ["49", "14", "21", "56"],
            "answer": "49",
            "explanation": "7 × 7 = 49."
        },
        {
            "question": "What is √81?",
            "choices": ["8", "9", "10", "7"],
            "answer": "9",
            "explanation": "9 × 9 = 81."
        },
        {
            "question": "What is the square of 12?",
            "choices": ["144", "24", "36", "132"],
            "answer": "144",
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
        },
        {
            "question": "Factor: x² + 5x + 6",
            "choices": ["(x + 2)(x + 3)", "(x - 2)(x - 3)", "(x + 1)(x + 6)", "(x - 1)(x - 6)"],
            "answer": "(x + 2)(x + 3)",
            "explanation": "Find two numbers that multiply to 6 and add to 5: (x + 2)(x + 3)."
        },
        {
            "question": "Expand: (x + 4)(x - 2)",
            "choices": ["x² + 2x - 8", "x² - 2x - 8", "x² + 6x - 8", "x² - 6x - 8"],
            "answer": "x² + 2x - 8",
            "explanation": "FOIL: x² - 2x + 4x - 8 = x² + 2x - 8."
        },
        {
            "question": "Solve for y: y/3 = 9",
            "choices": ["y = 27", "y = 3", "y = 12", "y = 6"],
            "answer": "y = 27",
            "explanation": "Multiply both sides by 3: y = 9 × 3 = 27."
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
        },
        {
            "question": "Convert 500 ml to liters.",
            "choices": ["0.5 L", "5 L", "50 L", "0.05 L"],
            "answer": "0.5 L",
            "explanation": "1 L = 1000 ml, so 500 ml = 500 / 1000 = 0.5 L."
        },
        {
            "question": "Find the perimeter of a square with side length 6 cm.",
            "choices": ["24 cm", "12 cm", "18 cm", "36 cm"],
            "answer": "24 cm",
            "explanation": "Perimeter = 4 × side length = 4 × 6 = 24 cm."
        },
        {
            "question": "Convert 3 hours to minutes.",
            "choices": ["180 minutes", "30 minutes", "300 minutes", "60 minutes"],
            "answer": "180 minutes",
            "explanation": "1 hour = 60 minutes, so 3 × 60 = 180 minutes."
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
        },
        {
            "question": "What is -5 × (-4)?",
            "choices": ["20", "-20", "9", "-9"],
            "answer": "20",
            "explanation": "Negative times negative gives a positive: -5 × -4 = 20."
        },
        {
            "question": "What is 12 + (-8)?",
            "choices": ["4", "-4", "20", "-20"],
            "answer": "4",
            "explanation": "Adding a negative is subtracting: 12 - 8 = 4."
        },
        {
            "question": "What is -3 ÷ (-1)?",
            "choices": ["3", "-3", "0", "-1"],
            "answer": "3",
            "explanation": "Negative divided by negative gives a positive: -3 ÷ -1 = 3."
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
        },
        {
            "question": "What is 3/4 ÷ 1/2?",
            "choices": ["3/2", "1/2", "1", "2"],
            "answer": "3/2",
            "explanation": "Dividing by 1/2 is multiplying by 2: 3/4 * 2 = 6/4 = 3/2."
        },
        {
            "question": "What is 7/8 + 1/4?",
            "choices": ["9/8", "5/8", "1", "11/8"],
            "answer": "9/8",
            "explanation": "1/4 = 2/8, so 7/8 + 2/8 = 9/8."
        },
        {
            "question": "What is 5/6 - 1/2?",
            "choices": ["1/3", "1/6", "1/2", "1"],
            "answer": "1/3",
            "explanation": "1/2 = 3/6, so 5/6 - 3/6 = 2/6 = 1/3."
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
        },
        {
            "question": "What is 0.9 - 0.3?",
            "choices": ["0.6", "0.3", "1.2", "0.9"],
            "answer": "0.6",
            "explanation": "0.9 - 0.3 = 0.6."
        },
        {
            "question": "What is 3.5 * 2?",
            "choices": ["7", "5", "6", "8"],
            "answer": "7",
            "explanation": "3.5 * 2 = 7."
        },
        {
            "question": "What is 4.8 ÷ 0.2?",
            "choices": ["24", "2.4", "0.96", "48"],
            "answer": "24",
            "explanation": "4.8 ÷ 0.2 = 48 ÷ 2 = 24."
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
        },
        {
            "question": "What is the square of 9?",
            "choices": ["81", "18", "27", "72"],
            "answer": "81",
            "explanation": "9 * 9 = 81."
        },
        {
            "question": "What is √100?",
            "choices": ["10", "9", "11", "12"],
            "answer": "10",
            "explanation": "10 * 10 = 100."
        },
        {
            "question": "What is the square of 5?",
            "choices": ["25", "10", "15", "20"],
            "answer": "25",
            "explanation": "5 * 5 = 25."
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
        },
        {
            "question": "Factor: x² - 9",
            "choices": ["(x + 3)(x - 3)", "(x + 9)(x - 1)", "(x + 1)(x - 9)", "(x + 2)(x - 4)"],
            "answer": "(x + 3)(x - 3)",
            "explanation": "Difference of squares: a² - b² = (a + b)(a - b)."
        },
        {
            "question": "Solve for y: 2y + 4 = 12",
            "choices": ["y = 4", "y = 8", "y = 6", "y = 2"],
            "answer": "y = 4",
            "explanation": "Subtract 4: 2y = 8, divide by 2: y = 4."
        },
        {
            "question": "Simplify: 3(x + 2) - 2(x - 1)",
            "choices": ["x + 8", "5x + 4", "x + 4", "5x + 8"],
            "answer": "x + 8",
            "explanation": "Distribute and combine like terms: (3x + 6) - (2x - 2) = x + 8."
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
        },
        {
            "question": "Find the perimeter of a rectangle with length 12 cm and width 5 cm.",
            "choices": ["34 cm", "17 cm", "24 cm", "30 cm"],
            "answer": "34 cm",
            "explanation": "Perimeter = 2(length + width) = 2(12 + 5) = 34."
        },
        {
            "question": "Convert 1500 meters to kilometers.",
            "choices": ["1.5 km", "15 km", "0.15 km", "150 km"],
            "answer": "1.5 km",
            "explanation": "1 km = 1000 m, so 1500 / 1000 = 1.5 km."
        },
        {
            "question": "Find the area of a circle with radius 7 cm (use π ≈ 3.14).",
            "choices": ["153.86 cm²", "43.96 cm²", "98 cm²", "154 cm²"],
            "answer": "153.86 cm²",
            "explanation": "Area = πr² ≈ 3.14 * 7² ≈ 153.86 cm²."
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


AgriQUESTIONS ={
    "Grade 7": {
      "Crop Production": {
        "Types of Crops": [
          {
            "question": "Maize is a type of?",
            "choices": ["Cereal", "Fruit", "Flower", "Root"],
            "answer": "Cereal",
            "explanation": "Maize is classified as a cereal because it is a grass grown for its edible grain."
          },
          {
            "question": "Beans are classified as?",
            "choices": ["Legumes", "Cereals", "Fruits", "Tubers"],
            "answer": "Legumes",
            "explanation": "Beans belong to the legume family, which are plants that produce pods containing seeds."
          }
        ]
      },
      "Soil Management": {
        "Soil Types": [
          {
            "question": "Best soil for farming?",
            "choices": ["Loam", "Sand", "Clay", "Rock"],
            "answer": "Loam",
            "explanation": "Loam soil has a balanced mixture of sand, silt, and clay making it ideal for crops."
          },
          {
            "question": "Soil erosion is caused by?",
            "choices": ["Wind and water", "Plastic", "Metal", "Fire"],
            "answer": "Wind and water",
            "explanation": "Soil erosion occurs when wind or water removes the topsoil."
          }
        ]
      },
      "Cells": {
        "Cell Structure": [
          {
            "question": "Basic unit of life?",
            "choices": ["Cell", "Atom", "Organ", "Tissue"],
            "answer": "Cell",
            "explanation": "The cell is the smallest structural and functional unit of life."
          },
          {
            "question": "Controls the cell?",
            "choices": ["Nucleus", "Ribosome", "Vacuole", "Chloroplast"],
            "answer": "Nucleus",
            "explanation": "The nucleus controls cell activities and stores genetic material."
          }
        ]
      }
    },
    "Grade 8": {
      "Soil Management": {
        "Soil Types": [
          {
            "question": "Which soil type is best for farming?",
            "choices": ["Loam", "Sand", "Clay", "Rock"],
            "answer": "Loam",
            "explanation": "Loam soil has a balanced mixture of sand, silt, and clay making it ideal for crops."
          },
          {
            "question": "Which soil drains water fastest?",
            "choices": ["Sandy soil", "Clay soil", "Loam soil", "Peat soil"],
            "answer": "Sandy soil",
            "explanation": "Sandy soil has large particles that allow water to drain quickly."
          },
          {
            "question": "Which soil holds the most water?",
            "choices": ["Clay soil", "Sandy soil", "Gravel", "Silt"],
            "answer": "Clay soil",
            "explanation": "Clay soil particles are very small and hold water tightly."
          },
          {
            "question": "Organic matter in soil is called?",
            "choices": ["Humus", "Sand", "Salt", "Dust"],
            "answer": "Humus",
            "explanation": "Humus is decomposed plant and animal material in soil."
          },
          {
            "question": "Which soil is easiest to cultivate?",
            "choices": ["Loam", "Clay", "Rock", "Gravel"],
            "answer": "Loam",
            "explanation": "Loam soil is soft and fertile, making it easy to cultivate."
          },
          {
            "question": "Soil erosion means?",
            "choices": ["Wearing away of soil", "Planting crops", "Adding fertilizer", "Watering crops"],
            "answer": "Wearing away of soil",
            "explanation": "Soil erosion occurs when wind or water removes the topsoil."
          },
          {
            "question": "Which agent causes soil erosion?",
            "choices": ["Wind", "Water", "Animals", "All of these"],
            "answer": "All of these",
            "explanation": "Wind, water, and animals can all contribute to soil erosion."
          },
          {
            "question": "Terracing helps to?",
            "choices": ["Reduce erosion", "Increase erosion", "Kill crops", "Dry soil"],
            "answer": "Reduce erosion",
            "explanation": "Terraces slow water flow and prevent soil loss on slopes."
          },
          {
            "question": "Planting trees helps to?",
            "choices": ["Prevent erosion", "Increase erosion", "Destroy soil", "Dry soil"],
            "answer": "Prevent erosion",
            "explanation": "Tree roots hold soil together and prevent erosion."
          },
          {
            "question": "Soil fertility means?",
            "choices": ["Ability of soil to support plant growth", "Hard soil", "Dry soil", "Rock soil"],
            "answer": "Ability of soil to support plant growth",
            "explanation": "Fertile soil contains nutrients necessary for plant growth."
          }
        ]
      }
    },
    "Grade 9": {
      "Agribusiness": {
        "Entrepreneurship": [
          {
            "question": "Who is an entrepreneur?",
            "choices": ["A person who starts and runs a business", "A teacher", "A customer", "An employee only"],
            "answer": "A person who starts and runs a business",
            "explanation": "An entrepreneur creates and manages a business."
          },
          {
            "question": "What is profit?",
            "choices": ["Money gained after expenses", "Money lost", "Total sales only", "Money borrowed"],
            "answer": "Money gained after expenses",
            "explanation": "Profit is what remains after subtracting expenses from income."
          },
          {
            "question": "What is a business plan?",
            "choices": ["A written guide for running a business", "A school timetable", "A farm tool", "A market stall"],
            "answer": "A written guide for running a business",
            "explanation": "A business plan outlines goals and strategies for running a business."
          },
          {
            "question": "Capital means?",
            "choices": ["Money used to start a business", "Profit", "Loss", "Tax"],
            "answer": "Money used to start a business",
            "explanation": "Capital is the money required to begin a business."
          },
          {
            "question": "Marketing means?",
            "choices": ["Promoting and selling products", "Planting crops", "Watering plants", "Harvesting"],
            "answer": "Promoting and selling products",
            "explanation": "Marketing involves promoting and selling goods or services."
          }
        ]
      }
    }
      
  }

intergratedsci_Questions ={
      "Grade 7": {
      "Cells": {
        "Cell Structure": [
          {
            "question": "Basic unit of life?",
            "choices": ["Cell", "Atom", "Organ", "Tissue"],
            "answer": "Cell",
            "explanation": "The cell is the smallest structural and functional unit of life."
          },
          {
            "question": "Controls the cell?",
            "choices": ["Nucleus", "Ribosome", "Vacuole", "Chloroplast"],
            "answer": "Nucleus",
            "explanation": "The nucleus controls cell activities and stores genetic material."
          },
          {
            "question": "Which cell organelle makes energy?",
            "choices": ["Mitochondria", "Ribosome", "Chloroplast", "Vacuole"],
            "answer": "Mitochondria",
            "explanation": "Mitochondria are the powerhouse of the cell."
          },
          {
            "question": "Which organelle helps in photosynthesis?",
            "choices": ["Chloroplast", "Nucleus", "Ribosome", "Lysosome"],
            "answer": "Chloroplast",
            "explanation": "Chloroplasts contain chlorophyll that captures sunlight for photosynthesis."
          },
          {
            "question": "Stores water and nutrients in plant cells?",
            "choices": ["Vacuole", "Ribosome", "Nucleus", "Mitochondria"],
            "answer": "Vacuole",
            "explanation": "Vacuoles store water, nutrients, and waste materials."
          },
          {
            "question": "Helps in protein synthesis?",
            "choices": ["Ribosome", "Nucleus", "Vacuole", "Chloroplast"],
            "answer": "Ribosome",
            "explanation": "Ribosomes assemble amino acids into proteins."
          },
          {
            "question": "Protects the cell and gives it shape?",
            "choices": ["Cell wall", "Cell membrane", "Nucleus", "Mitochondria"],
            "answer": "Cell wall",
            "explanation": "The cell wall provides protection and structure in plant cells."
          },
          {
            "question": "Controls what enters and leaves the cell?",
            "choices": ["Cell membrane", "Cell wall", "Nucleus", "Ribosome"],
            "answer": "Cell membrane",
            "explanation": "The cell membrane regulates movement of substances."
          },
          {
            "question": "Breaks down waste materials in the cell?",
            "choices": ["Lysosome", "Mitochondria", "Ribosome", "Nucleus"],
            "answer": "Lysosome",
            "explanation": "Lysosomes contain enzymes that digest waste."
          },
          {
            "question": "Thread-like structures in the nucleus are called?",
            "choices": ["Chromosomes", "Ribosomes", "Vacuoles", "Mitochondria"],
            "answer": "Chromosomes",
            "explanation": "Chromosomes carry genetic information in DNA."
          },
          {
            "question": "Supports the cell internally?",
            "choices": ["Cytoskeleton", "Nucleus", "Cell membrane", "Vacuole"],
            "answer": "Cytoskeleton",
            "explanation": "The cytoskeleton maintains cell shape and helps movement."
          },
          {
            "question": "Site where chemical reactions occur in the cell?",
            "choices": ["Cytoplasm", "Nucleus", "Vacuole", "Chloroplast"],
            "answer": "Cytoplasm",
            "explanation": "Most cellular reactions occur in the cytoplasm."
          },
          {
            "question": "Which organelle stores genetic material?",
            "choices": ["Nucleus", "Mitochondria", "Vacuole", "Lysosome"],
            "answer": "Nucleus",
            "explanation": "The nucleus stores DNA."
          },
          {
            "question": "Which organelle is involved in cell division?",
            "choices": ["Centrosome", "Ribosome", "Vacuole", "Mitochondria"],
            "answer": "Centrosome",
            "explanation": "The centrosome organizes microtubules during cell division."
          },
          {
            "question": "Which structure forms the boundary of an animal cell?",
            "choices": ["Cell membrane", "Cell wall", "Vacuole", "Chloroplast"],
            "answer": "Cell membrane",
            "explanation": "Animal cells are enclosed by a cell membrane."
          },
          {
            "question": "Organelle that helps in detoxification?",
            "choices": ["Peroxisome", "Mitochondria", "Ribosome", "Vacuole"],
            "answer": "Peroxisome",
            "explanation": "Peroxisomes break down harmful substances."
          },
          {
            "question": "Which organelle contains enzymes to digest food?",
            "choices": ["Lysosome", "Chloroplast", "Ribosome", "Nucleus"],
            "answer": "Lysosome",
            "explanation": "Lysosomes digest food and waste."
          },
          {
            "question": "Which part of the cell gives plants their color?",
            "choices": ["Chloroplast", "Nucleus", "Mitochondria", "Vacuole"],
            "answer": "Chloroplast",
            "explanation": "Chloroplasts contain green chlorophyll."
          },
          {
            "question": "Which organelle packages proteins for transport?",
            "choices": ["Golgi apparatus", "Ribosome", "Nucleus", "Vacuole"],
            "answer": "Golgi apparatus",
            "explanation": "The Golgi apparatus modifies and packages proteins."
          },
          {
            "question": "Which organelle produces lipids and detoxifies drugs?",
            "choices": ["Smooth endoplasmic reticulum", "Rough endoplasmic reticulum", "Mitochondria", "Lysosome"],
            "answer": "Smooth endoplasmic reticulum",
            "explanation": "Smooth ER produces lipids and detoxifies chemicals."
          }
        ]
      }
    },

    "Grade 8": {
      "Human Body": {
        "Digestive System": [
          {
            "question": "Where does digestion begin?",
            "choices": ["Mouth", "Stomach", "Liver", "Intestine"],
            "answer": "Mouth",
            "explanation": "Digestion begins in the mouth."
          },
          {
            "question": "Which organ pumps blood?",
            "choices": ["Heart", "Liver", "Kidney", "Brain"],
            "answer": "Heart",
            "explanation": "The heart pumps blood around the body."
          },
          {
            "question": "Which organ helps in breathing?",
            "choices": ["Lungs", "Heart", "Stomach", "Liver"],
            "answer": "Lungs",
            "explanation": "Lungs exchange oxygen and carbon dioxide."
          },
          {
            "question": "Where is food stored before digestion?",
            "choices": ["Stomach", "Heart", "Liver", "Kidney"],
            "answer": "Stomach",
            "explanation": "The stomach temporarily stores and digests food."
          },
          {
            "question": "Which organ absorbs nutrients?",
            "choices": ["Small intestine", "Large intestine", "Stomach", "Kidney"],
            "answer": "Small intestine",
            "explanation": "The small intestine absorbs nutrients."
          },
          {
            "question": "Which organ removes waste water?",
            "choices": ["Large intestine", "Stomach", "Heart", "Brain"],
            "answer": "Large intestine",
            "explanation": "The large intestine absorbs water and forms feces."
          }
        ]
      }
    }
  }


 

cre = {
  "Grade 7": {
        "Creation": {
            "Genesis": [
                {"q":"Who created the world?","o":["God","Paul","David","Moses"],"a":"God"},
                {"q":"Created in how many days?","o":["6","7","3","10"],"a":"6"},
                {"q":"Who created man?","o":["God","Jesus","Moses","David"],"a":"God"},
                {"q":"Who created woman?","o":["God","Adam","Noah","Abraham"],"a":"God"},
                {"q":"Which tree did God command Adam not to eat from?","o":["Tree of Knowledge","Tree of Life","Olive tree","Fig tree"],"a":"Tree of Knowledge"},
                {"q":"Who was the first man?","o":["Adam","Noah","Moses","Abraham"],"a":"Adam"},
                {"q":"Who was the first woman?","o":["Eve","Sarah","Mary","Hagar"],"a":"Eve"},
                {"q":"What was created on the first day?","o":["Light","Land","Sun","Stars"],"a":"Light"},
                {"q":"What was created on the second day?","o":["Sky","Animals","Plants","Moon"],"a":"Sky"},
                {"q":"What was created on the third day?","o":["Land and plants","Sun","Moon","Stars"],"a":"Land and plants"},
                {"q":"What was created on the fourth day?","o":["Sun, moon, stars","Fish","Birds","Animals"],"a":"Sun, moon, stars"},
                {"q":"What was created on the fifth day?","o":["Fish and birds","Land animals","Humans","Plants"],"a":"Fish and birds"},
                {"q":"What was created on the sixth day?","o":["Land animals and humans","Fish","Birds","Plants"],"a":"Land animals and humans"},
                {"q":"What did God do on the seventh day?","o":["Rested","Created humans","Created animals","Created plants"],"a":"Rested"},
                {"q":"Who named the animals?","o":["Adam","God","Eve","Noah"],"a":"Adam"},
                {"q":"What was Adam's job in the garden?","o":["To tend and keep it","To eat fruits only","To travel","To build houses"],"a":"To tend and keep it"},
                {"q":"Who was tempted by the serpent?","o":["Eve","Adam","Noah","Moses"],"a":"Eve"},
                {"q":"Who ate the forbidden fruit first?","o":["Eve","Adam","Noah","Abraham"],"a":"Eve"},
                {"q":"What happened after eating the forbidden fruit?","o":["Sin entered the world","God created more","Earth became dry","Animals spoke"],"a":"Sin entered the world"},
                {"q":"Where did Adam and Eve live?","o":["Garden of Eden","Jerusalem","Nazareth","Egypt"],"a":"Garden of Eden"}
            ]
        }
    },
  
  "Grade 8": {
    "Life of Jesus": [
      {
        "question": "Where was Jesus born?",
        "choices": ["Bethlehem", "Nazareth", "Jerusalem", "Rome"],
        "answer": "Bethlehem",
        "explanation": "Jesus was born in Bethlehem according to the Gospels."
      },
      {
        "question": "Who was the mother of Jesus?",
        "choices": ["Mary", "Martha", "Sarah", "Ruth"],
        "answer": "Mary",
        "explanation": "Mary was chosen by God to give birth to Jesus."
      },
      {
        "question": "Who was the earthly father of Jesus?",
        "choices": ["Joseph", "Peter", "David", "John"],
        "answer": "Joseph",
        "explanation": "Joseph cared for Jesus as his earthly father."
      },
      {
        "question": "Who baptized Jesus?",
        "choices": ["John the Baptist", "Peter", "James", "Paul"],
        "answer": "John the Baptist",
        "explanation": "John the Baptist baptized Jesus in the Jordan River."
      },
      {
        "question": "Where was Jesus baptized?",
        "choices": ["River Jordan", "Sea of Galilee", "Red Sea", "River Nile"],
        "answer": "River Jordan",
        "explanation": "Jesus was baptized in the River Jordan."
      },
      {
        "question": "How many disciples did Jesus have?",
        "choices": ["12", "10", "7", "15"],
        "answer": "12",
        "explanation": "Jesus chose twelve disciples to follow and learn from him."
      },
      {
        "question": "Jesus performed miracles to?",
        "choices": ["Help people", "Show magic", "Make money", "Entertain crowds"],
        "answer": "Help people",
        "explanation": "Jesus performed miracles to show God's power and compassion."
      },
      {
        "question": "Jesus fed 5000 people with?",
        "choices": ["Five loaves and two fish", "Ten loaves", "Bread only", "Fish only"],
        "answer": "Five loaves and two fish",
        "explanation": "Jesus multiplied five loaves and two fish to feed a large crowd."
      },
      {
        "question": "Jesus walked on?",
        "choices": ["Water", "Sand", "Mountains", "Clouds"],
        "answer": "Water",
        "explanation": "Jesus walked on water showing divine power."
      },
      {
        "question": "Jesus raised who from the dead?",
        "choices": ["Lazarus", "Peter", "James", "Matthew"],
        "answer": "Lazarus",
        "explanation": "Jesus brought Lazarus back to life in a miracle."
      },
      {
        "question": "Jesus taught people to?",
        "choices": ["Love one another", "Fight enemies", "Ignore others", "Hate neighbors"],
        "answer": "Love one another",
        "explanation": "Jesus emphasized love and kindness."
      },
      {
        "question": "What is the Golden Rule?",
        "choices": ["Treat others as you want to be treated", "Work hard", "Pray daily", "Study always"],
        "answer": "Treat others as you want to be treated",
        "explanation": "The Golden Rule teaches kindness and fairness."
      },
      {
        "question": "Jesus entered Jerusalem riding a?",
        "choices": ["Donkey", "Horse", "Camel", "Cart"],
        "answer": "Donkey",
        "explanation": "Jesus rode a donkey on Palm Sunday."
      },
      {
        "question": "What meal did Jesus share with disciples before crucifixion?",
        "choices": ["Last Supper", "Passover meal", "Wedding feast", "Breakfast"],
        "answer": "Last Supper",
        "explanation": "The Last Supper was Jesus’ final meal with his disciples."
      },
      {
        "question": "Where was Jesus crucified?",
        "choices": ["Golgotha", "Nazareth", "Bethlehem", "Rome"],
        "answer": "Golgotha",
        "explanation": "Jesus was crucified at Golgotha."
      },
      {
        "question": "Who betrayed Jesus?",
        "choices": ["Judas Iscariot", "Peter", "John", "Andrew"],
        "answer": "Judas Iscariot",
        "explanation": "Judas betrayed Jesus for thirty pieces of silver."
      },
      {
        "question": "Who denied Jesus three times?",
        "choices": ["Peter", "John", "Thomas", "James"],
        "answer": "Peter",
        "explanation": "Peter denied knowing Jesus three times before the rooster crowed."
      },
      {
        "question": "After how many days did Jesus rise?",
        "choices": ["Three days", "Seven days", "One day", "Ten days"],
        "answer": "Three days",
        "explanation": "Jesus rose from the dead on the third day."
      },
      {
        "question": "Jesus appeared to disciples after?",
        "choices": ["Resurrection", "Birth", "Baptism", "Temptation"],
        "answer": "Resurrection",
        "explanation": "After rising from the dead, Jesus appeared to his disciples."
      },
      {
        "question": "Jesus ascended to?",
        "choices": ["Heaven", "Jerusalem", "Nazareth", "Rome"],
        "answer": "Heaven",
        "explanation": "Jesus ascended into heaven after his resurrection."
      }
    ]
  },
  "CRE_GRADE_9": {
    "Early Church": [
      {
        "question": "Which book describes the early church?",
        "choices": ["Acts", "Genesis", "Luke", "Matthew"],
        "answer": "Acts",
        "explanation": "The Book of Acts explains the growth of the early church."
      },
      {
        "question": "The Holy Spirit came during?",
        "choices": ["Pentecost", "Christmas", "Easter", "Passover"],
        "answer": "Pentecost",
        "explanation": "The Holy Spirit descended on the disciples during Pentecost."
      },
      {
        "question": "Who preached the first sermon after Pentecost?",
        "choices": ["Peter", "Paul", "James", "John"],
        "answer": "Peter",
        "explanation": "Peter preached and many people believed."
      },
      {
        "question": "How many people believed after Peter's sermon?",
        "choices": ["3000", "500", "100", "50"],
        "answer": "3000",
        "explanation": "About 3000 people accepted the message."
      },
      {
        "question": "What helped spread Christianity?",
        "choices": ["Preaching", "War", "Trade only", "Politics"],
        "answer": "Preaching",
        "explanation": "The apostles spread Christianity through preaching."
      },
      {
        "question": "Who was formerly called Saul?",
        "choices": ["Paul", "Peter", "James", "Matthew"],
        "answer": "Paul",
        "explanation": "Paul was originally called Saul before converting."
      },
      {
        "question": "Paul was converted on the road to?",
        "choices": ["Damascus", "Jerusalem", "Rome", "Nazareth"],
        "answer": "Damascus",
        "explanation": "Paul encountered Jesus on the road to Damascus."
      },
      {
        "question": "Early Christians met in?",
        "choices": ["Homes", "Palaces", "Schools", "Markets"],
        "answer": "Homes",
        "explanation": "They gathered in homes for worship."
      },
      {
        "question": "Stephen was the first?",
        "choices": ["Martyr", "Priest", "King", "Prophet"],
        "answer": "Martyr",
        "explanation": "Stephen was killed for his faith."
      },
      {
        "question": "Barnabas was known as?",
        "choices": ["Encourager", "King", "Judge", "Warrior"],
        "answer": "Encourager",
        "explanation": "Barnabas supported and encouraged believers."
      },
      {
        "question": "The disciples were first called Christians in?",
        "choices": ["Antioch", "Jerusalem", "Rome", "Galilee"],
        "answer": "Antioch",
        "explanation": "The name Christian was first used in Antioch."
      },
      {
        "question": "Paul wrote letters to?",
        "choices": ["Churches", "Kings", "Farmers", "Soldiers"],
        "answer": "Churches",
        "explanation": "Paul wrote letters to guide Christian communities."
      },
      {
        "question": "Persecution means?",
        "choices": ["Suffering for beliefs", "Celebration", "Teaching", "Praying"],
        "answer": "Suffering for beliefs",
        "explanation": "Early Christians were persecuted for their faith."
      },
      {
        "question": "Faith means?",
        "choices": ["Trust in God", "Fear", "Doubt", "Anger"],
        "answer": "Trust in God",
        "explanation": "Faith means trusting God even without seeing."
      },
      {
        "question": "The Bible teaches believers to?",
        "choices": ["Love others", "Hate others", "Ignore others", "Fight others"],
        "answer": "Love others",
        "explanation": "Love is a central teaching of Christianity."
      },
      {
        "question": "Prayer is?",
        "choices": ["Talking to God", "Sleeping", "Eating", "Working"],
        "answer": "Talking to God",
        "explanation": "Prayer is communication with God."
      },
      {
        "question": "Church leaders are called?",
        "choices": ["Pastors", "Kings", "Soldiers", "Farmers"],
        "answer": "Pastors",
        "explanation": "Pastors guide believers spiritually."
      },
      {
        "question": "The gospel means?",
        "choices": ["Good news", "War story", "Song", "Law"],
        "answer": "Good news",
        "explanation": "The gospel is the good news about Jesus."
      },
      {
        "question": "The church is?",
        "choices": ["Community of believers", "A building only", "A school", "A market"],
        "answer": "Community of believers",
        "explanation": "The church refers to people who believe in Christ."
      },
      {
        "question": "Christians follow the teachings of?",
        "choices": ["Jesus", "Moses", "Abraham", "David"],
        "answer": "Jesus",
        "explanation": "Jesus’ teachings guide Christian life."
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
    level = session.get("level", 1)
    

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
    
    # shuffle questions
    shuffled = topic_questions.copy()
    random.shuffle(shuffled)

    session["questions"] = shuffled
    session["q_index"] = 0
    session["score"] = 0

    return render_template(
        "mathpractice.html",
        grade=grade,
        topic=topic
    )

@app.route("/mathpractice/<grade>/<topic>/get_question")
def get_math_question(grade, topic):

    if "questions" not in session:
        return jsonify({"error": "No questions"}), 404

    questions = session["questions"]
    index = session.get("q_index", 0)

    if index >= len(questions):
        return jsonify({"finished": True})

    question = questions[index]
    session["q_index"] = index + 1

    return jsonify({
        "question": question["question"],
        "choices": question["choices"],
        "answer": question["answer"],
        "explanation": question.get("explanation", "")
    })
# ----------------- FINISH TEST -----------------

@app.route("/mathpractice/<grade>/<topic>/finish", methods=["POST"])
def finish_mathtest(grade, topic):

    data = request.get_json()
    percent = data.get("percent", 0)

    passed = percent >= 70

    if passed:
        return redirect(url_for("start_boss"))

    
    return jsonify({
        "passed": passed,
        "percent": percent
    })

def complete_topic():
    level = session.get("level", 1)
    session["level"] = level + 1
    return session["level"]

# ----------------- boss battle route -----------------

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


#============================================Everything Pretech======================================================

#---------------------------------------loading the page------------------------------------------
@app.route("/pretech")
def pretech_page():
    if "user" not in session:
        return redirect(url_for("login"))

    grade = session.get("grade")
    topics = Pre_techQuestions.get(grade, {}).keys()

    return render_template(
        "pretechpage.html",
        grade=grade,
        topics=topics
    )

#-----------------------------------------PRETECH TOPICS PAGE------------------------------------------
@app.route("/pretechpage/<grade>/topics")
def pretech_topics(grade):
    if "user" not in session:
        return redirect(url_for("login"))
     
    grade = str(grade)
    
   
    topics = list(Pre_techQuestions[grade].keys())

    return render_template(
        "pretechpage.html",
        grade=grade,
        topics=topics
    )

#-------------------------------------PRETECH PRACTICE PAGE----------------------------------------
@app.route("/pretechpractice/<grade>/<topic>")
def pretech_practice(grade, topic):

    if "user" not in session:
        return redirect(url_for("login"))

    topic_questions = Pre_techQuestions.get(str(grade), {}).get(topic, [])

    if not topic_questions:
        return "No questions found for this topic", 404
    
    # shuffle questions
    shuffled = topic_questions.copy()
    random.shuffle(shuffled)

    session["questions"] = shuffled
    session["q_index"] = 0
    session["score"] = 0

    return render_template(
        "pretechpractice.html",
        grade=grade,
        topic=topic
    )

@app.route("/pretechpractice/<grade>/<topic>/get_question")
def get_pretech_question(grade, topic):

    if "questions" not in session:
        return jsonify({"error": "No questions"}), 404

    questions = session["questions"]
    index = session.get("q_index", 0)

    if index >= len(questions):
        return jsonify({"finished": True})

    question = questions[index]
    session["q_index"] = index + 1

    return jsonify({
        "question": question["question"],
        "choices": question["choices"],
        "answer": question["answer"],
        "explanation": question.get("explanation", "")
    })
# ----------------- FINISH TEST -----------------

@app.route("/pretechpractice/<grade>/<topic>/finish", methods=["POST"])
def finish_pretechtest(grade, topic):

    data = request.get_json()
    percent = data.get("percent", 0)

    passed = percent >= 70

    return jsonify({
        "passed": passed,
        "percent": percent
    })
def compleate_topic():
    level = session.get("level", 1)
    if level not in session:
        session["level"] = 1

    else:
        session["level"] += 1

    return session["level"]


#=====================================EVERYTHING AGRICULTURE=============================================

#---------------------------------------loading the page------------------------------------------
@app.route("/Agriculture")
def Agriculter_page():
    if "user" not in session:
        return redirect(url_for("login"))

    grade = session.get("grade")
    topics = AgriQUESTIONS.get(grade, {}).keys()

    return render_template(
        "Agriculture.html",
        grade=grade,
        topics=topics
    )

#-----------------------------------------AGRI TOPICS PAGE------------------------------------------
@app.route("/Agriculture/<grade>/topics")
def agriculture_topics(grade):
    if "user" not in session:
        return redirect(url_for("login"))
     
    grade = str(grade)
    
   
    topics = list(AgriQUESTIONS[grade].keys())

    return render_template(
        "Agriculturepage.html",
        grade=grade,
        topics=topics
    )

#-------------------------------------AGRI PRACTICE PAGE----------------------------------------
@app.route("/Agriculturepractice/<grade>/<topic>")
def agriculture_practice(grade, topic):

    if "user" not in session:
        return redirect(url_for("login"))

    topic_questions = AgriQUESTIONS.get(str(grade), {}).get(topic, [])

    if not topic_questions:
        return "No questions found for this topic", 404
    
    # shuffle questions
    shuffled = topic_questions.copy()
    random.shuffle(shuffled)

    session["questions"] = shuffled
    session["q_index"] = 0
    session["score"] = 0

    return render_template(
        "agriculturepractice.html",
        grade=grade,
        topic=topic
    )

@app.route("/agriculturepractice/<grade>/<topic>/get_question")
def get_agriculture_question(grade, topic):

    if "questions" not in session:
        return jsonify({"error": "No questions"}), 404

    questions = session["questions"]
    index = session.get("q_index", 0)

    if index >= len(questions):
        return jsonify({"finished": True})

    question = questions[index]
    session["q_index"] = index + 1

    return jsonify({
        "question": question["question"],
        "choices": question["choices"],
        "answer": question["answer"],
        "explanation": question.get("explanation", "")
    })
# ----------------- FINISH TEST -----------------

@app.route("/Agriculturepractice/<grade>/<topic>/finish", methods=["POST"])
def finish_agritest(grade, topic):

    data = request.get_json()
    percent = data.get("percent", 0)

    passed = percent >= 70

    return jsonify({
        "passed": passed,
        "percent": percent
    })

#=====================================EVERYTHING INTERGRATED SCI========================================
#---------------------------------------loading the page------------------------------------------
@app.route("/IntegratedSci")
def IntegratedSci_page():
    if "user" not in session:
        return redirect(url_for("login"))

    grade = session.get("grade")
    topics = intergratedsci_Questions.get(grade, {}).keys()

    return render_template(
        "integratedsci.html",
        grade=grade,
        topics=topics
    )

#-----------------------------------------SCI TOPICS PAGE------------------------------------------
@app.route("/IntegratedSci/<grade>/topics")
def intergratedsci_topics(grade):
    if "user" not in session:
        return redirect(url_for("login"))
     
    grade = str(grade)
    
   
    topics = list(intergratedsci_Questions[grade].keys())

    return render_template(
        "intergratedscipage.html",
        grade=grade,
        topics=topics
    )

#-------------------------------------SCI PRACTICE PAGE----------------------------------------
@app.route("/intergratedscipractice/<grade>/<topic>")
def intergratedsci_practice(grade, topic):

    if "user" not in session:
        return redirect(url_for("login"))

    topic_questions = intergratedsci_Questions.get(str(grade), {}).get(topic, [])

    if not topic_questions:
        return "No questions found for this topic", 404
    
    # shuffle questions
    shuffled = topic_questions.copy()
    random.shuffle(shuffled)

    session["questions"] = shuffled
    session["q_index"] = 0
    session["score"] = 0

    return render_template(
        "intergratedscipractice.html",
        grade=grade,
        topic=topic
    )

@app.route("/intergratedscipractice/<grade>/<topic>/get_question")
def get_intergratedsci_question(grade, topic):

    if "questions" not in session:
        return jsonify({"error": "No questions"}), 404

    questions = session["questions"]
    index = session.get("q_index", 0)

    if index >= len(questions):
        return jsonify({"finished": True})

    question = questions[index]
    session["q_index"] = index + 1

    return jsonify({
        "question": question["question"],
        "choices": question["choices"],
        "answer": question["answer"],
        "explanation": question.get("explanation", "")
    })

# ----------------- FINISH TEST -----------------

@app.route("/IntegratedScipractice/<grade>/<topic>/finish", methods=["POST"])
def finish_integratedsci_test(grade, topic):

    data = request.get_json()
    percent = data.get("percent", 0)

    passed = percent >= 70

    return jsonify({
        "passed": passed,
        "percent": percent
    })

def complete_topic():
    level = session.get("level", 1)
    session["level"] = level + 1
    return session["level"]
# ----------------- LOGOUT -----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ----------------- RUN -----------------

if __name__ == "__main__":
    app.run(debug=True)