import random
import pygame 
import sys

player_health = 100
shark_health = 200

def ask_question(question, answer):
    global shark_health
    global player_health
    
    print("\n🦈 Shark asks:")
    print(question)
    
    user_answer = input("Your answer: ")
    
    if user_answer == str(answer):
        print("✅ Correct! You hit the shark!")
        shark_health -= 20
    else:
        print("❌ Wrong! The shark bites you!")
        player_health -= 5

    print(f"Player Health: {player_health}")
    print(f"Shark Health: {shark_health}")

def numbers_battle():
    for i in range(3):
        num1 = random.randint(10, 50)
        num2 = random.randint(10, 50)
        question = f"What is {num1} + {num2}?"
        answer = num1 + num2
        ask_question(question, answer)

print("🌊 WELCOME TO SHARK BOSS BATTLE 🌊")

numbers_battle()

def fractions_battle():
    question = "What is 1/2 + 1/4? (Answer as decimal)"
    answer = 0.75
    ask_question(question, answer)

print("🌊 WELCOME TO SHARK BOSS BATTLE 🌊")

numbers_battle()

if player_health > 0:
    fractions_battle()

if shark_health <= 0:
    print("🎉 You defeated the Shark!")
elif player_health <= 0:
    print("💀 The Shark has defeated you...")

    print("🦈 'You dare enter my coral kingdom?! Solve this!'")


current_question = random.choice(question_list)

buttons = []
font = pygame.font.Font(None, 32)

for i, option in enumerate(current_question["options"]):
    btn = Button(300, 350 + i*60, 400, 50, option, font)
    buttons.append(btn)
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

    for btn in buttons:
        if btn.is_clicked(event):
            if btn.text == current_question["answer"]:
                shark_health -= 20
                print("Correct!")
            else:
                player_health -= 5
                print("Wrong!")
            
            next_question()

            question_surface = font.render(current_question["question"], True, (255,255,255))
screen.blit(question_surface, (200, 200))
if correct:
    screen.fill((0,255,0))
    pygame.display.update()
    pygame.time.delay(200)

background = pygame.image.load("assets/backgrounds/coral_reef.png")
screen.blit(background, (0,0))
questions = {
   "Grade 7": {...},
   "Grade 8": {...},
   "Grade 9": {...}
}

import random

questions = {

    # =========================
    #        GRADE 7
    # =========================
    "Grade 7": {

        "Number": {
            "Integers": [],
            "Factors & Multiples": [],
            "Fractions": [],
            "Decimals": [],
            "Ratios": []
        },

        "Algebra": {
            "Expressions": [],
            "Linear Equations": [],
            "Substitution": []
        },

        "Geometry": {
            "Angles": [],
            "Triangles": [],
            "Quadrilaterals": []
        },

        "Measurement": {
            "Perimeter": [],
            "Area": [],
            "Volume": []
        },

        "Statistics & Probability": {
            "Data Collection": [],
            "Mean Median Mode": [],
            "Basic Probability": []
        }
    },

    # =========================
    #        GRADE 8
    # =========================
    "Grade 8": {

        "Number": {
            "Exponents": [],
            "Standard Form": [],
            "Square Roots": []
        },

        "Algebra": {
            "Linear Equations": [],
            "Simultaneous Equations": [],
            "Factorization": []
        },

        "Geometry": {
            "Transformations": [],
            "Congruence & Similarity": [],
            "Pythagoras": []
        },

        "Measurement": {
            "Surface Area": [],
            "Volume": []
        },

        "Statistics & Probability": {
            "Grouped Data": [],
            "Probability": []
        }
    },

    # =========================
    #        GRADE 9
    # =========================
    "Grade 9": {

        "Number": {
            "Surds": [],
            "Indices Laws": [],
            "Logarithms": []
        },

        "Algebra": {
            "Quadratic Equations": [],
            "Functions": [],
            "Algebraic Fractions": []
        },

        "Geometry": {
            "Trigonometry": [],
            "Circle Theorems": []
        },

        "Measurement": {
            "3D Shapes": [],
            "Bearings": []
        },

        "Statistics & Probability": {
            "Histograms": [],
            "Probability Rules": []
        }
    }
}

