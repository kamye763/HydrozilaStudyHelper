import pygame
import random
import sys

pygame.init()

# ---------------- WINDOW ----------------

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hydrozoa Boss Arena")

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
    "xp": 0,
    "level": 1
}

# ---------------- BOSSES ----------------

bosses = [
    {"name":"Abyss Jellylord","hp":120,"damage":(10,20)},
    {"name":"Cosmic Ink Hydra","hp":140,"damage":(12,25)},
    {"name":"Alien Reef Titan","hp":160,"damage":(15,28)}
]

# ---------------- QUESTIONS ----------------

visual_arts = [
{"q":"Mixing red and yellow makes?","o":["Orange","Purple","Green","Blue"],"a":"Orange"},
{"q":"A repeated design is called?","o":["Pattern","Pitch","Noise","Beat"],"a":"Pattern"},
{"q":"Clay art is called?","o":["Pottery","Drawing","Music","Dance"],"a":"Pottery"},
{"q":"Drawing is commonly done on?","o":["Paper","Glass","Stone","Metal"],"a":"Paper"},
{"q":"Blue + Yellow = ?","o":["Green","Red","Purple","Orange"],"a":"Green"}
]

sports = [
{"q":"Players in football team?","o":["11","7","5","15"],"a":"11"},
{"q":"Jumping over a bar?","o":["High jump","Sprint","Swim","Throw"],"a":"High jump"},
{"q":"Throwing heavy ball?","o":["Shot put","Tennis","Hockey","Cricket"],"a":"Shot put"},
{"q":"Exercise improves?","o":["Health","Color","Noise","Rain"],"a":"Health"},
{"q":"Fair play means?","o":["Follow rules","Cheat","Fight","Ignore"],"a":"Follow rules"}
]

performing = [
{"q":"Acting in front of people?","o":["Drama","Running","Drawing","Cooking"],"a":"Drama"},
{"q":"Group singing?","o":["Choir","Team","Class","Band"],"a":"Choir"},
{"q":"Story of play?","o":["Script","Recipe","Map","Song"],"a":"Script"},
{"q":"Where actors perform?","o":["Stage","Road","River","Roof"],"a":"Stage"},
{"q":"Music speed is?","o":["Tempo","Pitch","Shape","Pattern"],"a":"Tempo"}
]

substrands = [
("Visual Arts",visual_arts),
("Sports",sports),
("Performing Arts",performing)
]

# ---------------- UI ----------------

def draw_text(text,x,y,font_obj=font):
    img = font_obj.render(text,True,WHITE)
    screen.blit(img,(x,y))


def draw_bar(x,y,value,max_value):
    pygame.draw.rect(screen,(30,30,30),(x,y,300,25))
    width = int((value/max_value)*300)
    pygame.draw.rect(screen,NEON_BLUE,(x,y,width,25))


# ---------------- MESSAGE ----------------

def show_message(text):

    screen.fill(DEEP_BLUE)

    draw_text(text,WIDTH//2-120,HEIGHT//2)

    pygame.display.update()

    pygame.time.delay(1000)


# ---------------- QUIZ SYSTEM ----------------

def ask_question(q, category):

    selected = None

    while True:

        screen.fill(DEEP_BLUE)

        draw_text(category,50,40,small_font)
        draw_text(q["q"],50,80)

        draw_text("Press 1-4 to answer",50,500,small_font)

        for i,opt in enumerate(q["o"]):

            rect = pygame.Rect(80,200+i*60,500,40)

            pygame.draw.rect(screen,DARK_PURPLE,rect)

            draw_text(f"{i+1}. {opt}",100,210+i*60,small_font)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1: selected = 0
                if event.key == pygame.K_2: selected = 1
                if event.key == pygame.K_3: selected = 2
                if event.key == pygame.K_4: selected = 3

                if selected is not None:

                    if q["o"][selected] == q["a"]:
                        show_message("Correct!")
                        return True
                    else:
                        show_message("Wrong!")
                        return False


# ---------------- BOSS BATTLE ----------------

def boss_battle():

    boss = random.choice(bosses).copy()
    boss["max_hp"] = boss["hp"]

    show_message("A wild "+boss["name"]+" appeared!")

    while boss["hp"] > 0 and player["hp"] > 0:

        q = random.choice(visual_arts + sports + performing)

        correct = ask_question(q,"Boss Question")

        if correct:
            damage = random.randint(20,35)
            boss["hp"] -= damage
            player["xp"] += 20
        else:
            damage = random.randint(*boss["damage"])
            player["hp"] -= damage
            show_message(boss["name"]+" attacked!")

        screen.fill(DEEP_BLUE)

        draw_text("BOSS: "+boss["name"],50,50)

        draw_text("Player HP",50,120)
        draw_bar(50,150,player["hp"],100)

        draw_text("Boss HP",50,220)
        draw_bar(50,250,boss["hp"],boss["max_hp"])

        draw_text("XP",50,320)
        draw_bar(50,350,player["xp"],player["level"]*100)

        draw_text("Level: "+str(player["level"]),50,400)

        pygame.display.update()

        pygame.time.delay(1200)

    if player["hp"] <= 0:
        game_over()
    else:
        player["xp"] += 50
        level_up()


# ---------------- LEVEL SYSTEM ----------------

def level_up():

    if player["xp"] >= player["level"]*100:
        player["level"] += 1
        player["hp"] = 100
        show_message("LEVEL UP!")


# ---------------- GAME OVER ----------------

def game_over():

    while True:

        screen.fill(DARK_PURPLE)

        draw_text("YOU WERE DEFEATED",320,250)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# ---------------- VICTORY ----------------

def victory():

    while True:

        screen.fill(DEEP_BLUE)

        draw_text("YOU DEFEATED ALL BOSSES!",250,250)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# ---------------- MAIN GAME ----------------

def run_game():

    for name,questions in substrands:

        for q in questions:
            ask_question(q,name)

        boss_battle()

    victory()


run_game()