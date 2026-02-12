import pygame
import random
import sys

pygame.init()

# =============================
# SETTINGS
# =============================
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shark Boss Battle")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
menu_font = pygame.font.Font(None, 60)

# =============================
# GAME STATE
# =============================
game_state = "grade_select"
selected_grade = None

player_health = 100
max_player_health = 100

shark_health = 100
max_shark_health = 100

damage_flash = 0
winner_text = ""

"questions"["Grade 7"]["Number"]["Integers"]




# =============================
# BUTTON CLASS
# =============================
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.base_color = (0, 0, 150)
        self.hover_color = (0, 0, 255)

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        pygame.draw.rect(screen, color, self.rect)

        text_surface = font.render(str(self.text), True, (255,255,255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# =============================
# GRADE BUTTONS
# =============================
grade7_btn = Button(350, 200, 300, 60, "Grade 7")
grade8_btn = Button(350, 300, 300, 60, "Grade 8")
grade9_btn = Button(350, 400, 300, 60, "Grade 9")

# =============================
# BATTLE LOGIC
# =============================
current_questions = []
current_index = 0
answer_buttons = []

def start_battle(grade):
    global current_questions, current_index
    global shark_health, max_shark_health
    global player_health

    player_health = 100
    current_questions = random.sample(questions[grade], len(questions[grade]))
    current_index = 0

    if grade == "Grade 7":
        shark_health = max_shark_health = 150
    elif grade == "Grade 8":
        shark_health = max_shark_health = 220
    else:
        shark_health = max_shark_health = 300

    load_question()

def load_question():
    global answer_buttons
    q = current_questions[current_index]
    answer_buttons = []

    for i, option in enumerate(q["options"]):
        btn = Button(300, 350 + i*60, 400, 50, option)
        answer_buttons.append(btn)

# =============================
# MAIN LOOP
# =============================
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "grade_select":
            if grade7_btn.clicked(event):
                selected_grade = "Grade 7"
                start_battle(selected_grade)
                game_state = "battle"

            if grade8_btn.clicked(event):
                selected_grade = "Grade 8"
                start_battle(selected_grade)
                game_state = "battle"

            if grade9_btn.clicked(event):
                selected_grade = "Grade 9"
                start_battle(selected_grade)
                game_state = "battle"

        elif game_state == "battle":
            for btn in answer_buttons:
                if btn.clicked(event):

                    correct = current_questions[current_index]["answer"]

                    if btn.text == correct:
                        damage = 20
                        if shark_health < max_shark_health * 0.3:
                            damage = 30  # boss phase 2
                        shark_health -= damage
                    else:
                        player_health -= 15
                        damage_flash = 15

                    current_index += 1

                    if shark_health <= 0:
                        winner_text = "YOU DEFEATED THE SHARK!"
                        game_state = "game_over"

                    elif player_health <= 0:
                        winner_text = "THE SHARK ATE YOU!"
                        game_state = "game_over"

                    elif current_index >= len(current_questions):
                        winner_text = "OUT OF QUESTIONS!"
                        game_state = "game_over"
                    else:
                        load_question()

        elif game_state == "game_over":
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_state = "grade_select"

    # ================= DRAW =================
    screen.fill((0, 105, 148))

    if damage_flash > 0:
        flash = pygame.Surface((WIDTH, HEIGHT))
        flash.set_alpha(100)
        flash.fill((255, 0, 0))
        screen.blit(flash, (0, 0))
        damage_flash -= 1

    if game_state == "grade_select":
        title = menu_font.render("Select Your Grade", True, (255,255,255))
        screen.blit(title, (300, 100))

        grade7_btn.draw()
        grade8_btn.draw()
        grade9_btn.draw()

    elif game_state == "battle":

        q_text = font.render(current_questions[current_index]["question"], True, (255,255,255))
        screen.blit(q_text, (200, 250))

        for btn in answer_buttons:
            btn.draw()

        # Player health bar
        pygame.draw.rect(screen, (255,0,0), (50,50,200,20))
        pygame.draw.rect(screen, (0,255,0),
                         (50,50,200*(player_health/max_player_health),20))

        # Shark health bar
        pygame.draw.rect(screen, (255,0,0), (750,50,200,20))
        pygame.draw.rect(screen, (0,255,0),
                         (750,50,200*(shark_health/max_shark_health),20))

    elif game_state == "game_over":
        text = menu_font.render(winner_text, True, (255,255,255))
        screen.blit(text, (200, 250))

        restart = font.render("Click to return to menu", True, (255,255,255))
        screen.blit(restart, (350, 350))

    pygame.display.update()

pygame.quit()
sys.exit()



import pygame
import random
import sys
import json
import os
import time
import math

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shark Boss Battle - ULTIMATE")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 72)

SAVE_FILE = "save_data.json"
LEADERBOARD_FILE = "leaderboard.json"

QUESTION_TIME = 12
BASE_DAMAGE = 25

# =============================
# DATA SYSTEM
# =============================
player_data = {
    "xp": 0,
    "level": 1,
    "coins": 0,
    "upgrades": {
        "damage": 0,
        "hp": 0,
        "time": 0,
        "shield": 0
    },
    "highscores": []
}

def save_game():
    with open(SAVE_FILE, "w") as f:
        json.dump(player_data, f)

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            player_data.update(json.load(f))

load_game()

# =============================
# QUESTIONS
# =============================
questions = {
    "Grade 7": [
        {"q":"5+7=?", "o":[12,10,13,11], "a":12},
        {"q":"8x6=?", "o":[48,42,36,54], "a":48},
        {"q":"18/3=?", "o":[6,3,9,4], "a":6},
    ],
    "Grade 8": [
        {"q":"2^5=?", "o":[32,16,25,64], "a":32},
        {"q":"√144=?", "o":[12,14,16,10], "a":12},
        {"q":"3x+2=11", "o":[3,2,4,5], "a":3},
    ],
    "Grade 9": [
        {"q":"x²=81", "o":["9 or -9","9","-9","18"], "a":"9 or -9"},
        {"q":"Factor x²-16", "o":["(x-4)(x+4)","Prime","(x-8)","(x-2)(x-8)"], "a":"(x-4)(x+4)"},
    ]
}


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

# =============================
# QUESTIONS
# =============================
questions = {
    "Grade 7": [
        {"question": "What is -5 + 8?", "options": [3, -3, 13, -13], "answer": 3},
        {"question": "What is 12 - 20?", "options": [-8, 8, -12, 12], "answer": -8},
        {"question": "What is -7 - 6?", "options": [-13, 13, -1, 1], "answer": -13},
        {"question": "What is 9 + (-4)?", "options": [5, -5, 13, -13], "answer": 5},
    ],
    "Grade 8": [
        {"question": "What is -15 + 9?", "options": [-6, 6, -24, 24], "answer": -6},
        {"question": "What is 18 - (-7)?", "options": [25, -25, 11, -11], "answer": 25},
        {"question": "What is -12 × 3?", "options": [-36, 36, -15, 15], "answer": -36},
        {"question": "What is -48 ÷ 6?", "options": [-8, 8, -42, 42], "answer": -8},
    ],
    "Grade 9": [
        {"question": "What is (-3)³?", "options": [-27, 27, -9, 9], "answer": -27},
        {"question": "What is -2 × (-8)?", "options": [16, -16, 10, -10], "answer": 16},
        {"question": "What is 6² - 40?", "options": [-4, 4, -76, 76], "answer": -4},
        {"question": "What is (-10)²?", "options": [100, -100, 20, -20], "answer": 100},
    ]
}



# =============================
# BUTTON CLASS
# =============================
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.base_color = (0, 0, 150)
        self.hover_color = (0, 0, 255)

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        pygame.draw.rect(screen, color, self.rect)

        text_surface = font.render(str(self.text), True, (255,255,255))
        screen.blit(text_surface, (self.rect.x + 20, self.rect.y + 10))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# =============================
# GRADE BUTTONS
# =============================
grade7_btn = Button(350, 200, 300, 60, "Grade 7")
grade8_btn = Button(350, 300, 300, 60, "Grade 8")
grade9_btn = Button(350, 400, 300, 60, "Grade 9")

# =============================
# OCEAN ANIMATION
# =============================
waves_offset = 0
bubbles = []

for i in range(20):
    bubbles.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(2, 5)
    ])