def get_battle_questions(grade, strand, substrand, amount=10):
    pool = questions[grade][strand][substrand]
    return random.sample(pool, min(amount, len(pool)))

game_state = "menu"
"menu"
"grade_select"
"strand_select"
"battle"
"correct_animation"
"wrong_animation"
"victory"
"game_over"

self.state = "idle"
"idle"
"attack"
"hurt"
"rage"
"defeated"

Grade :7 → 150 HP
Grade :8 → 220 HP
Grade :9 → 300 HP



questions = {
    "Grade 7": {
        "Number": {
            "Integers": [
                {"question": "What is -5 + 8?",
                 "options": [3, -3, 13, -13],
                 "answer": 3},

                {"question": "What is 12 - 20?",
                 "options": [-8, 8, -12, 12],
                 "answer": -8},

                {"question": "What is -7 - 6?",
                 "options": [-13, 13, -1, 1],
                 "answer": -13},

                {"question": "What is 9 + (-4)?",
                 "options": [5, -5, 13, -13],
                 "answer": 5},

                {"question": "What is -3 + (-6)?",
                 "options": [-9, 9, -3, 3],
                 "answer": -9},

                {"question": "What is 15 + (-10)?",
                 "options": [5, -5, 25, -25],
                 "answer": 5},

                {"question": "What is -12 + 4?",
                 "options": [-8, 8, -16, 16],

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = (0, 0, 150)
        self.hover_color = (0, 0, 255)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        pygame.draw.rect(screen, color, self.rect)

        text_surface = self.font.render(str(self.text), True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + 20, self.rect.y + 10))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

        import pygame
import sys
from button import Button
from questions import get_battle_questions

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shark Boss Battle")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Load assets
background = pygame.image.load("assets/background.png")
shark_frames = [
    pygame.image.load("assets/shark1.png"),
    pygame.image.load("assets/shark2.png")
]

# Shark animation variables
shark_frame_index = 0
animation_timer = 0

player_health = 100
shark_health = 150

questions = get_battle_questions()
current_question_index = 0

def create_buttons(question):
    buttons = []
    for i, option in enumerate(question["options"]):
        btn = Button(300, 350 + i*60, 400, 50, option, font)
        buttons.append(btn)
    return buttons

current_question = questions[current_question_index]
buttons = create_buttons(current_question)

def draw_health_bar(x, y, health, max_health):
    ratio = health / max_health
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 200, 20))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, 200 * ratio, 20))

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for btn in buttons:
            if btn.is_clicked(event):
                if btn.text == current_question["answer"]:
                    shark_health -= 15
                else:
                    player_health -= 10

                current_question_index += 1

                if current_question_index >= len(questions):
                    running = False
                    break

                current_question = questions[current_question_index]
                buttons = create_buttons(current_question)

    # Animate shark
    animation_timer += 1
    if animation_timer >= 30:
        shark_frame_index = (shark_frame_index + 1) % len(shark_frames)
        animation_timer = 0

    # Draw
    screen.blit(background, (0, 0))
    screen.blit(shark_frames[shark_frame_index], (400, 100))

    # Draw question
    question_surface = font.render(current_question["question"], True, (255,255,255))
    screen.blit(question_surface, (200, 250))

    # Draw buttons
    for btn in buttons:
        btn.draw(screen)

    # Draw health
    draw_health_bar(50, 50, player_health, 100)
    draw_health_bar(750, 50, shark_health, 150)

    pygame.display.update()

pygame.quit()
sys.exit()

game_state = "grade_select"
selected_grade = None
menu_font = pygame.font.Font(None, 60)

