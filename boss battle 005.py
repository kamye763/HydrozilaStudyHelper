import pygame
import random
import sys
import json
import os
import time
import math

pygame.init()
pygame.mixer.init()

# ================= SETTINGS =================
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shark Boss Battle - ULTIMATE")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 72)

SAVE_FILE = "save_data.json"

# ================= PLAYER DATA =================
player_data = {
    "xp": 0,
    "level": 1,
    "coins": 0,
    "upgrades": {
        "damage": 0,
        "hp": 0,
        "shield": 0
    }
}

if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        player_data.update(json.load(f))

def save_game():
    with open(SAVE_FILE, "w") as f:
        json.dump(player_data, f)

# ================= QUESTIONS =================
questions = {
    "Grade 7": [
        {"q":"What is -5 + 8?", "o":[3,-3,13,-13], "a":3},
        {"q":"What is 12 - 20?", "o":[-8,8,-12,12], "a":-8},
        {"q":"What is -7 - 6?", "o":[-13,13,-1,1], "a":-13},
        {"q":"What is 9 + (-4)?", "o":[5,-5,13,-13], "a":5},
        {"q":"What is 3/4 + 1/4?", "o":[1,2,0,3], "a":1},
        {"q":"What is 15 × 2?", "o":[30,25,20,35], "a":30},
        {"q":"What is 49 ÷ 7?", "o":[7,6,8,9], "a":7},
    ],
    "Grade 8": [
        {"q":"What is -15 + 9?", "o":[-6,6,-24,24], "a":-6},
        {"q":"What is 18 - (-7)?", "o":[25,-25,11,-11], "a":25},
        {"q":"What is -12 × 3?", "o":[-36,36,-15,15], "a":-36},
        {"q":"What is -48 ÷ 6?", "o":[-8,8,-42,42], "a":-8},
        {"q":"Solve: 3x = 15", "o":[5,3,6,4], "a":5},
        {"q":"What is 4²?", "o":[16,8,12,14], "a":16},
        {"q":"What is √81?", "o":[9,8,7,6], "a":9},
    ],
    "Grade 9": [
        {"q":"What is (-3)³?", "o":[-27,27,-9,9], "a":-27},
        {"q":"What is -2 × (-8)?", "o":[16,-16,10,-10], "a":16},
        {"q":"What is 6² - 40?", "o":[-4,4,-76,76], "a":-4},
        {"q":"What is (-10)²?", "o":[100,-100,20,-20], "a":100},
        {"q":"Solve: x² = 49", "o":["7 or -7",7,-7,14], "a":"7 or -7"},
        {"q":"What is log10(100)?", "o":[2,1,10,100], "a":2},
        {"q":"Factor: x² - 9", "o":["(x-3)(x+3)","Prime","(x-9)(x+1)","(x-1)(x-9)"], "a":"(x-3)(x+3)"},
    ]
}

# ================= BUTTON CLASS =================
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

