import pygame
import random
import sys

pygame.init()

# ---------------- WINDOW ----------------
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Agri Boss Arena 🌾")

font = pygame.font.SysFont("arial", 28)
small_font = pygame.font.SysFont("arial", 22)
clock = pygame.time.Clock()

# ---------------- COLORS ----------------
DEEP_BLUE = (5,10,48)
DARK_PURPLE = (26,0,51)
NEON_BLUE = (0,207,255)
WHITE = (255,255,255)

# ---------------- PLAYER ----------------
player = {
    "hp": 100,
    "max_hp": 100,
    "xp": 0,
    "level": 1,
    "coins": 0,
    "streak": 0,
    "potions": 2
}

# ---------------- BOSSES ----------------
bosses = [
    {"name": "Soil Guardian", "hp": 120, "damage": (10,20), "weakness": "Soil"},
    {"name": "Crop Master", "hp": 140, "damage": (12,25), "weakness": "Crop"},
    {"name": "Agri Tycoon", "hp": 170, "damage": (15,30), "weakness": "Entrepreneurship"}
]

# ---------------- AGRI QUESTIONS ----------------
AgriQUESTIONS = {
    "Grade 7": {
        "Soil Management": {
            "Soil Types": [
                {"question":"Best soil for farming?","choices":["Loam","Sand","Clay","Rock"],"answer":"Loam","explanation":"Loam is best for crops."},
                {"question":"Soil erosion is caused by?","choices":["Wind and water","Plastic","Metal","Fire"],"answer":"Wind and water","explanation":"Erosion removes topsoil."}
            ]
        }
    },
    "Grade 8": {
        "Soil Management": {
            "Soil Types": [
                {"question":"Which soil drains fastest?","choices":["Sandy soil","Clay","Loam","Peat"],"answer":"Sandy soil","explanation":"Large particles drain water quickly."},
                {"question":"Which soil holds most water?","choices":["Clay","Sand","Gravel","Silt"],"answer":"Clay","explanation":"Clay retains water."}
            ]
        }
    },
    "Grade 9": {
        "Agribusiness": {
            "Entrepreneurship": [
                {"question":"Who is an entrepreneur?","choices":["Business owner","Teacher","Farmer","Driver"],"answer":"Business owner","explanation":"They run businesses."},
                {"question":"Profit means?","choices":["Money gained","Loss","Sales","Tax"],"answer":"Money gained","explanation":"Profit is earnings after costs."}
            ]
        }
    }
}

# ---------------- BUILD QUESTIONS ----------------
agri_questions = []
for grade in AgriQUESTIONS:
    for strand in AgriQUESTIONS[grade]:
        for substrand in AgriQUESTIONS[grade][strand]:
            questions = AgriQUESTIONS[grade][strand][substrand]
            category = f"{grade} - {strand} - {substrand}"
            agri_questions.append((category, questions))

# ---------------- UI ----------------
def draw_text(text,x,y,font_obj=font):
    img = font_obj.render(text,True,WHITE)
    screen.blit(img,(x,y))

def draw_bar(x,y,value,max_value):
    pygame.draw.rect(screen,(30,30,30),(x,y,300,25))
    width=int((value/max_value)*300)
    pygame.draw.rect(screen,NEON_BLUE,(x,y,width,25))