grade7_button = Button(350, 200, 300, 70, "Grade 7", menu_font)
grade8_button = Button(350, 300, 300, 70, "Grade 8", menu_font)
grade9_button = Button(350, 400, 300, 70, "Grade 9", menu_font)
def get_battle_questions():
def get_battle_questions(grade):
    return random.sample(
        questions[grade]["Number"]["Integers"],
        10
    )
    for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

    if game_state == "grade_select":

        if grade7_button.is_clicked(event):
            selected_grade = "Grade 7"
            questions = get_battle_questions(selected_grade)
            current_question_index = 0
            current_question = questions[current_question_index]
            buttons = create_buttons(current_question)
            game_state = "battle"

        if grade8_button.is_clicked(event):
            selected_grade = "Grade 8"
            questions = get_battle_questions(selected_grade)
            current_question_index = 0
            current_question = questions[current_question_index]
            buttons = create_buttons(current_question)
            game_state = "battle"

        if grade9_button.is_clicked(event):
            selected_grade = "Grade 9"
            questions = get_battle_questions(selected_grade)
            current_question_index = 0
            current_question = questions[current_question_index]
            buttons = create_buttons(current_question)
            game_state = "battle"

    elif game_state == "battle":

        for btn in buttons:
            if btn.is_clicked(event):
                if btn.text == current_question["answer"]:
                    shark_health -= 15
                else:
                    player_health -= 10

                current_question_index += 1

                if current_question_index >= len(questions):
                    running = False
                    break

                current_question = questions[current_question_index]
                buttons = create_buttons(current_question)
if game_state == "grade_select":

    screen.fill((0, 100, 200))

    title = menu_font.render("Select Your Grade", True, (255,255,255))
    screen.blit(title, (300, 100))

    grade7_button.draw(screen)
    grade8_button.draw(screen)
    grade9_button.draw(screen)

elif game_state == "battle":

    screen.blit(background, (0, 0))
    screen.blit(shark_frames[shark_frame_index], (400, 100))

    question_surface = font.render(current_question["question"], True, (255,255,255))
    screen.blit(question_surface, (200, 250))

    for btn in buttons:
        btn.draw(screen)

    draw_health_bar(50, 50, player_health, 100)
    draw_health_bar(750, 50, shark_health, 150)

"Grade 8": {
    "Number": {
        "Integers": [

            {"question": "What is -15 + 9?",
             "options": [-6, 6, -24, 24],
             "answer": -6},

            {"question": "What is 18 - (-7)?",
             "options": [25, -25, 11, -11],
             "answer": 25},

            {"question": "What is -12 × 3?",
             "options": [-36, 36, -15, 15],
             "answer": -36},

            {"question": "What is -48 ÷ 6?",
             "options": [-8, 8, -42, 42],
             "answer": -8},

            {"question": "What is 7 × (-9)?",
             "options": [-63, 63, -16, 16],
             "answer": -63},

            {"question": "What is -5²?",
             "options": [-25, 25, -10, 10],
             "answer": -25},

            {"question": "What is (-4)²?",
             "options": [16, -16, 8, -8],
             "answer": 16},

            {"question": "What is -30 + (-20)?",
             "options": [-50, 50, -10, 10],
             "answer": -50},

            {"question": "What is 45 ÷ (-9)?",
             "options": [-5, 5, -36, 36],
             "answer": -5},

            {"question": "What is -14 - (-6)?",
             "options": [-8, 8, -20, 20],
             "answer": -8}
        ]
    }
}

"Grade 9": {
    "Number": {
        "Integers": [

            {"question": "What is (-3)³?",
             "options": [-27, 27, -9, 9],
             "answer": -27},

            {"question": "What is -2 × (-8)?",
             "options": [16, -16, 10, -10],
             "answer": 16},

            {"question": "What is -100 ÷ (-4)?",
             "options": [25, -25, 96, -96],
             "answer": 25},

            {"question": "What is 6² - 40?",
             "options": [-4, 4, -76, 76],
             "answer": -4},

            {"question": "What is -7³?",
             "options": [-343, 343, -21, 21],
             "answer": -343},

            {"question": "What is (-5)(-6)?",
             "options": [30, -30, 11, -11],
             "answer": 30},

            {"question": "What is -90 + 45?",
             "options": [-45, 45, -135, 135],
             "answer": -45},

            {"question": "What is 81 ÷ (-9)?",
             "options": [-9, 9, -72, 72],
             "answer": -9},

            {"question": "What is (-10)²?",
             "options": [100, -100, 20, -20],
             "answer": 100},

            {"question": "What is -64 ÷ 8?",
             "options": [-8, 8, -72, 72],
             "answer": -8}
        ]
    }
}

import json
def save_game(grade, player_hp, shark_hp):
    data = {
        "last_grade": grade,
        "player_health": player_hp,
        "shark_health": shark_hp
    }

    with open("save.json", "w") as file:
        json.dump(data, file)


def load_game():
    try:
        with open("save.json", "r") as file:
            return json.load(file)
    except:
        return None
