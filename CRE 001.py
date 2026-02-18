import pygame
import random
import sys
import json
import os

pygame.init()
pygame.mixer.init()

# ================= WINDOW =================
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEPTUNE PROTOCOL: CRE WARFARE")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 28)
BIG = pygame.font.Font(None, 64)
SMALL = pygame.font.Font(None, 22)

# ================= COLORS =================
BG_TOP = (20, 10, 40)
BG_BOTTOM = (60, 0, 80)
NEON_BLUE = (0, 220, 255)
NEON_PURPLE = (170, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 50, 150)
WHITE = (255, 255, 255)
DARK = (20, 20, 40)

# ================= SAVE SYSTEM =================
SAVE_FILE = "cre_save.json"

player_data = {
    "xp": 0,
    "level": 1,
    "coins": 0,
    "upgrades": {"damage": 0, "hp": 0},
    "skills": {"critical": 0, "regen": 0, "energy_blast": 0},
    "achievements": [],
    "progress": {}
}

if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        player_data.update(json.load(f))

def save():
    with open(SAVE_FILE, "w") as f:
        json.dump(player_data, f)

# ==========================================================
# 📖 CRE CBC QUESTION BANK (GRADE 7–9)
# ==========================================================

questions = {

# ================= GRADE 7 =================
"Grade 7": {

    "Creation & God’s Work": [
        {"q":"Who created the world?","o":["God","Moses","David","Paul"],"a":"God"},
        {"q":"How many days did God take to create the world?","o":["6","7","3","10"],"a":"6"},
        {"q":"God rested on which day?","o":["7th day","1st day","3rd day","5th day"],"a":"7th day"}
    ],

    "Bible Knowledge": [
        {"q":"First book of the Bible?","o":["Genesis","Exodus","Matthew","Psalms"],"a":"Genesis"},
        {"q":"Who built the ark?","o":["Noah","Abraham","Peter","Joseph"],"a":"Noah"},
        {"q":"The Ten Commandments were given to?","o":["Moses","David","Paul","Samuel"],"a":"Moses"}
    ]
},

# ================= GRADE 8 =================
"Grade 8": {

    "Life of Jesus": [
        {"q":"Jesus was born in?","o":["Bethlehem","Nazareth","Jerusalem","Egypt"],"a":"Bethlehem"},
        {"q":"Mother of Jesus?","o":["Mary","Martha","Ruth","Esther"],"a":"Mary"},
        {"q":"Jesus performed miracles to show?","o":["God’s power","Anger","Fear","War"],"a":"God’s power"}
    ],

    "Parables & Teachings": [
        {"q":"Parable of the Good Samaritan teaches?","o":["Love others","Hate enemies","Fight","Ignore strangers"],"a":"Love others"},
        {"q":"Jesus taught forgiveness how many times?","o":["70x7","10","5","1"],"a":"70x7"},
        {"q":"Golden Rule says?","o":["Do to others as you want them to do to you","Take revenge","Be silent","Work alone"],"a":"Do to others as you want them to do to you"}
    ]
},

# ================= GRADE 9 =================
"Grade 9": {

    "Church & Mission": [
        {"q":"Disciples were also called?","o":["Apostles","Prophets","Kings","Judges"],"a":"Apostles"},
        {"q":"Holy Spirit came during?","o":["Pentecost","Christmas","Easter","Passover"],"a":"Pentecost"},
        {"q":"Church means?","o":["Body of believers","Building only","Priest only","Choir"],"a":"Body of believers"}
    ],

    "Christian Living": [
        {"q":"Fruit of the Spirit includes?","o":["Love","Anger","Pride","Jealousy"],"a":"Love"},
        {"q":"Prayer is communication with?","o":["God","Pastor","Friend","Angel"],"a":"God"},
        {"q":"Faith means?","o":["Trust in God","Fear","Doubt","Silence"],"a":"Trust in God"}
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

# ================= FLOATING TEXT =================
class Floating:
    def __init__(self, text, pos, color):
        self.text = text
        self.pos = list(pos)
        self.color = color
        self.life = 60

    def update(self):
        self.pos[1] -= 1
        self.life -= 1

    def draw(self):
        t = FONT.render(self.text, True, self.color)
        screen.blit(t, self.pos)

# ================= GAME =================
class Game:
    def __init__(self):
        self.state = "menu"
        self.grade = "Grade 7"
        self.substrand = None
        self.q_list = []
        self.index = 0
        self.buttons = []
        self.player_hp = 200
        self.boss_hp = 600
        self.phase = 1
        self.floating = []
        self.shield = 1

    def start_battle(self, substrand):
        self.substrand = substrand
        pool = questions[self.grade][substrand]
        self.q_list = random.sample(pool, len(pool))

        self.index = 0
        self.player_hp = 200
        self.boss_hp = 600
        self.phase = 1
        self.shield = 1
        self.load_q()
        self.state = "battle"

    def load_q(self):
        q = self.q_list[self.index]
        random.shuffle(q["o"])
        self.buttons = []
        for i, opt in enumerate(q["o"]):
            self.buttons.append(Button(400, 420 + i*60, 400, 50, opt))

    def answer(self, choice):
        correct = self.q_list[self.index]["a"]

        if choice == correct:
            dmg = 50
            self.boss_hp -= dmg
            self.floating.append(Floating(f"-{dmg}", (900,200), CYAN))
        else:
            self.player_hp -= 30
            self.floating.append(Floating("-30", (200,250), MAGENTA))

        self.index += 1

        if self.index >= len(self.q_list) or self.boss_hp <= 0:
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
            t = BIG.render("CRE WARFARE", True, NEON_BLUE)
            screen.blit(t, (420,200))
            y = 350
            for sub in questions[self.grade]:
                b = Button(450,y,300,60,sub)
                b.draw()
                if pygame.mouse.get_pressed()[0] and b.rect.collidepoint(pygame.mouse.get_pos()):
                    self.start_battle(sub)
                y += 80

        elif self.state == "battle":
            pygame.draw.rect(screen, DARK, (50,50,300,20))
            pygame.draw.rect(screen, NEON_BLUE, (50,50,300*(self.player_hp/200),20))

            pygame.draw.rect(screen, DARK, (850,50,300,20))
            pygame.draw.rect(screen, NEON_PURPLE, (850,50,300*(self.boss_hp/600),20))

            q = FONT.render(self.q_list[self.index]["q"], True, WHITE)
            screen.blit(q, (400,350))

            for b in self.buttons:
                b.draw()

            for f in self.floating:
                f.draw()

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

    for f in game.floating:
        f.update()

    game.floating = [f for f in game.floating if f.life > 0]

    game.draw()
    pygame.display.update()

pygame.quit()
sys.exit()
