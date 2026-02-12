import pygame
import random
import sys
import json
import os
import math
import time

pygame.init()
pygame.mixer.init()

# ================= WINDOW =================
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEPTUNE PROTOCOL: OCEANIC SCI-FI RPG")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 28)
BIG = pygame.font.Font(None, 64)
SMALL = pygame.font.Font(None, 22)

# ================= COLORS =================
BG_TOP = (8, 10, 35)
BG_BOTTOM = (35, 0, 80)
NEON_BLUE = (0, 220, 255)
NEON_PURPLE = (170, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 50, 150)
WHITE = (255, 255, 255)
DARK = (20, 20, 40)

# ================= SAVE SYSTEM =================
SAVE_FILE = "save_data.json"

player_data = {
    "xp": 0,
    "level": 1,
    "coins": 0,
    "upgrades": {"damage": 0, "hp": 0, "shield": 0},
    "skills": {"critical": 0, "regen": 0, "energy_blast": 0},
}

if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        player_data.update(json.load(f))

def save():
    with open(SAVE_FILE, "w") as f:
        json.dump(player_data, f)

# ================= QUESTION BANK =================
questions = {

# ================= GRADE 7 =================
"Grade 7": {
    "Integers": [
        {"q":"-8 + 3","o":[-5,5,-11,11],"a":-5},
        {"q":"15 - 22","o":[-7,7,-37,37],"a":-7},
        {"q":"-4 × 6","o":[-24,24,-10,10],"a":-24},
        {"q":"-12 ÷ 3","o":[-4,4,-9,9],"a":-4},
        {"q":"9 + (-14)","o":[-5,5,-23,23],"a":-5}
    ],
    "Fractions":[
        {"q":"1/2 + 1/4","o":[0.75,0.5,1,0.25],"a":0.75},
        {"q":"3/5 - 1/5","o":[0.4,0.2,0.8,0.6],"a":0.4},
        {"q":"2/3 + 1/3","o":[1,0.5,0.75,2],"a":1},
        {"q":"4/8 simplified","o":[0.5,0.25,0.75,1],"a":0.5},
        {"q":"5/10 as decimal","o":[0.5,0.2,0.8,0.1],"a":0.5}
    ]
},

# ================= GRADE 8 =================
"Grade 8": {
    "Linear Equations":[
        {"q":"Solve: 3x = 18","o":[6,3,9,12],"a":6},
        {"q":"Solve: x - 7 = 5","o":[12,-12,2,7],"a":12},
        {"q":"Solve: 5x = 45","o":[9,5,15,40],"a":9},
        {"q":"Solve: x/4 = 6","o":[24,12,10,2],"a":24},
        {"q":"Solve: 2x + 4 = 10","o":[3,4,5,6],"a":3}
    ],
    "Exponents":[
        {"q":"4²","o":[16,8,12,14],"a":16},
        {"q":"3³","o":[27,9,18,6],"a":27},
        {"q":"2⁵","o":[32,16,10,64],"a":32},
        {"q":"5²","o":[25,10,15,20],"a":25},
        {"q":"10²","o":[100,20,200,10],"a":100}
    ]
},

# ================= GRADE 9 =================
"Grade 9": {
    "Quadratics":[
        {"q":"(-3)²","o":[9,-9,6,-6],"a":9},
        {"q":"Factor: x² - 9","o":["(x-3)(x+3)","Prime","(x-9)(x+1)","(x-1)(x-9)"],"a":"(x-3)(x+3)"},
        {"q":"x² = 16","o":["4 or -4",4,-4,8],"a":"4 or -4"},
        {"q":"5² - 20","o":[5,25,-5,0],"a":5},
        {"q":"(-6)²","o":[36,-36,12,-12],"a":36}
    ],
    "Laws of Exponents":[
        {"q":"2² × 2³","o":[32,16,64,8],"a":32},
        {"q":"3³ ÷ 3¹","o":[9,27,3,81],"a":9},
        {"q":"5¹ × 5²","o":[125,25,10,50],"a":125},
        {"q":"10³ ÷ 10²","o":[10,100,1000,1],"a":10},
        {"q":"4¹ × 4¹","o":[16,8,4,12],"a":16}
    ]
}

}