save_data = load_game()

if save_data and save_data["last_grade"]:
    selected_grade = save_data["last_grade"]
    player_health = save_data["player_health"]
    shark_health = save_data["shark_health"]
    questions = get_battle_questions(selected_grade)
    current_question_index = 0
    current_question = questions[current_question_index]
    buttons = create_buttons(current_question)
    game_state = "battle"
else:
    game_state = "grade_select"

import random

waves_offset = 0
bubbles = []

# Create initial bubbles
for i in range(20):
    bubbles.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(2, 5)
    ])
def draw_ocean_background():
    global waves_offset

    # Base ocean color
    screen.fill((0, 105, 148))

    # Moving wave layer
    waves_offset += 1
    for i in range(0, WIDTH, 40):
        pygame.draw.circle(
            screen,
            (0, 120, 170),
            (i - waves_offset % 40, 100),
            30
        )

    # Bubbles
    for bubble in bubbles:
        pygame.draw.circle(screen, (200, 230, 255), (bubble[0], bubble[1]), bubble[2])
        bubble[1] -= 1  # Move upward

        if bubble[1] < 0:
            bubble[0] = random.randint(0, WIDTH)
            bubble[1] = HEIGHT
screen.blit(background, (0, 0))
draw_ocean_background()
if game_state == "grade_select"
if game_state == "battle"
for i in range(0, WIDTH, 60):
    pygame.draw.circle(
        screen,
        (0, 80, 130),
        (i + waves_offset % 60, 180),
        40
    )
for i in range(5):
    pygame.draw.line(
        screen,
        (255, 255, 255),
        (i*200 + waves_offset % 200, 0),
        (i*200 + 100 + waves_offset % 200, HEIGHT),
        2
    )




questions = {
    "Grade 7": {
        "Number": {
            "Integers": [
                {"question": "What is -5 + 8?", "answer": 3},
                {"question": "What is 12 - 20?", "answer": -8},
            ],
            "Factors": [
                {"question": "Find the GCF of 12 and 18.", "answer": 6},
            ]
        },
        "Algebra": {
            "Expressions": [
                {"question": "Simplify: 3x + 2x", "answer": "5x"},
            ]
        }
    },

    "Grade 8": {
        "Geometry": {
            "Angles": [
                {"question": "What is the sum of interior angles of a triangle?", "answer": 180}
            ]
        }
    }
}

questions = {
    "Grade 7": {
        "Number": {
            "Integers": [
                {
                    "question": "What is -5 + 8?",
                    "options": [3, -3, 13, -13],
                    "answer": 3
                },
                {
                    "question": "What is 12 - 20?",
                    "options": [-8, 8, -12, 12],
                    "answer": -8
                }
            ]
        }
    }
}





def get_random_questions(grade, strand, substrand, amount=10):
    pool = questions[grade][strand][substrand]
    return random.sample(pool, min(amount, len(pool)))


class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = (0, 0, 150)
        self.hover_color = (0, 0, 255)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surface = self.font.render(str(self.text), True, (255,255,255))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False



def get_random_questions(grade, strand, substrand, amount=10):
    pool = questions[grade][strand][substrand]
    return random.sample(pool, amount)
def start_battle(grade, strand, substrand):
    battle_questions = get_random_questions(grade, strand, substrand, 10)
    
    for q in battle_questions:
        def run_question_scene(q):
            {
                

            }


pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shark Boss Battle")

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 100, 200))  # Ocean background color
    
    pygame.display.update()

pygame.quit()
sys.exit()

class Shark:
    def __init__(self):
        self.frames = [
            pygame.image.load("assets/images/shark1.png"),
            pygame.image.load("assets/images/shark2.png"),
            pygame.image.load("assets/images/shark3.png")
        ]
        self.current_frame = 0
        self.animation_speed = 0.1
        self.counter = 0

    def update(self):
        self.counter += self.animation_speed
        if self.counter >= len(self.frames):
            self.counter = 0
        self.current_frame = int(self.counter)

    def draw(self, screen):
        screen.blit(self.frames[self.current_frame], (400, 200))

        def draw_health_bar(screen, x, y, health, max_health):
    ratio  = health / max_health
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 200, 20))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, 200 * ratio, 20))


































  