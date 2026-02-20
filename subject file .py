import pygame
import random
import json
import os
import sys

# ==========================================================
# ====================== ENGINE =============================
# ==========================================================

class Engine:
    def __init__(self, width=1200, height=700):
        pygame.init()
        pygame.mixer.init()

        self.WIDTH = width
        self.HEIGHT = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("CBC WARFARE SYSTEM")

        self.clock = pygame.time.Clock()
        self.running = True
        self.active_scene = None

    def set_scene(self, scene):
        self.active_scene = scene

    def run(self):
        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.active_scene:
                    self.active_scene.handle_event(event)

            if self.active_scene:
                self.active_scene.update()
                self.active_scene.draw(self.screen)

            pygame.display.update()

        pygame.quit()
        sys.exit()

# ==========================================================
# ====================== SAVE SYSTEM =======================
# ==========================================================

class PlayerProfile:
    FILE = "cbc_profile.json"

    def __init__(self):
        self.data = {
            "xp": 0,
            "level": 1,
            "coins": 0,
            "upgrades": {"damage": 0, "hp": 0},
            "skills": {"critical": 0, "regen": 0, "energy_blast": 0},
            "achievements": [],
            "progress": {}
        }
        self.load()

    def load(self):
        if os.path.exists(self.FILE):
            with open(self.FILE, "r") as f:
                self.data.update(json.load(f))

    def save(self):
        with open(self.FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def add_xp(self, amount):
        self.data["xp"] += amount
        needed = self.data["level"] * 150
        if self.data["xp"] >= needed:
            self.data["xp"] -= needed
            self.data["level"] += 1

# ==========================================================
# ====================== QUESTIONS =========================
# ==========================================================

QUESTIONS = {
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


"Grade 7": 
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

    "Grade 8": 

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

    "Grade 9": 

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
        ] # type: ignore
    }
}

# ==========================================================
# ====================== UI ================================
# ==========================================================

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen,(170,0,255),self.rect, border_radius=10)
        pygame.draw.rect(screen,(0,220,255),self.rect,2,border_radius=10)
        font = pygame.font.Font(None,28)
        txt = font.render(self.text,True,(255,255,255))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self,event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# ==========================================================
# ====================== MAIN MENU =========================
# ==========================================================

class MainMenu:
    def __init__(self, engine, profile):
        self.engine = engine
        self.profile = profile

        self.buttons = [
            Button(400,250,400,70,"CRE"),
            Button(400,350,400,70,"SCIENCE"),
            Button(400,450,400,70,"PRETECH")
        ]

    def handle_event(self,event):
        for b in self.buttons:
            if b.clicked(event):
                self.engine.set_scene(SubjectMenu(self.engine,self.profile,b.text))

    def update(self): pass

    def draw(self,screen):
        screen.fill((20,10,50))
        title = pygame.font.Font(None,60).render("CBC WARFARE",True,(0,255,255))
        screen.blit(title,(350,150))
        for b in self.buttons:
            b.draw(screen)

# ==========================================================
# ====================== SUBJECT MENU ======================
# ==========================================================

class SubjectMenu:
    def __init__(self,engine,profile,subject):
        self.engine = engine
        self.profile = profile
        self.subject = subject
        self.grade = "Grade 7"

        self.buttons = []
        y = 250
        for strand in QUESTIONS[subject][self.grade]:
            self.buttons.append(Button(350,y,500,70,strand))
            y += 90

    def handle_event(self,event):
        for b in self.buttons:
            if b.clicked(event):
                self.engine.set_scene(
                    BattleScene(self.engine,self.profile,self.subject,self.grade,b.text)
                )

    def update(self): pass

    def draw(self,screen):
        screen.fill((10,0,40))
        title = pygame.font.Font(None,50).render(self.subject,True,(0,255,255))
        screen.blit(title,(500,150))
        for b in self.buttons:
            b.draw(screen)

# ==========================================================
# ====================== BATTLE ============================
# ==========================================================

class BattleScene:
    def __init__(self,engine,profile,subject,grade,strand):
        self.engine = engine
        self.profile = profile
        self.subject = subject
        self.grade = grade
        self.strand = strand

        self.q_list = QUESTIONS[subject][grade][strand]
        self.index = 0

        self.player_hp = 200 + profile.data["upgrades"]["hp"]
        self.boss_hp = 400 + profile.data["level"] * 50

        self.buttons = []
        self.load_question()

    def load_question(self):
        q = self.q_list[self.index]
        random.shuffle(q["o"])
        self.buttons = []
        for i,opt in enumerate(q["o"]):
            self.buttons.append(Button(350,420+i*60,500,50,opt))

    def handle_event(self,event):
        for b in self.buttons:
            if b.clicked(event):
                self.answer(b.text)

    def answer(self,choice):
        correct = self.q_list[self.index]["a"]

        if choice == correct:
            dmg = 40 + self.profile.data["upgrades"]["damage"]
            if random.random() < 0.1 + self.profile.data["skills"]["critical"]*0.05:
                dmg *= 2
            self.boss_hp -= dmg
        else:
            self.player_hp -= 35

        self.index += 1

        if self.index >= len(self.q_list) or self.boss_hp <= 0:
            self.end_battle()
        else:
            self.load_question()

    def end_battle(self):
        self.profile.data["coins"] += 100
        self.profile.add_xp(75)
        self.profile.save()
        self.engine.set_scene(ShopScene(self.engine,self.profile))

    def update(self): pass

    def draw(self,screen):
        screen.fill((20,20,40))
        pygame.draw.rect(screen,(0,220,255),(50,50,300*(self.player_hp/300),20))
        pygame.draw.rect(screen,(170,0,255),(850,50,300*(self.boss_hp/800),20))
        question = pygame.font.Font(None,30).render(
            self.q_list[self.index]["q"],True,(255,255,255)
        )
        screen.blit(question,(350,350))
        for b in self.buttons:
            b.draw(screen)

# ==========================================================
# ====================== SHOP ==============================
# ==========================================================

class ShopScene:
    def __init__(self,engine,profile):
        self.engine = engine
        self.profile = profile

        self.items = [
            ("+10 Damage",50,"damage"),
            ("+20 HP",50,"hp"),
            ("Critical Boost",80,"critical"),
            ("Energy Blast",100,"energy_blast")
        ]

        self.buttons=[]
        y=250
        for name,cost,stat in self.items:
            self.buttons.append(Button(300,y,600,60,f"{name} - {cost} coins"))
            y+=80

        self.return_btn=Button(400,600,400,60,"Return to Menu")

    def handle_event(self,event):
        for i,b in enumerate(self.buttons):
            if b.clicked(event):
                name,cost,stat=self.items[i]
                if self.profile.data["coins"]>=cost:
                    self.profile.data["coins"]-=cost
                    if stat in self.profile.data["upgrades"]:
                        self.profile.data["upgrades"][stat]+=10
                    else:
                        self.profile.data["skills"][stat]+=1
                    self.profile.save()

        if self.return_btn.clicked(event):
            self.engine.set_scene(MainMenu(self.engine,self.profile))

    def update(self): pass

    def draw(self,screen):
        screen.fill((30,0,60))
        title=pygame.font.Font(None,50).render("TECH SHOP",True,(0,255,255))
        screen.blit(title,(450,150))
        for b in self.buttons:
            b.draw(screen)
        self.return_btn.draw(screen)

# ==========================================================
# ====================== START SYSTEM ======================
# ==========================================================

if __name__ == "__main__":
    engine = Engine()
    profile = PlayerProfile()
    engine.set_scene(MainMenu(engine,profile))
    engine.run()