# ================= UI =================
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, NEON_PURPLE, self.rect, border_radius=10)
        pygame.draw.rect(screen, NEON_BLUE, self.rect, 2, border_radius=10)
        txt = FONT.render(str(self.text), True, WHITE)
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, e):
        return e.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(e.pos)

# ================= GAME =================
class Game:
    def __init__(self):
        self.state = "menu"
        self.grade = None
        self.substrand = None
        self.q_list = []
        self.index = 0
        self.buttons = []
        self.player_hp = 200
        self.boss_hp = 600

    def start_battle(self, grade, substrand):
        self.grade = grade
        self.substrand = substrand
        self.q_list = random.sample(
            questions[grade][substrand],
            len(questions[grade][substrand])
        )
        self.index = 0
        self.player_hp = 200 + player_data["upgrades"]["hp"]
        self.boss_hp = 600
        self.load_q()
        self.state = "battle"

    def load_q(self):
        q = self.q_list[self.index]
        random.shuffle(q["o"])
        self.buttons = []
        for i,opt in enumerate(q["o"]):
            self.buttons.append(Button(400,420+i*60,400,50,opt))

    def answer(self, choice):
        correct = self.q_list[self.index]["a"]
        if choice == correct:
            dmg = 40 + player_data["upgrades"]["damage"]
            self.boss_hp -= dmg
        else:
            self.player_hp -= 25

        self.index += 1
        if self.index >= len(self.q_list) or self.boss_hp <= 0:
            player_data["coins"] += 100
            player_data["xp"] += 50
            save()
            self.state = "menu"
        else:
            self.load_q()

    def draw_bg(self):
        for y in range(HEIGHT):
            color = [
                BG_TOP[i] + (BG_BOTTOM[i]-BG_TOP[i])*y/HEIGHT
                for i in range(3)
            ]
            pygame.draw.line(screen, color, (0,y), (WIDTH,y))

    def draw(self):
        self.draw_bg()

        if self.state == "menu":
            t = BIG.render("SELECT GRADE", True, NEON_BLUE)
            screen.blit(t,(400,200))

            y = 350
            for grade in questions.keys():
                b = Button(450,y,300,60,grade)
                b.draw()
                if pygame.mouse.get_pressed()[0] and b.rect.collidepoint(pygame.mouse.get_pos()):
                    self.state = grade
                y += 80

        elif self.state in questions:
            y = 300
            for sub in questions[self.state]:
                b = Button(450,y,300,60,sub)
                b.draw()
                if pygame.mouse.get_pressed()[0] and b.rect.collidepoint(pygame.mouse.get_pos()):
                    self.start_battle(self.state, sub)
                y += 80

        elif self.state == "battle":
            pygame.draw.circle(screen, NEON_BLUE, (200,300), 40)
            pygame.draw.circle(screen, NEON_PURPLE, (900,250), 70)

            pygame.draw.rect(screen, DARK, (50,50,300,20))
            pygame.draw.rect(screen, NEON_BLUE, (50,50,300*(self.player_hp/250),20))

            pygame.draw.rect(screen, DARK, (850,50,300,20))
            pygame.draw.rect(screen, NEON_PURPLE, (850,50,300*(self.boss_hp/700),20))

            q = FONT.render(self.q_list[self.index]["q"], True, WHITE)
            screen.blit(q,(400,350))

            for b in self.buttons:
                b.draw()

# ================= MAIN LOOP =================
game = Game()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game.state == "battle":
            for b in game.buttons:
                if b.clicked(event):
                    game.answer(b.text)

    game.draw()
    pygame.display.update()

pygame.quit()
sys.exit()
