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

{
  "Agriculture": {
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
  },
  "Science": {
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
            "explanation": "Mitochondria are the powerhouse of the cell and produce energy through respiration."
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
            "explanation": "Vacuoles store water, nutrients, and waste materials in cells."
          },
          {
            "question": "Helps in protein synthesis?",
            "choices": ["Ribosome", "Nucleus", "Vacuole", "Chloroplast"],
            "answer": "Ribosome",
            "explanation": "Ribosomes are responsible for assembling amino acids into proteins."
          },
          {
            "question": "Protects the cell and gives it shape?",
            "choices": ["Cell wall", "Cell membrane", "Nucleus", "Mitochondria"],
            "answer": "Cell wall",
            "explanation": "The cell wall is a rigid outer layer in plant cells that provides protection and shape."
          },
          {
            "question": "Controls what enters and leaves the cell?",
            "choices": ["Cell membrane", "Cell wall", "Nucleus", "Ribosome"],
            "answer": "Cell membrane",
            "explanation": "The cell membrane regulates the movement of substances in and out of the cell."
          },
          {
            "question": "Breaks down waste materials in the cell?",
            "choices": ["Lysosome", "Mitochondria", "Ribosome", "Nucleus"],
            "answer": "Lysosome",
            "explanation": "Lysosomes contain enzymes that digest cellular waste and foreign materials."
          },
          {
            "question": "Thread-like structures in the nucleus are called?",
            "choices": ["Chromosomes", "Ribosomes", "Vacuoles", "Mitochondria"],
            "answer": "Chromosomes",
            "explanation": "Chromosomes carry genetic information in the form of DNA."
          },
          {
            "question": "Supports the cell internally?",
            "choices": ["Cytoskeleton", "Nucleus", "Cell membrane", "Vacuole"],
            "answer": "Cytoskeleton",
            "explanation": "The cytoskeleton is a network of fibers that maintains cell shape and helps in movement."
          },
          {
            "question": "Site where chemical reactions occur in the cell?",
            "choices": ["Cytoplasm", "Nucleus", "Vacuole", "Chloroplast"],
            "answer": "Cytoplasm",
            "explanation": "The cytoplasm is a jelly-like fluid where most cellular reactions take place."
          },
          {
            "question": "Which organelle stores genetic material?",
            "choices": ["Nucleus", "Mitochondria", "Vacuole", "Lysosome"],
            "answer": "Nucleus",
            "explanation": "The nucleus stores DNA, which controls cell activities and heredity."
          },
          {
            "question": "Which organelle is involved in cell division?",
            "choices": ["Centrosome", "Ribosome", "Vacuole", "Mitochondria"],
            "answer": "Centrosome",
            "explanation": "The centrosome helps in organizing microtubules during cell division."
          },
          {
            "question": "Which structure forms the boundary of an animal cell?",
            "choices": ["Cell membrane", "Cell wall", "Vacuole", "Chloroplast"],
            "answer": "Cell membrane",
            "explanation": "Animal cells have a flexible cell membrane that encloses the cell."
          },
          {
            "question": "Organelle that helps in detoxification?",
            "choices": ["Peroxisome", "Mitochondria", "Ribosome", "Vacuole"],
            "answer": "Peroxisome",
            "explanation": "Peroxisomes break down harmful substances and protect the cell."
          },
          {
            "question": "Which organelle contains enzymes to digest food?",
            "choices": ["Lysosome", "Chloroplast", "Ribosome", "Nucleus"],
            "answer": "Lysosome",
            "explanation": "Lysosomes contain digestive enzymes to break down food and waste."
          },
          {
            "question": "Which part of the cell gives it color in plants?",
            "choices": ["Chloroplast", "Nucleus", "Mitochondria", "Vacuole"],
            "answer": "Chloroplast",
            "explanation": "Chloroplasts contain green chlorophyll which gives plants their color."
          },
          {
            "question": "Which organelle packages proteins for transport?",
            "choices": ["Golgi apparatus", "Ribosome", "Nucleus", "Vacuole"],
            "answer": "Golgi apparatus",
            "explanation": "The Golgi apparatus modifies, sorts, and packages proteins for secretion or use."
          },
          {
            "question": "Which organelle produces lipids and detoxifies drugs?",
            "choices": ["Smooth endoplasmic reticulum", "Rough endoplasmic reticulum", "Mitochondria", "Lysosome"],
            "answer": "Smooth endoplasmic reticulum",
            "explanation": "The smooth ER produces lipids and helps in detoxification processes."
          }
        
      }
    }
    "Grade 8": {
      "Human Body": {
        "Digestive System": [
          {
            "question": "Where does digestion begin?",
            "choices": ["Mouth", "Stomach", "Liver", "Intestine"],
            "answer": "Mouth",
            "explanation": "Digestion begins in the mouth where food is chewed and mixed with saliva."
          },
          {
            "question": "Which organ pumps blood?",
            "choices": ["Heart", "Liver", "Kidney", "Brain"],
            "answer": "Heart",
            "explanation": "The heart pumps blood to all parts of the body."
          },
          {
            "question": "Which organ helps in breathing?",
            "choices": ["Lungs", "Heart", "Stomach", "Liver"],
            "answer": "Lungs",
            "explanation": "Lungs allow oxygen to enter the blood and remove carbon dioxide."
          },
          {
            "question": "Where is food stored before digestion?",
            "choices": ["Stomach", "Heart", "Liver", "Kidney"],
            "answer": "Stomach",
            "explanation": "The stomach stores and digests food using acids and enzymes."
          },
          {
            "question": "Which organ absorbs nutrients?",
            "choices": ["Small intestine", "Large intestine", "Stomach", "Kidney"],
            "answer": "Small intestine",
            "explanation": "The small intestine absorbs nutrients into the bloodstream."
          },
          {
            "question": "Which organ removes waste water?",
            "choices": ["Large intestine", "Stomach", "Heart", "Brain"],
            "answer": "Large intestine",
            "explanation": "The large intestine absorbs water and forms solid waste."
          }
        ]
      }
    }
  }

}