def show_message(text):
    screen.fill(DEEP_BLUE)
    draw_text(text,WIDTH//2-200,HEIGHT//2)
    pygame.display.update()
    pygame.time.delay(1200)

# ---------------- QUESTION ----------------
def ask_question(q,category):
    selected=None

    while True:
        screen.fill(DEEP_BLUE)
        draw_text(category,50,40,small_font)
        draw_text(q["question"],50,80)
        draw_text("Press 1-4 | H = Heal",50,500,small_font)

        for i,opt in enumerate(q["choices"]):
            rect=pygame.Rect(80,200+i*60,500,40)
            pygame.draw.rect(screen,DARK_PURPLE,rect)
            draw_text(f"{i+1}. {opt}",100,210+i*60,small_font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.KEYDOWN:

                if event.key == pygame.K_h:
                    if player["potions"] > 0:
                        player["hp"] += 30
                        player["potions"] -= 1
                        if player["hp"] > player["max_hp"]:
                            player["hp"] = player["max_hp"]
                        show_message("❤️ Healed!")

                if event.key==pygame.K_1: selected=0
                if event.key==pygame.K_2: selected=1
                if event.key==pygame.K_3: selected=2
                if event.key==pygame.K_4: selected=3

                if selected!=None:
                    if q["choices"][selected]==q["answer"]:
                        show_message("✅ Correct!")
                        return True
                    else:
                        show_message("❌ Wrong!")
                        show_message(q["explanation"])
                        return False

# ---------------- SHOP ----------------
def shop():
    while True:
        screen.fill(DARK_PURPLE)

        draw_text("SHOP",400,50)
        draw_text(f"Coins: {player['coins']}",50,120)

        draw_text("1. Potion (30 coins)",100,200)
        draw_text("2. +20 Max HP (50 coins)",100,260)
        draw_text("3. Exit",100,320)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.KEYDOWN:

                if event.key==pygame.K_1 and player["coins"]>=30:
                    player["potions"]+=1
                    player["coins"]-=30
                    show_message("Bought Potion!")

                if event.key==pygame.K_2 and player["coins"]>=50:
                    player["max_hp"]+=20
                    player["coins"]-=50
                    show_message("Max HP Up!")

                if event.key==pygame.K_3:
                    return

# ---------------- LEVEL ----------------
def level_up():
    if player["xp"] >= player["level"]*100:
        player["level"] += 1
        player["xp"] = 0
        player["hp"] = player["max_hp"]
        show_message("LEVEL UP!")

# ---------------- BOSS BATTLE ----------------
def boss_battle():

    boss = random.choice(bosses).copy()
    boss["max_hp"] = boss["hp"]

    show_message("🌾 " + boss["name"] + " appeared!")

    while boss["hp"] > 0 and player["hp"] > 0:

        category,questions = random.choice(agri_questions)
        q = random.choice(questions)

        correct = ask_question(q,category)

        if correct:
            player["streak"] += 1

            base = random.randint(15,25)
            combo = player["streak"] * 2

            if boss["weakness"].lower() in category.lower():
                bonus = 10
            else:
                bonus = 0

            dmg = base + combo + bonus
            boss["hp"] -= dmg

            player["xp"] += 20
            player["coins"] += 10

            show_message(f"💥 {dmg} damage! Combo x{player['streak']}")

        else:
            player["streak"] = 0
            dmg = random.randint(*boss["damage"])
            player["hp"] -= dmg
            show_message(f"💢 Took {dmg} damage!")

        # HUD
        screen.fill(DEEP_BLUE)

        draw_text("Boss: "+boss["name"],50,50)
        draw_text("HP",50,120)
        draw_bar(50,150,player["hp"],player["max_hp"])

        draw_text("Boss HP",50,220)
        draw_bar(50,250,boss["hp"],boss["max_hp"])

        draw_text(f"Coins: {player['coins']}",600,50)
        draw_text(f"Potions: {player['potions']}",600,90)
        draw_text(f"Streak: {player['streak']}",600,130)

        pygame.display.update()
        pygame.time.delay(1000)

    if player["hp"] <= 0:
        game_over()
    else:
        player["xp"] += 50
        show_message("🌾 Boss Defeated!")
        level_up()

# ---------------- END STATES ----------------
def game_over():
    while True:
        screen.fill(DARK_PURPLE)
        draw_text("YOU LOST",350,250)
        pygame.display.update()

def victory():
    while True:
        screen.fill(DEEP_BLUE)
        draw_text("YOU WON THE GAME!",250,250)
        pygame.display.update()

# ---------------- MAIN ----------------
def run_game():
    while True:
        boss_battle()
        shop()
        if player["level"] >= 5:
            victory()

run_game()