# ================= GAME CLASS =================
class Game:
    def __init__(self):
        self.state = "cutscene"  # cutscene, menu, battle, gameover
        self.grade = None
        self.questions = []
        self.index = 0
        self.buttons = []
        self.player_hp = 100
        self.shark_hp = 300
        self.phase = 1
        self.score = 0
        self.correct = 0
        self.total = 0
        self.timer = 0
        self.shark_offset = 0

    def start_battle(self, grade):
        self.grade = grade
        self.questions = random.sample(questions[grade], len(questions[grade]))
        self.index = 0
        self.player_hp = 100 + player_data["upgrades"]["hp"]
        self.shark_hp = 300 + player_data["level"] * 10
        self.phase = 1
        self.score = 0
        self.correct = 0
        self.total = 0
        self.state = "battle"
        self.load_question()

    def load_question(self):
        q = self.questions[self.index]
        random.shuffle(q["o"])
        self.buttons = []
        for i,opt in enumerate(q["o"]):
            self.buttons.append(Button(400,400+i*60,400,50,opt))
        self.timer = time.time()

    def adaptive_ai(self):
        accuracy = self.correct/self.total if self.total>0 else 0
        if accuracy>0.8:
            self.shark_hp += 5
        elif accuracy<0.5:
            self.player_hp += 5

    def boss_phase(self):
        if self.shark_hp < 200 and self.phase==1:
            self.phase = 2
        if self.shark_hp < 100 and self.phase==2:
            self.phase = 3

    def shark_attack(self):
        damage = 20
        if self.phase==2:
            damage = 30
        if self.phase==3:
            damage = 50
        if player_data["upgrades"]["shield"]>0:
            player_data["upgrades"]["shield"] -= 1
            return
        self.player_hp -= damage

    def answer(self, choice):
        self.total += 1
        correct_ans = self.questions[self.index]["a"]

        if choice == correct_ans:
            self.correct += 1
            dmg = 25 + player_data["upgrades"]["damage"]
            self.shark_hp -= dmg
            self.score += 100
        else:
            self.shark_attack()

        self.adaptive_ai()
        self.boss_phase()
        self.index += 1

        if self.index >= len(self.questions):
            self.end_game()
        else:
            self.load_question()

    def end_game(self):
        player_data["coins"] += self.score//50
        player_data["xp"] += 50
        if player_data["xp"] >= player_data["level"]*150:
            player_data["xp"] = 0
            player_data["level"] += 1
        save_game()
        self.state = "gameover"

    def update(self):
        self.shark_offset = math.sin(time.time()*2)*15

    def draw(self):
        # ocean background
        screen.fill((0,105,148))
        for i in range(0,WIDTH,40):
            pygame.draw.circle(screen,(0,120,170),(i,int(100 + math.sin(i/20 + time.time()*2)*10)),30)

        # bubbles
        for i in range(20):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            pygame.draw.circle(screen,(200,230,255),(x,y),random.randint(2,5))

        if self.state=="cutscene":
            txt = big_font.render("A Wild Shark Appears!", True, (255,255,255))
            screen.blit(txt, (300,300))
            sub = font.render("Click to continue", True, (255,255,255))
            screen.blit(sub,(450,400))

        elif self.state=="menu":
            title = big_font.render("Select Grade", True, (255,255,255))
            screen.blit(title,(400,250))
            for b in grade_buttons:
                b.draw()

        elif self.state=="battle":
            # question
            q_txt = font.render(self.questions[self.index]["q"], True, (255,255,255))
            screen.blit(q_txt,(400,300))
            for b in self.buttons:
                b.draw()

            # player HP
            pygame.draw.rect(screen,(255,0,0),(50,50,300,20))
            pygame.draw.rect(screen,(0,255,0),(50,50,300*(self.player_hp/200),20))

            # shark HP
            shark_color=(200,0,0) if self.phase>1 else (0,0,255)
            pygame.draw.rect(screen,(255,0,0),(850,50,300,20))
            pygame.draw.rect(screen,shark_color,(850,50,300*(self.shark_hp/400),20))

            # shark graphic
            pygame.draw.circle(screen,(100,100,255),(1000,int(200+self.shark_offset)),80)
            screen.blit(font.render(f"Phase {self.phase}",True,(255,255,255)),(950,150))
            screen.blit(font.render(f"Score {self.score}",True,(255,255,255)),(50,100))

        elif self.state=="gameover":
            result = "YOU WIN!" if self.shark_hp <= 0 else "GAME OVER"
            txt = big_font.render(result, True, (255,255,255))
            screen.blit(txt,(450,300))
            sub = font.render("Click to return to menu", True, (255,255,255))
            screen.blit(sub,(450,400))

# ================= GRADE BUTTONS =================
grade_buttons = [
    Button(450,400,300,60,"Grade 7"),
    Button(450,480,300,60,"Grade 8"),
    Button(450,560,300,60,"Grade 9")
]

# ================= MAIN LOOP =================
game = Game()

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        if game.state=="cutscene":
            if event.type==pygame.MOUSEBUTTONDOWN:
                game.state="menu"

        elif game.state=="menu":
            for b in grade_buttons:
                if b.clicked(event):
                    game.start_battle(b.text)

        elif game.state=="battle":
            for b in game.buttons:
                if b.clicked(event):
                    game.answer(b.text)

        elif game.state=="gameover":
            if event.type==pygame.MOUSEBUTTONDOWN:
                game.state="menu"

    game.update()
    game.draw()
    pygame.display.update()

    

pygame.quit()
sys.exit()