SCIENCE_GRADE_9 = {

"Physics":{

"Force and Motion":[

{
"question":"What is force?",
"choices":["Push or pull","Heat","Light","Sound"],
"answer":"Push or pull",
"explanation":"Force is any push or pull that can change motion."
},
{
"question":"Unit of force?",
"choices":["Newton","Joule","Watt","Volt"],
"answer":"Newton",
"explanation":"Force is measured in newtons."
},
{
"question":"Gravity pulls objects?",
"choices":["Toward Earth","Away from Earth","Sideways","Up only"],
"answer":"Toward Earth",
"explanation":"Gravity attracts objects toward the center of Earth."
},
{
"question":"Speed equals?",
"choices":["Distance divided by time","Time divided by distance","Mass times speed","Force divided by time"],
"answer":"Distance divided by time",
"explanation":"Speed measures how fast distance is covered."
},
{
"question":"Friction causes?",
"choices":["Resistance to motion","More speed","No movement change","Energy creation"],
"answer":"Resistance to motion",
"explanation":"Friction slows moving objects."
},

{
"question":"Energy unit?",
"choices":["Joule","Newton","Volt","Ampere"],
"answer":"Joule",
"explanation":"Energy is measured in joules."
},
{
"question":"Light travels fastest in?",
"choices":["Vacuum","Water","Air","Glass"],
"answer":"Vacuum",
"explanation":"Light moves fastest where there is no medium."
},
{
"question":"Sound travels through?",
"choices":["Matter","Vacuum","Light","Nothing"],
"answer":"Matter",
"explanation":"Sound needs a medium like air or water."
},
{
"question":"Heat transfer by contact?",
"choices":["Conduction","Radiation","Reflection","Refraction"],
"answer":"Conduction",
"explanation":"Conduction transfers heat through direct contact."
},
{
"question":"Heat transfer through waves?",
"choices":["Radiation","Conduction","Convection","Reflection"],
"answer":"Radiation",
"explanation":"Radiation transfers heat through electromagnetic waves."
},

{
"question":"Motion means?",
"choices":["Change of position","Standing still","Sleeping","Growing"],
"answer":"Change of position",
"explanation":"Motion occurs when an object changes its position."
},
{
"question":"Balanced forces cause?",
"choices":["No motion change","Acceleration","Falling","Jumping"],
"answer":"No motion change",
"explanation":"Balanced forces cancel each other."
},
{
"question":"Unbalanced forces cause?",
"choices":["Movement change","No motion","Rest only","Silence"],
"answer":"Movement change",
"explanation":"Unbalanced forces change motion."
},
{
"question":"Energy stored in food?",
"choices":["Chemical energy","Light energy","Sound energy","Wind energy"],
"answer":"Chemical energy",
"explanation":"Food contains chemical energy used by the body."
},
{
"question":"Sun provides?",
"choices":["Light and heat","Water","Air","Food"],
"answer":"Light and heat",
"explanation":"The Sun is the main source of energy for Earth."
},

{
"question":"Magnet attracts?",
"choices":["Iron","Plastic","Wood","Paper"],
"answer":"Iron",
"explanation":"Magnets attract magnetic metals like iron."
},
{
"question":"Opposite magnetic poles?",
"choices":["Attract","Repel","Disappear","Break"],
"answer":"Attract",
"explanation":"North and south poles attract each other."
},
{
"question":"Similar magnetic poles?",
"choices":["Repel","Attract","Break","Disappear"],
"answer":"Repel",
"explanation":"Like poles push away from each other."
},
{
"question":"Electric current flows through?",
"choices":["Conductors","Insulators","Air only","Wood"],
"answer":"Conductors",
"explanation":"Conductors allow electricity to flow easily."
},
{
"question":"Example of conductor?",
"choices":["Copper","Plastic","Rubber","Glass"],
"answer":"Copper",
"explanation":"Copper is widely used in electrical wiring."
}
]
}

"CRE": {
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
    }
    {
  "CRE_GRADE_8": {
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
    if "user" not in session:
        return redirect(url_for("login"))

    topics = MathQUESTIONS.get(grade, {}).keys()

    return render_template(
        "topics.html",
        grade=grade,
        topics=topics
    )

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


#============================================Everything Pretech============================================================

#---------------------------------------loading the page------------------------------------------
@app.route("/pretech")
def math_page():
    if "user" not in session:
        return redirect(url_for("login"))

    grade = session.get("grade")
    topics = MathQUESTIONS.get(grade, {}).keys()

    return render_template(
        "pretech.html",
        grade=grade,
        topics=topics
    )

#-----------------------------------------PRETECH TOPICS PAGE------------------------------------------
@app.route("/pretech/<grade>/topics")
def pretech_topics():
    if "user" not in session:
        return redirect(url_for("login"))
     
    grade = str(grade)
    
   
    topics = list(MathQUESTIONS[grade].keys())

    return render_template(
        "pretech.html",
        grade=grade,
        topics=topics
    )

#-------------------------------------PRETECH PRACTICE PAGE----------------------------------------
@app.route("/pretech/<grade>/<topic>")
def pretech_practice(grade, topic):
    if "user" not in session:
        return redirect(url_for('login'))
    topic_questions = Pre_techQuestions.get(str(grade), {}).get(topic, [])

    if not topic_questions:
        return "No questions found for this topic", 404

    # Reset session score when entering topic
    session["score"] = 0

    return render_template(
        "pretechpractice.html",
        grade=grade,
        topic=topic
    )
@app.route("/pretechpractice/<grade>/<topic>/get_question")
def get_math_question(grade, topic):
    if "user" not in session:
        return redirect(url_for("login"))

    topics = Pre_techQuestions.get(grade, {}).keys()

    return render_template(
        "topics.html",
        grade=grade,
        topics=topics
    )

# ----------------- GET RANDOM QUESTION (AJAX) -----------------

@app.route("/mathpractice/<grade>/<topic>/get_question")
def get_math_question(grade, topic):

    topic_questions = Pre_techQuestions.get(str(grade), {}).get(topic, [])

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

# ----------------- LOGOUT -----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ----------------- RUN -----------------

if __name__ == "__main__":
    app.run(debug=True)
