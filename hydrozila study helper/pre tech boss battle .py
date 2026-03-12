import pygame
import random
import sys

pygame.init()

# ---------------- WINDOW ----------------

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hydrozoa Pre-Technical Boss Arena")

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
    {"name":"Workshop Guardian","hp":120,"damage":(10,20)},
    {"name":"Circuit Overlord","hp":140,"damage":(12,25)},
    {"name":"Master Engineer","hp":160,"damage":(15,28)}
]

# ---------------- CBC PRE TECH QUESTIONS ----------------

Pre_techQuestions = {

# ---------------- GRADE 7 ----------------

"7": {

"Workshop Safety": [
{
"question": "What is workshop safety?",
"choices": [
"Observing rules to prevent accidents",
"Working without supervision",
"Using tools quickly",
"Avoiding all machines"
],
"answer": "Observing rules to prevent accidents",
"explanation": "Workshop safety involves following rules and precautions."
},

{
"question": "Which of the following is personal protective equipment?",
"choices": ["Goggles","Notebook","Chair","Ruler"],
"answer": "Goggles",
"explanation": "Goggles protect the eyes from dust and particles."
}
],

"Tools and Equipment": [
{
"question": "What is the function of a claw hammer?",
"choices": [
"Driving and removing nails",
"Measuring length",
"Cutting metal",
"Holding wood"
],
"answer": "Driving and removing nails",
"explanation": "A claw hammer drives nails and removes them."
},

{
"question": "Which tool checks right angles?",
"choices": ["Try square","Spanner","File","Chisel"],
"answer": "Try square",
"explanation": "A try square checks 90° angles."
}
],

"Materials Technology": [
{
"question": "What is seasoning of timber?",
"choices": [
"Drying timber to remove moisture",
"Painting timber",
"Burning timber",
"Polishing timber"
],
"answer": "Drying timber to remove moisture",
"explanation": "Seasoning removes water to make timber stronger."
}
],

"Technical Drawing": [
{
"question": "What is a T-square used for?",
"choices": [
"Drawing horizontal lines",
"Cutting paper",
"Measuring angles",
"Sharpening pencils"
],
"answer": "Drawing horizontal lines",
"explanation": "T-square helps draw straight horizontal lines."
}
],

"Basic Electricity": [
{
"question": "Which material conducts electricity?",
"choices": ["Copper","Rubber","Plastic","Wood"],
"answer": "Copper",
"explanation": "Copper allows electricity to flow easily."
}
],

"Entrepreneurship": [
{
"question": "Who is an entrepreneur?",
"choices": [
"A person who starts a business",
"A teacher",
"A customer",
"An employee"
],
"answer": "A person who starts a business",
"explanation": "Entrepreneurs create and run businesses."
}
]

},

# ---------------- GRADE 8 ----------------

"8": {

"Workshop Safety": [
{
"question": "What should you do before using a machine?",
"choices": [
"Check safety instructions",
"Start it quickly",
"Ignore warnings",
"Touch moving parts"
],
"answer": "Check safety instructions",
"explanation": "Safety instructions prevent accidents."
}
],

"Tools and Equipment": [
{
"question": "Which tool tightens nuts and bolts?",
"choices": ["Spanner","Hammer","Chisel","File"],
"answer": "Spanner",
"explanation": "A spanner is used to tighten or loosen bolts."
}
],

"Materials Technology": [
{
"question": "Which material is commonly used for electrical wiring?",
"choices": ["Copper","Wood","Glass","Rubber"],
"answer": "Copper",
"explanation": "Copper is a good conductor."
}
],

"Technical Drawing": [
{
"question": "Which tool measures angles in drawing?",
"choices": ["Protractor","T-square","Compass","Scale rule"],
"answer": "Protractor",
"explanation": "A protractor measures angles."
}
],

"Basic Electricity": [
{
"question": "What is an electric circuit?",
"choices": [
"A complete path for electricity",
"A broken wire",
"A type of battery",
"A metal plate"
],
"answer": "A complete path for electricity",
"explanation": "Electricity flows in a closed circuit."
}
],

"Entrepreneurship": [
{
"question": "What is capital in business?",
"choices": [
"Money used to start a business",
"Workers in a company",
"Products sold",
"Business losses"
],
"answer": "Money used to start a business",
"explanation": "Capital is money invested to start or run a business."
}
]

},

# ---------------- GRADE 9 ----------------

"9": {

"Workshop Safety": [
{
"question": "Why should machines be switched off after use?",
"choices": [
"To prevent accidents",
"To waste electricity",
"To make noise",
"To test power"
],
"answer": "To prevent accidents",
"explanation": "Switching machines off reduces risk of injury."
}
],

"Tools and Equipment": [
{
"question": "Which tool is used to cut wood accurately?",
"choices": ["Tenon saw","Hammer","File","Spanner"],
"answer": "Tenon saw",
"explanation": "Tenon saws cut wood precisely."
}
],

"Materials Technology": [
{
"question": "Which material is strongest for construction?",
"choices": ["Steel","Rubber","Plastic","Paper"],
"answer": "Steel",
"explanation": "Steel is strong and durable."
}
],

"Technical Drawing": [
{
"question": "What does scale 1:10 mean?",
"choices": [
"Drawing is one tenth of real size",
"Drawing is ten times larger",
"Drawing equals real size",
"Drawing is double size"
],
"answer": "Drawing is one tenth of real size",
"explanation": "1:10 means the drawing is reduced."
}
],

"Basic Electricity": [
{
"question": "What does a switch do in a circuit?",
"choices": [
"Opens or closes the circuit",
"Stores electricity",
"Increases voltage",
"Measures current"
],
"answer": "Opens or closes the circuit",
"explanation": "A switch controls current flow."
}
],

"Entrepreneurship": [
{
"question": "What is marketing?",
"choices": [
"Promoting and selling products",
"Producing goods",
"Repairing machines",
"Counting money"
],
"answer": "Promoting and selling products",
"explanation": "Marketing helps businesses attract customers."
}
]

}

}


# convert substrands

substrands = list(Pre_techQuestions["7"].items())

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

def ask_question(q,category):

    selected=None

    while True:

        screen.fill(DEEP_BLUE)

        draw_text(category,50,40,small_font)
        draw_text(q["question"],50,80)

        draw_text("Press 1-4 to answer",50,500,small_font)

        for i,opt in enumerate(q["choices"]):

            rect = pygame.Rect(80,200+i*60,500,40)

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

                if selected is not None:

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

        category,questions=random.choice(substrands)

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


# ---------------- LEVEL SYSTEM ----------------

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

        draw_text("YOU MASTERED PRE-TECH!",250,250)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
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