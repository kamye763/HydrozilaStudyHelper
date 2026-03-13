import pygame
import random
import sys

pygame.init()

# ---------------- WINDOW ----------------

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CRE Boss Arena")

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
    "hp":100,
    "xp":0,
    "level":1,
    "holy_shield":1,
    "faith_power":1
}

# ---------------- BOSSES ----------------

bosses = [
    {"name":"Pharaoh of Doubt","hp":120,"damage":(10,20)},
    {"name":"Roman Governor","hp":150,"damage":(12,25)},
    {"name":"False Prophet","hp":180,"damage":(15,30)}
]

# ---------------- CRE QUESTIONS ----------------

cre = {

 "Grade 7":{
     "Creation":{
         "Genesis":[

         {"q":"Who created the world?",
           "o":["God","Paul","David","Moses"],
           "a":"God"},
         {"q":"Created in how many days?", 
          "o":["6","7","3","10"],
          "a":"6"},
         {"q":"Who was the first man?",
          "o":["Adam","Noah","Moses","Abraham"],
          "a":"Adam"},
         {"q":"Who was the first woman?",
          "o":["Eve","Sarah","Mary","Hagar"],
          "a":"Eve"},
         {"q":"What was created on the first day?",
          "o":["Light","Land","Sun","Stars"],
          "a":"Light"}
]
}
},

 "Grade 8":{
     "Life of Jesus":[

         {"q":"Where was Jesus born?",
          "o":["Bethlehem","Nazareth","Jerusalem","Rome"],
          "a":"Bethlehem"},
         {"q":"Who baptized Jesus?",
          "o":["John the Baptist","Peter","James","Paul"],
          "a":"John the Baptist"},
         {"q":"How many disciples did Jesus have?",
          "o":["12","10","7","15"],
          "a":"12"},
         {"q":"Jesus walked on?",
          "o":["Water","Sand","Mountains","Clouds"],
          "a":"Water"},
         {"q":"Jesus fed 5000 people with?",
          "o":["Five loaves and two fish","Ten loaves","Bread only","Fish only"],
          "a":"Five loaves and two fish"}
]
},

 "Grade 9":{
     "Early Church":[

         {"q":"Which book describes the early church?",
          "o":["Acts","Genesis","Luke","Matthew"],
          "a":"Acts"},
         {"q":"The Holy Spirit came during?",
          "o":["Pentecost","Christmas","Easter","Passover"],
          "a":"Pentecost"},
         {"q":"Who preached the first sermon after Pentecost?",
          "o":["Peter","Paul","James","John"],
          "a":"Peter"},
         {"q":"How many people believed after Peter's sermon?",
          "o":["3000","500","100","50"],
          "a":"3000"},
         {"q":"Who was formerly called Saul?",
          "o":["Paul","Peter","James","Matthew"],
          "a":"Paul"}
]
}

}

# ---------------- BUILD QUESTION LIST ----------------

cre_questions = []

for grade in cre:
    for strand in cre[grade]:
        strand_data = cre[grade][strand]

        if isinstance(strand_data,dict):

            for substrand in strand_data:

                for q in strand_data[substrand]:

                    formatted = {
                        "question":q["q"],
                        "choices":q["o"],
                        "answer":q["a"]
                    }

                    category=f"{grade} - {strand} - {substrand}"

                    cre_questions.append((category,formatted))

        else:

            for q in strand_data:

                formatted = {
                    "question":q["q"],
                    "choices":q["o"],
                    "answer":q["a"]
                }

                category=f"{grade} - {strand}"

                cre_questions.append((category,formatted))

# ---------------- UI ----------------

def draw_text(text,x,y,font_obj=font):

    img = font_obj.render(text,True,WHITE)
    screen.blit(img,(x,y))

def draw_bar(x,y,value,max_value):

    pygame.draw.rect(screen,(30,30,30),(x,y,300,25))

    width=int((value/max_value)*300)

    pygame.draw.rect(screen,NEON_BLUE,(x,y,width,25))

# ---------------- MESSAGE ----------------

def show_message(text):

    screen.fill(DEEP_BLUE)

    draw_text(text,WIDTH//2-200,HEIGHT//2)

    pygame.display.update()

    pygame.time.delay(1300)

# ---------------- QUESTION ----------------

def ask_question(q,category):

    selected=None

    while True:

        screen.fill(DEEP_BLUE)

        draw_text(category,50,40,small_font)
        draw_text(q["question"],50,90)

        draw_text("Press 1-4 | H = Holy Shield | F = Faith Power",50,500,small_font)

        for i,opt in enumerate(q["choices"]):

            rect=pygame.Rect(80,200+i*60,600,40)

            pygame.draw.rect(screen,DARK_PURPLE,rect)

            draw_text(f"{i+1}. {opt}",100,210+i*60,small_font)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.KEYDOWN:

                if event.key==pygame.K_1: selected=0
                if event.key==pygame.K_2: selected=1
                if event.key==pygame.K_3: selected=2
                if event.key==pygame.K_4: selected=3

                if event.key==pygame.K_h and player["holy_shield"]>0:
                    player["holy_shield"]-=1
                    show_message("Holy Shield Activated!")
                    return True

                if event.key==pygame.K_f and player["faith_power"]>0:
                    player["faith_power"]-=1
                    show_message("Faith Power Activated!")
                    return "power"

                if selected!=None:

                    if q["choices"][selected]==q["answer"]:
                        show_message("Correct!")
                        return True
                    else:
                        show_message("Wrong! Answer: "+q["answer"])
                        return False

# ---------------- BOSS BATTLE ----------------

def boss_battle():

    boss=random.choice(bosses).copy()
    boss["max_hp"]=boss["hp"]

    show_message("A wild "+boss["name"]+" appeared!")

    while boss["hp"]>0 and player["hp"]>0:

        category,q=random.choice(cre_questions)

        result=ask_question(q,category)

        if result==True:

            damage=random.randint(20,35)

            boss["hp"]-=damage
            player["xp"]+=20

        elif result=="power":

            damage=random.randint(40,60)

            boss["hp"]-=damage

        else:

            damage=random.randint(*boss["damage"])

            player["hp"]-=damage

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

    if player["hp"]<=0:
        game_over()
    else:
        player["xp"]+=50
        level_up()

# ---------------- LEVEL UP ----------------

def level_up():

    if player["xp"]>=player["level"]*100:

        player["level"]+=1
        player["hp"]=100
        player["holy_shield"]+=1
        player["faith_power"]+=1

        show_message("LEVEL UP!")

# ---------------- GAME OVER ----------------

def game_over():

    while True:

        screen.fill(DARK_PURPLE)

        draw_text("YOU WERE DEFEATED",320,250)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

# ---------------- VICTORY ----------------

def victory():

    while True:

        screen.fill(DEEP_BLUE)

        draw_text("YOU MASTERED CRE!",300,250)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

# ---------------- MAIN ----------------

def run_game():

    for i in range(5):

        boss_battle()

    victory()

run_game()