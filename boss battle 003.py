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
shark_health = 150

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