def draw_ocean():
    global waves_offset

    screen.fill((0, 105, 148))

    waves_offset += 1

    # Waves
    for i in range(0, WIDTH, 40):
        pygame.draw.circle(screen, (0, 120, 170),
                           (i - waves_offset % 40, 120), 30)

    # Bubbles
    for bubble in bubbles:
        pygame.draw.circle(screen, (200,230,255),
                           (bubble[0], bubble[1]), bubble[2])
        bubble[1] -= 1
        if bubble[1] < 0:
            bubble[0] = random.randint(0, WIDTH)
            bubble[1] = HEIGHT

# =============================
# BATTLE SETUP
# =============================
current_questions = []
current_index = 0
answer_buttons = []

def start_battle(grade):
    global current_questions, current_index, answer_buttons
    global shark_health

    current_questions = random.sample(questions[grade], len(questions[grade]))
    current_index = 0

    if grade == "Grade 7":
        shark_health = 150
    elif grade == "Grade 8":
        shark_health = 220
    else:
        shark_health = 300

    load_question()

def load_question():
    global answer_buttons

    q = current_questions[current_index]
    answer_buttons = []

    for i, option in enumerate(q["options"]):
        btn = Button(300, 350 + i*60, 400, 50, option)
        answer_buttons.append(btn)

