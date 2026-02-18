# ==========================================================
# 1️⃣ IMPORT LIBRARIES
# ==========================================================

import pygame
import random
import sys
import json
import os

pygame.init()


# ==========================================================
# 2️⃣ WINDOW SETUP
# ==========================================================

WIDTH, HEIGHT = 1150, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PRE-TECH CBC WARFARE")

clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 26)
BIG = pygame.font.Font(None, 60)


# ==========================================================
# 3️⃣ COLORS
# ==========================================================

BG_TOP = (15, 10, 50)
BG_BOTTOM = (40, 0, 90)

BLUE = (0, 200, 255)
PURPLE = (170, 0, 255)
WHITE = (255, 255, 255)
DARK = (20, 20, 40)
RED = (255, 60, 60)


# ==========================================================
# 4️⃣ SAVE SYSTEM
# ==========================================================

SAVE_FILE = "pretech_save.json"

player_data = {
    "xp": 0,
    "level": 1,
    "coins": 0
}

if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        player_data.update(json.load(f))

def save():
    with open(SAVE_FILE, "w") as f:
        json.dump(player_data, f)


# ==========================================================
# 5️⃣ CBC STRUCTURED QUESTION BANK
# ==========================================================

questions = {

# ==========================================================
# 🔵 GRADE 7
# ==========================================================

"Grade 7": {

    # -------- STRAND 1: DIGITAL LITERACY --------
    "Digital Literacy": {

        "Computer Parts": [
            {"q":"Brain of the computer?","o":["CPU","Monitor","Mouse","Keyboard"],"a":"CPU"},
            {"q":"Device used to type?","o":["Keyboard","Printer","Speaker","Scanner"],"a":"Keyboard"},
            {"q":"Output device?","o":["Monitor","Mouse","CPU","RAM"],"a":"Monitor"}
        ],

        "Storage Devices": [
            {"q":"Permanent storage?","o":["Hard Drive","RAM","Mouse","Fan"],"a":"Hard Drive"},
            {"q":"RAM is?","o":["Temporary memory","Permanent memory","Printer","Software"],"a":"Temporary memory"}
        ]
    },

    # -------- STRAND 2: INTERNET SAFETY --------
    "Internet Safety": {

        "Online Security": [
            {"q":"Strong password contains?","o":["Letters & symbols","Name only","Birthday","1234"],"a":"Letters & symbols"},
            {"q":"Do not share your?","o":["Password","Homework","Book","Pen"],"a":"Password"}
        ]
    }
},


# ==========================================================
# 🟣 GRADE 8
# ==========================================================

"Grade 8": {

    # -------- STRAND 1: INTRO TO PROGRAMMING --------
    "Programming Basics": {

        "Variables & Output": [
            {"q":"Used to store data?","o":["Variable","Loop","Mouse","CPU"],"a":"Variable"},
            {"q":"print() does?","o":["Displays output","Deletes file","Shuts down PC","Saves file"],"a":"Displays output"}
        ],

        "Control Structures": [
            {"q":"Loop is used to?","o":["Repeat code","Delete RAM","Fix PC","Create virus"],"a":"Repeat code"},
            {"q":"If statement is used to?","o":["Make decisions","Draw pictures","Open browser","Install app"],"a":"Make decisions"}
        ]
    },

    # -------- STRAND 2: FILE MANAGEMENT --------
    "File Management": {

        "File Types": [
            {"q":".docx is a?","o":["Document file","Image file","Video file","Audio file"],"a":"Document file"},
            {"q":".jpg is a?","o":["Image file","Text file","Program file","Folder"],"a":"Image file"}
        ]
    }
},


# ==========================================================
# 🟢 GRADE 9
# ==========================================================

"Grade 9": {

    # -------- STRAND 1: ADVANCED CODING --------
    "Programming Concepts": {

        "Data Types": [
            {"q":"Whole numbers are?","o":["Integers","Strings","Booleans","Files"],"a":"Integers"},
            {"q":"True or False is?","o":["Boolean","Integer","Loop","Variable"],"a":"Boolean"}
        ],

        "Functions": [
            {"q":"Function is used to?","o":["Reuse code","Delete system","Format disk","Close window"],"a":"Reuse code"},
            {"q":"def is used to?","o":["Define function","Delete file","Debug PC","Download app"],"a":"Define function"}
        ]
    },

    # -------- STRAND 2: CYBER SECURITY --------
    "Cyber Security": {

        "Threats": [
            {"q":"Phishing tries to?","o":["Steal information","Fix RAM","Boost speed","Clean disk"],"a":"Steal information"},
            {"q":"Antivirus is used to?","o":["Remove malware","Increase RAM","Type faster","Create folder"],"a":"Remove malware"}
        ]
    }
}

}


