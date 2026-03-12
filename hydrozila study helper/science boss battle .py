import pygame
import random
import sys

pygame.init()

# ---------------- WINDOW ----------------

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hydrozoa Science Boss Arena")

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
    "level":1
}

# ---------------- BOSSES ----------------

bosses = [
    {"name":"Cell Master","hp":120,"damage":(10,20)},
    {"name":"Body System Titan","hp":140,"damage":(12,25)},
    {"name":"Matter Overlord","hp":160,"damage":(15,28)}
]

# ---------------- SCIENCE QUESTIONS ----------------

ScienceQuestions = {

"7": {

"Cells": [

{"question":"Basic unit of life?",
"choices":["Cell","Atom","Organ","Tissue"],
"answer":"Cell",
"explanation":"Cells are the smallest living units."},

{"question":"Which organelle controls the cell?",
"choices":["Nucleus","Ribosome","Vacuole","Chloroplast"],
"answer":"Nucleus",
"explanation":"The nucleus controls cell activities."},

{"question":"Which organelle produces energy?",
"choices":["Mitochondria","Ribosome","Chloroplast","Vacuole"],
"answer":"Mitochondria",
"explanation":"Mitochondria are the powerhouse of the cell."},

{"question":"Which structure controls entry and exit?",
"choices":["Cell membrane","Cell wall","Nucleus","Cytoplasm"],
"answer":"Cell membrane",
"explanation":"The cell membrane regulates substances entering and leaving."},

{"question":"Which organelle contains chlorophyll?",
"choices":["Chloroplast","Mitochondria","Nucleus","Ribosome"],
"answer":"Chloroplast",
"explanation":"Chloroplasts contain chlorophyll."}

],

"Living Things":[

{"question":"Which of these is living?",
"choices":["Tree","Stone","Water","Sand"],
"answer":"Tree",
"explanation":"Living things grow and reproduce."},

{"question":"Living things respond to?",
"choices":["Stimuli","Noise","Gravity","Air"],
"answer":"Stimuli",
"explanation":"Stimuli are environmental changes."}

]

},

"8":{

"Human Body":[

{"question":"Where does digestion begin?",
"choices":["Mouth","Stomach","Liver","Intestine"],
"answer":"Mouth",
"explanation":"Digestion begins in the mouth."},

{"question":"Which organ pumps blood?",
"choices":["Heart","Brain","Kidney","Liver"],
"answer":"Heart",
"explanation":"The heart pumps blood."},

{"question":"Which organ helps breathing?",
"choices":["Lungs","Heart","Liver","Kidney"],
"answer":"Lungs",
"explanation":"Lungs exchange oxygen and carbon dioxide."},

{"question":"Which organ absorbs nutrients?",
"choices":["Small intestine","Large intestine","Stomach","Kidney"],
"answer":"Small intestine",
"explanation":"Most nutrients are absorbed here."}

],

"Respiration":[

{"question":"Which gas do humans inhale?",
"choices":["Oxygen","Carbon dioxide","Nitrogen","Hydrogen"],
"answer":"Oxygen",
"explanation":"Oxygen is used in respiration."},

{"question":"Which gas do humans exhale?",
"choices":["Carbon dioxide","Oxygen","Nitrogen","Helium"],
"answer":"Carbon dioxide",
"explanation":"Carbon dioxide is produced in respiration."}

]

},

"9":{

"Matter":[

{"question":"Which state has fixed shape?",
"choices":["Solid","Liquid","Gas","Plasma"],
"answer":"Solid",
"explanation":"Solids keep their shape."},

{"question":"Which state takes container shape?",
"choices":["Liquid","Solid","Gas","Crystal"],
"answer":"Liquid",
"explanation":"Liquids change shape but keep volume."},

{"question":"Which state fills container?",
"choices":["Gas","Liquid","Solid","Ice"],
"answer":"Gas",
"explanation":"Gases expand to fill space."}

],

"Energy":[

{"question":"Energy of motion?",
"choices":["Kinetic energy","Potential energy","Heat energy","Chemical energy"],
"answer":"Kinetic energy",
"explanation":"Moving objects have kinetic energy."},

{"question":"Stored energy?",
"choices":["Potential energy","Kinetic energy","Light energy","Sound energy"],
"answer":"Potential energy",
"explanation":"Potential energy is stored energy."}

]

}

}

# ---------------- BUILD QUESTION LIST ----------------

science_questions = []

for grade in ScienceQuestions:
    for topic in ScienceQuestions[grade]:
        questions = ScienceQuestions[grade][topic]
        science_questions.append((f"Grade {grade} - {topic}", questions))

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

    draw_text(text,WIDTH//2-150,HEIGHT//2)

    pygame.display.update()

    pygame.time.delay(1200)

# ---------------- QUESTION ----------------

def ask_question(q,category):

    selected=None

    while True:

        screen.fill(DEEP_BLUE)

        draw_text(category,50,40,small_font)
        draw_text(q["question"],50,80)

        draw_text("Press 1-4 to answer",50,500,small_font)

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

                if event.key==pygame.K_1: selected=0
                if event.key==pygame.K_2: selected=1
                if event.key==pygame.K_3: selected=2
                if event.key==pygame.K_4: selected=3

                if selected!=None:

                    if q["choices"][selected]==q["answer"]:
                        show_message("Correct!")
                        return True
                    else:
                        show_message("Wrong!")
                        show_message("Explanation: "+q["explanation"])
                        return False

# ---------------- BOSS BATTLE ----------------

def boss_battle():

    boss=random.choice(bosses).copy()
    boss["max_hp"]=boss["hp"]

    show_message("A wild "+boss["name"]+" appeared!")

    while boss["hp"]>0 and player["hp"]>0:

        category,questions=random.choice(science_questions)

        q=random.choice(questions)

        correct=ask_question(q,category)

        if correct:

            damage=random.randint(20,35)
            boss["hp"]-=damage
            player["xp"]+=20

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

# ---------------- LEVEL ----------------

def level_up():

    if player["xp"]>=player["level"]*100:

        player["level"]+=1
        player["hp"]=100

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

        draw_text("YOU MASTERED SCIENCE!",260,250)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

# ---------------- MAIN ----------------

def run_game():

    for name,questions in science_questions:

        for q in questions:
            ask_question(q,name)

        boss_battle()

    victory()

run_game()