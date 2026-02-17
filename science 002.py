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
pygame.display.set_caption("NEPTUNE PROTOCOL: SCIENCE WARFARE")
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
SAVE_FILE = "science_save.json"

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

# ================= SCIENCE QUESTION BANK =================

# ================= EXPANDED SCIENCE QUESTION BANK =================

questions = {

    "Grade 7": {

        "Cells": [
            {"q":"Basic unit of life?","o":["Cell","Atom","Organ","Tissue"],"a":"Cell"},
            {"q":"Controls the cell?","o":["Nucleus","Ribosome","Vacuole","Chloroplast"],"a":"Nucleus"},
            {"q":"Energy factory of cell?","o":["Mitochondria","Nucleus","Membrane","Cytoplasm"],"a":"Mitochondria"},
            {"q":"Plant cells have?","o":["Cell wall","Fur","Bones","Wings"],"a":"Cell wall"},
            {"q":"Photosynthesis occurs in?","o":["Chloroplast","Nucleus","Heart","Skin"],"a":"Chloroplast"},
            {"q":"Cells form?","o":["Tissues","Planets","Atoms","Stars"],"a":"Tissues"}
        ],

        "Matter": [
            {"q":"State with fixed shape?","o":["Solid","Liquid","Gas","Plasma"],"a":"Solid"},
            {"q":"Boiling point of water?","o":["100°C","50°C","0°C","200°C"],"a":"100°C"},
            {"q":"Density = Mass / ?","o":["Volume","Area","Weight","Energy"],"a":"Volume"},
            {"q":"Negatively charged particle?","o":["Electron","Proton","Neutron","Photon"],"a":"Electron"},
            {"q":"Smallest unit of element?","o":["Atom","Cell","Molecule","Organ"],"a":"Atom"},
            {"q":"Air is a?","o":["Mixture","Element","Compound","Solid"],"a":"Mixture"}
        ]
    },

    "Grade 8": {

        "Human Body": [
            {"q":"Pumps blood?","o":["Heart","Brain","Kidney","Lungs"],"a":"Heart"},
            {"q":"Filters blood?","o":["Kidney","Liver","Heart","Lungs"],"a":"Kidney"},
            {"q":"System that carries oxygen?","o":["Circulatory","Digestive","Skeletal","Excretory"],"a":"Circulatory"},
            {"q":"Brain belongs to?","o":["Nervous","Digestive","Respiratory","Muscular"],"a":"Nervous"},
            {"q":"Gas taken during breathing?","o":["Oxygen","Carbon","Nitrogen","Hydrogen"],"a":"Oxygen"}
        ],

        "Energy": [
            {"q":"Energy cannot be created or?","o":["Destroyed","Moved","Measured","Seen"],"a":"Destroyed"},
            {"q":"Unit of force?","o":["Newton","Watt","Volt","Joule"],"a":"Newton"},
            {"q":"F=ma is?","o":["Newton's 2nd Law","Energy Law","Gravity Law","Motion Rule"],"a":"Newton's 2nd Law"},
            {"q":"Stored energy?","o":["Potential","Kinetic","Heat","Light"],"a":"Potential"},
            {"q":"Energy of motion?","o":["Kinetic","Potential","Chemical","Solar"],"a":"Kinetic"}
        ]
    },

    "Grade 9": {

        "Chemical Reactions": [
            {"q":"Rusting needs?","o":["Oxygen","Hydrogen","Carbon","Nitrogen"],"a":"Oxygen"},
            {"q":"pH less than 7 is?","o":["Acid","Base","Salt","Water"],"a":"Acid"},
            {"q":"Neutral pH value?","o":["7","1","14","0"],"a":"7"},
            {"q":"Burning is?","o":["Combustion","Freezing","Melting","Evaporation"],"a":"Combustion"},
            {"q":"H2O is?","o":["Water","Oxygen","Hydrogen","Salt"],"a":"Water"}
        ],

        "Earth and Space": [
            {"q":"Earth revolves around?","o":["Sun","Moon","Mars","Venus"],"a":"Sun"},
            {"q":"Moon causes?","o":["Tides","Rain","Wind","Heat"],"a":"Tides"},
            {"q":"Largest planet?","o":["Jupiter","Earth","Mars","Venus"],"a":"Jupiter"},
            {"q":"Galaxy we live in?","o":["Milky Way","Andromeda","Orion","Pegasus"],"a":"Milky Way"},
            {"q":"Earth rotation causes?","o":["Day and Night","Seasons","Rain","Tides"],"a":"Day and Night"}
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
        self.correct = 0
        self.total = 0

    # ================= LOAD QUESTIONS =================
    def start_battle(self, substrand):
        self.substrand = substrand
        pool = questions[self.grade][substrand]

        if player_data["level"] < 3:
            self.q_list = random.sample(pool, min(5, len(pool)))
        else:
            self.q_list = random.sample(pool, len(pool))

        self.index = 0
        self.player_hp = 200 + player_data["upgrades"]["hp"]
        self.boss_hp = 600 + player_data["level"] * 40
        self.phase = 1
        self.shield = 1
        self.correct = 0
        self.total = 0
        self.load_q()
        self.state = "battle"

    def load_q(self):
        q = self.q_list[self.index]
        random.shuffle(q["o"])
        self.buttons = []
        for i, opt in enumerate(q["o"]):
            self.buttons.append(Button(400, 420 + i*60, 400, 50, opt))

    # ================= BOSS ATTACK =================
    def boss_attack(self):
        dmg = 25 * self.phase
        if self.shield > 0:
            self.shield -= 1
            self.floating.append(Floating("Shield Block!", (200,200), CYAN))
        else:
            self.player_hp -= dmg
            self.floating.append(Floating(f"-{dmg}", (200,250), MAGENTA))

        if self.phase == 3:
            extra = 20
            self.player_hp -= extra
            self.floating.append(Floating(f"ULTIMATE -{extra}", (200,220), MAGENTA))

    # ================= ANSWER LOGIC =================
    def answer(self, choice):
        self.total += 1
        correct = self.q_list[self.index]["a"]

        if choice == correct:
            self.correct += 1
            dmg = 45 + player_data["upgrades"]["damage"]

            if random.random() < 0.1 + player_data["skills"]["critical"]*0.05:
                dmg *= 2
                self.floating.append(Floating("CRITICAL!", (850,150), CYAN))

            if player_data["skills"]["energy_blast"] > 0:
                bonus = 10 * player_data["skills"]["energy_blast"]
                dmg += bonus

            self.boss_hp -= dmg
            self.floating.append(Floating(f"-{dmg}", (900,200), CYAN))
        else:
            self.boss_attack()

        if self.boss_hp < 400: self.phase = 2
        if self.boss_hp < 200: self.phase = 3

        self.index += 1
        if self.index >= len(self.q_list) or self.boss_hp <= 0:
            self.end_boss()
        else:
            self.load_q()

    # ================= END BOSS =================
    def end_boss(self):
        player_data["coins"] += 150
        player_data["xp"] += 75

        xp_needed = player_data["level"] * 150
        if player_data["xp"] >= xp_needed:
            player_data["xp"] -= xp_needed
            player_data["level"] += 1

        player_data["progress"][self.substrand] = True
        self.check_achievements()
        save()
        self.state = "shop"

    # ================= ACHIEVEMENTS =================
    def check_achievements(self):
        if player_data["level"] >= 5 and "Ocean Elite" not in player_data["achievements"]:
            player_data["achievements"].append("Ocean Elite")

    # ================= DRAW =================
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
            t = BIG.render("SCIENCE WARFARE", True, NEON_BLUE)
            screen.blit(t, (350,200))
            y = 350
            for sub in questions[self.grade]:
                b = Button(450,y,300,60,sub)
                b.draw()
                if pygame.mouse.get_pressed()[0] and b.rect.collidepoint(pygame.mouse.get_pos()):
                    self.start_battle(sub)
                y += 80

        elif self.state == "battle":
            pygame.draw.rect(screen, DARK, (50,50,300,20))
            pygame.draw.rect(screen, NEON_BLUE, (50,50,300*(self.player_hp/250),20))

            pygame.draw.rect(screen, DARK, (850,50,300,20))
            pygame.draw.rect(screen, NEON_PURPLE, (850,50,300*(self.boss_hp/800),20))

            q = FONT.render(self.q_list[self.index]["q"], True, WHITE)
            screen.blit(q, (400,350))

            for b in self.buttons:
                b.draw()

            for f in self.floating:
                f.draw()

        elif self.state == "shop":
            title = BIG.render("TECH UPGRADE BAY", True, NEON_BLUE)
            screen.blit(title,(330,150))

            shop_items = [
                ("+10 Damage",50,"damage"),
                ("+20 HP",50,"hp"),
                ("Critical Boost",80,"critical"),
                ("Regen Boost",80,"regen"),
                ("Energy Blast",100,"energy_blast")
            ]

            y = 280
            for name,cost,stat in shop_items:
                b = Button(350,y,500,60,f"{name} - {cost} coins")
                b.draw()
                if pygame.mouse.get_pressed()[0] and b.rect.collidepoint(pygame.mouse.get_pos()):
                    if player_data["coins"] >= cost:
                        player_data["coins"] -= cost
                        if stat in player_data["upgrades"]:
                            player_data["upgrades"][stat] += 10
                        else:
                            player_data["skills"][stat] += 1
                        save()
                y += 70

            cont = Button(450,600,300,50,"Return to Menu")
            cont.draw()
            if pygame.mouse.get_pressed()[0] and cont.rect.collidepoint(pygame.mouse.get_pos()):
                self.state = "menu"

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