# ==========================================================
# 6️⃣ BUTTON CLASS
# ==========================================================

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, PURPLE, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLUE, self.rect, 2, border_radius=10)

        txt = FONT.render(self.text, True, WHITE)
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


# ==========================================================
# 7️⃣ GAME CLASS
# ==========================================================

class Game:

    def __init__(self):
        self.state = "grade"
        self.grade = None
        self.strand = None
        self.substrand = None
        self.q_list = []
        self.index = 0
        self.buttons = []
        self.player_hp = 200
        self.boss_hp = 400


    # ---------------- START BATTLE ----------------
    def start_battle(self):
        pool = questions[self.grade][self.strand][self.substrand]
        self.q_list = random.sample(pool, len(pool))
        self.index = 0
        self.player_hp = 200
        self.boss_hp = 400
        self.load_question()
        self.state = "battle"


    # ---------------- LOAD QUESTION ----------------
    def load_question(self):
        question = self.q_list[self.index]
        random.shuffle(question["o"])

        self.buttons = []
        for i, option in enumerate(question["o"]):
            self.buttons.append(
                Button(350, 380 + i * 55, 450, 45, option)
            )


    # ---------------- ANSWER SYSTEM ----------------
    def answer(self, choice):

        correct_answer = self.q_list[self.index]["a"]

        if choice == correct_answer:
            self.boss_hp -= 50
        else:
            self.player_hp -= 40

        self.index += 1

        if self.index >= len(self.q_list) or self.boss_hp <= 0:
            self.state = "grade"
        else:
            self.load_question()


    # ---------------- DRAW BACKGROUND ----------------
    def draw_background(self):
        for y in range(HEIGHT):
            color = [
                BG_TOP[i] + (BG_BOTTOM[i] - BG_TOP[i]) * y / HEIGHT
                for i in range(3)
            ]
            pygame.draw.line(screen, color, (0,y), (WIDTH,y))


    # ---------------- DRAW SCREEN ----------------
    def draw(self):

        self.draw_background()

        if self.state == "grade":
            y = 250
            for grade in questions:
                b = Button(400, y, 350, 60, grade)
                b.draw()
                if pygame.mouse.get_pressed()[0] and b.rect.collidepoint(pygame.mouse.get_pos()):
                    self.grade = grade
                    self.state = "strand"
                y += 90

        elif self.state == "strand":
            y = 250
            for strand in questions[self.grade]:
                b = Button(350, y, 450, 60, strand)
                b.draw()
                if pygame.mouse.get_pressed()[0] and b.rect.collidepoint(pygame.mouse.get_pos()):
                    self.strand = strand
                    self.state = "substrand"
                y += 90

        elif self.state == "substrand":
            y = 250
            for sub in questions[self.grade][self.strand]:
                b = Button(350, y, 450, 60, sub)
                b.draw()
                if pygame.mouse.get_pressed()[0] and b.rect.collidepoint(pygame.mouse.get_pos()):
                    self.substrand = sub
                    self.start_battle()
                y += 90

        elif self.state == "battle":

            pygame.draw.rect(screen, DARK, (50,50,300,20))
            pygame.draw.rect(screen, BLUE, (50,50,300*(self.player_hp/200),20))

            pygame.draw.rect(screen, DARK, (750,50,300,20))
            pygame.draw.rect(screen, PURPLE, (750,50,300*(self.boss_hp/400),20))

            question_text = FONT.render(self.q_list[self.index]["q"], True, WHITE)
            screen.blit(question_text, (300,300))

            for button in self.buttons:
                button.draw()


# ==========================================================
# 8️⃣ MAIN LOOP
# ==========================================================

game = Game()
running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game.state == "battle":
            for button in game.buttons:
                if button.clicked(event):
                    game.answer(button.text)

    game.draw()
    pygame.display.update()

pygame.quit()
sys.exit()