# =============================
# MAIN LOOP
# =============================
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "grade_select":

            if grade7_btn.clicked(event):
                selected_grade = "Grade 7"
                start_battle(selected_grade)
                game_state = "battle"

            if grade8_btn.clicked(event):
                selected_grade = "Grade 8"
                start_battle(selected_grade)
                game_state = "battle"

            if grade9_btn.clicked(event):
                selected_grade = "Grade 9"
                start_battle(selected_grade)
                game_state = "battle"

        elif game_state == "battle":

            for btn in answer_buttons:
                if btn.clicked(event):

                    correct_answer = current_questions[current_index]["answer"]

                    if btn.text == correct_answer:
                        shark_health -= 20
                    else:
                        player_health -= 10

                    current_index += 1

                    if current_index >= len(current_questions):
                        game_state = "grade_select"
                    else:
                        load_question()

    # DRAW
    draw_ocean()

    if game_state == "grade_select":
        title = menu_font.render("Select Your Grade", True, (255,255,255))
        screen.blit(title, (300, 100))

        grade7_btn.draw()
        grade8_btn.draw()
        grade9_btn.draw()

    elif game_state == "battle":

        # Question
        q_text = font.render(current_questions[current_index]["question"], True, (255,255,255))
        screen.blit(q_text, (200, 250))

        # Buttons
        for btn in answer_buttons:
            btn.draw()

        # Health Bars
        pygame.draw.rect(screen, (255,0,0), (50,50,200,20))
        pygame.draw.rect(screen, (0,255,0), (50,50,200*(player_health/100),20))

        pygame.draw.rect(screen, (255,0,0), (750,50,200,20))
        pygame.draw.rect(screen, (0,255,0), (750,50,200*(shark_health/300),20))

    pygame.display.update()

pygame.quit()
sys.exit()

# =============================
# QUESTIONS
# =============================
questions = {
    "Grade 7": [
        {"question": "What is -5 + 8?", "options": [3, -3, 13, -13], "answer": 3},
        {"question": "What is 12 - 20?", "options": [-8, 8, -12, 12], "answer": -8},
        {"question": "What is -7 - 6?", "options": [-13, 13, -1, 1], "answer": -13},
        {"question": "What is 9 + (-4)?", "options": [5, -5, 13, -13], "answer": 5},
        {"question": "What is 3/4 + 1/4?", "options": [1, 2, 0, 3], "answer": 1},
        {"question": "What is 15 × 2?", "options": [30, 25, 20, 35], "answer": 30},
        {"question": "What is 49 ÷ 7?", "options": [7, 6, 8, 9], "answer": 7},
    ],
    "Grade 8": [
        {"question": "What is -15 + 9?", "options": [-6, 6, -24, 24], "answer": -6},
        {"question": "What is 18 - (-7)?", "options": [25, -25, 11, -11], "answer": 25},
        {"question": "What is -12 × 3?", "options": [-36, 36, -15, 15], "answer": -36},
        {"question": "What is -48 ÷ 6?", "options": [-8, 8, -42, 42], "answer": -8},
        {"question": "Solve: 3x = 15", "options": [5, 3, 6, 4], "answer": 5},
        {"question": "What is 4²?", "options": [16, 8, 12, 14], "answer": 16},
        {"question": "What is √81?", "options": [9, 8, 7, 6], "answer": 9},
    ],
    "Grade 9": [
        {"question": "What is (-3)³?", "options": [-27, 27, -9, 9], "answer": -27},
        {"question": "What is -2 × (-8)?", "options": [16, -16, 10, -10], "answer": 16},
        {"question": "What is 6² - 40?", "options": [-4, 4, -76, 76], "answer": -4},
        {"question": "What is (-10)²?", "options": [100, -100, 20, -20], "answer": 100},
        {"question": "Solve: x² = 49", "options": [7, -7, 7 or -7, 14], "answer": "7 or -7"},
        {"question": "What is log10(100)?", "options": [2, 1, 10, 100], "answer": 2},
        {"question": "Factor: x² - 9", "options": ["(x-3)(x+3)", "(x-9)(x+1)", "Prime", "(x-1)(x-9)"], "answer": "(x-3)(x+3)"},
    ]
}


# =============================
# BUTTON
# =============================
class Button:
    def __init__(self,x,y,w,h,text):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = text

    def draw(self):
        mouse = pygame.mouse.get_pos()
        color = (0,0,200) if self.rect.collidepoint(mouse) else (0,0,150)
        pygame.draw.rect(screen,color,self.rect,border_radius=12)
        txt = font.render(str(self.text),True,(255,255,255))
        screen.blit(txt,txt.get_rect(center=self.rect.center))

    def clicked(self,event):
        return event.type==pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# =============================
# GAME
# =============================
class Game:
    def __init__(self):
        self.state="cutscene"
        self.grade=None
        self.questions=[]
        self.index=0
        self.player_hp=100
        self.shark_hp=300
        self.phase=1
        self.score=0
        self.correct=0
        self.total=0
        self.timer=0
        self.shark_offset=0

    def start(self,grade):
        self.grade=grade
        self.questions=random.sample(questions[grade],len(questions[grade]))
        self.index=0
        self.player_hp=100+player_data["upgrades"]["hp"]
        self.shark_hp=300+player_data["level"]*10
        self.phase=1
        self.score=0
        self.correct=0
        self.total=0
        self.timer=time.time()
        self.state="battle"
        self.load_question()

    def load_question(self):
        q=self.questions[self.index]
        random.shuffle(q["o"])
        self.buttons=[]
        for i,opt in enumerate(q["o"]):
            self.buttons.append(Button(400,400+i*60,400,50,opt))
        self.timer=time.time()

    def adaptive_ai(self):
        accuracy = self.correct/self.total if self.total>0 else 0
        if accuracy>0.8:
            self.shark_hp+=5
        elif accuracy<0.5:
            self.player_hp+=5

    def boss_phase(self):
        if self.shark_hp<150 and self.phase==1:
            self.phase=2
        if self.shark_hp<75 and self.phase==2:
            self.phase=3

    def shark_attack(self):
        damage=20
        if self.phase==2:
            damage=30
        if self.phase==3:
            damage=45
        if player_data["upgrades"]["shield"]>0:
            player_data["upgrades"]["shield"]-=1
            return
        self.player_hp-=damage

    def answer(self,choice):
        self.total+=1
        correct_ans=self.questions[self.index]["a"]

        if choice==correct_ans:
            self.correct+=1
            damage=BASE_DAMAGE+player_data["upgrades"]["damage"]
            self.shark_hp-=damage
            self.score+=100
        else:
            self.shark_attack()

        self.adaptive_ai()
        self.boss_phase()

        self.index+=1
        if self.index>=len(self.questions):
            self.end_game()
        else:
            self.load_question()

    def end_game(self):
        player_data["coins"]+=self.score//50
        player_data["xp"]+=50
        if player_data["xp"]>=player_data["level"]*150:
            player_data["xp"]=0
            player_data["level"]+=1
        save_game()
        self.state="gameover"

    def update(self):
        self.shark_offset=math.sin(time.time()*2)*10

    def draw(self):
        screen.fill((0,105,148))

        if self.state=="cutscene":
            txt=big_font.render("A Wild Shark Appears!",True,(255,255,255))
            screen.blit(txt,(250,300))

        elif self.state=="battle":
            q=font.render(self.questions[self.index]["q"],True,(255,255,255))
            screen.blit(q,(300,300))

            for b in self.buttons:
                b.draw()

            # Player HP
            pygame.draw.rect(screen,(255,0,0),(50,50,300,20))
            pygame.draw.rect(screen,(0,255,0),(50,50,300*(self.player_hp/200),20))

            # Shark HP
            shark_color=(200,0,0) if self.phase>1 else (0,0,255)
            pygame.draw.rect(screen,(255,0,0),(850,50,300,20))
            pygame.draw.rect(screen,shark_color,(850,50,300*(self.shark_hp/400),20))

            pygame.draw.circle(screen,(100,100,255),
                               (1000,int(200+self.shark_offset)),80)

            screen.blit(font.render(f"Phase {self.phase}",True,(255,255,255)),(950,150))
            screen.blit(font.render(f"Score {self.score}",True,(255,255,255)),(50,100))

        elif self.state=="gameover":
            result="YOU WIN!" if self.shark_hp<=0 else "GAME OVER"
            txt=big_font.render(result,True,(255,255,255))
            screen.blit(txt,(450,300))

# =============================
# MAIN
# =============================
game=Game()

grade_buttons=[
    Button(450,400,300,60,"Grade 7"),
    Button(450,480,300,60,"Grade 8"),
    Button(450,560,300,60,"Grade 9"),
]

running=True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        if game.state=="cutscene":
            if event.type==pygame.MOUSEBUTTONDOWN:
                game.state="menu"

        elif game.state=="menu":
            for btn in grade_buttons:
                if btn.clicked(event):
                    game.start(btn.text)

        elif game.state=="battle":
            for btn in game.buttons:
                if btn.clicked(event):
                    game.answer(btn.text)

        elif game.state=="gameover":
            if event.type==pygame.MOUSEBUTTONDOWN:
                game.state="menu"

    game.update()
    game.draw()

    if game.state=="menu":
        title=big_font.render("Select Grade",True,(255,255,255))
        screen.blit(title,(400,250))
        for btn in grade_buttons:
            btn.draw()

    pygame.display.update()

pygame.quit()
sys.exit()

