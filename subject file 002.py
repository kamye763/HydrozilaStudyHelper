import pygame
import random
import json
import os
import sys



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


class PlayerProfile:
    FILE = "cbc_profile.json"

    def __init__(self):
        self.data = {
            "xp": 0,
            "level": 1,
            "coins": 0,
            "upgrades": {"damage": 0, "hp": 0},
            "skills": {"critical": 0},
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


QUESTIONS = {

"PRETECH": {
    "Grade 7": {
        "Digital Literacy": {
            "Computer Parts": [
                {"q":"Brain of computer?","o":["CPU","Monitor","Mouse","Keyboard"],"a":"CPU"},
                {"q":"Used to type?","o":["Keyboard","Speaker","Printer","Scanner"],"a":"Keyboard"}
            ]
        },
        "Internet Safety": {
            "Online Security": [
                {"q":"Strong password contains?","o":["Letters & symbols","Name only","1234","Birthday"],"a":"Letters & symbols"},
                {"q":"Phishing tries to?","o":["Steal info","Fix RAM","Cook food","Print faster"],"a":"Steal info"}
            ]
        }
    },
    "Grade 8": {
        "Programming Basics": {
            "Variables": [
                {"q":"Used to store data?","o":["Variable","Loop","Mouse","CPU"],"a":"Variable"},
                {"q":"String is?","o":["Text","Number","Device","Loop"],"a":"Text"}
            ]
        }
    },
    "Grade 9": {
        "Programming Concepts": {
            "Functions": [
                {"q":"Function used to?","o":["Reuse code","Delete PC","Format disk","Crash app"],"a":"Reuse code"},
                {"q":"def means?","o":["Define function","Delete file","Debug","Download"],"a":"Define function"}
            ]
        }
    }
},

"SCIENCE": {
    "Grade 7": {
        "Cells": {
            "Cell Structure": [
                {"q":"Basic unit of life?","o":["Cell","Atom","Organ","Tissue"],"a":"Cell"},
                {"q":"Controls the cell?","o":["Nucleus","Ribosome","Vacuole","Chloroplast"],"a":"Nucleus"}
            ]
        }
    },
    "Grade 8": {
        "Human Body": {
            "Body Systems": [
                {"q":"Pumps blood?","o":["Heart","Brain","Kidney","Lungs"],"a":"Heart"},
                {"q":"Carries oxygen?","o":["Circulatory","Digestive","Skeletal","Excretory"],"a":"Circulatory"}
            ]
        }
    },
    "Grade 9": {
        "Chemical Reactions": {
            "Acids and Bases": [
                {"q":"pH less than 7?","o":["Acid","Base","Salt","Water"],"a":"Acid"},
                {"q":"Neutral pH?","o":["7","1","14","0"],"a":"7"}
            ]
        }
    }
},

"CRE": {
    "Grade 7": {
        "Creation": {
            "Genesis": [
                {"q":"Who created the world?","o":["God","Paul","David","Moses"],"a":"God"},
                {"q":"Created in how many days?","o":["6","7","3","10"],"a":"6"}
            ]
        }
    },
    "Grade 8": {
        "Prophets": {
            "Major Prophets": [
                {"q":"Led Israelites from Egypt?","o":["Moses","Paul","Peter","John"],"a":"Moses"},
                {"q":"Built the ark?","o":["Noah","Abraham","David","Samuel"],"a":"Noah"}
            ]
        }
    },
    "Grade 9": {
        "Life of Jesus": {
            "Teachings": [
                {"q":"Golden rule?","o":["Love others","Hate enemies","Ignore people","Fight all"],"a":"Love others"},
                {"q":"Birthplace of Jesus?","o":["Bethlehem","Jerusalem","Nazareth","Rome"],"a":"Bethlehem"}
            ]
        }
    }
},

"AGRICULTURE": {
    "Grade 7": {
        "Crop Production": {
            "Types of Crops": [
                {"q":"Maize is a type of?","o":["Cereal","Fruit","Flower","Root"],"a":"Cereal"},
                {"q":"Beans are classified as?","o":["Legumes","Cereals","Fruits","Tubers"],"a":"Legumes"}
            ]
        },
        "Soil Management": {
            "Soil Types": [
                {"q":"Best soil for farming?","o":["Loam","Sand","Clay only","Rock"],"a":"Loam"},
                {"q":"Soil erosion is caused by?","o":["Wind and water","Plastic","Metal","Fire"],"a":"Wind and water"}
            ]
        }
    },

    "Grade 8": {
        "Livestock Production": {
            "Animal Care": [
                {"q":"Vaccination helps to?","o":["Prevent diseases","Increase weight instantly","Color animals","Make noise"],"a":"Prevent diseases"},
                {"q":"Cows are mainly kept for?","o":["Milk and meat","Wool","Eggs","Honey"],"a":"Milk and meat"}
            ]
        },
        "Farm Tools": {
            "Tool Use": [
                {"q":"Jembe is used for?","o":["Digging","Cutting trees","Spraying","Harvesting milk"],"a":"Digging"},
                {"q":"A tractor is used for?","o":["Ploughing","Cooking","Cleaning house","Typing"],"a":"Ploughing"}
            ]
        }
    },

    "Grade 9": {
        "Agribusiness": {
            "Farm Economics": [
                {"q":"Profit equals?","o":["Income minus expenses","Income plus expenses","Expenses only","Loss only"],"a":"Income minus expenses"},
                {"q":"Marketing means?","o":["Selling products","Planting seeds","Watering crops","Weeding"],"a":"Selling products"}
            ]
        },
        "Environmental Conservation": {
            "Sustainable Farming": [
                {"q":"Crop rotation helps to?","o":["Improve soil fertility","Destroy soil","Increase erosion","Reduce sunlight"],"a":"Improve soil fertility"},
                {"q":"Agroforestry involves?","o":["Growing trees with crops","Cutting all trees","Burning farms","Mining soil"],"a":"Growing trees with crops"}
            ]
        }
    }
},

"IRE":{
  "grade 7"
    "Foundations of Islam": [
        {"q":"Islam means?","o":["Submission to Allah","Peace only","Prayer","Charity"],"a":"Submission to Allah"},
        {"q":"Muslims believe in one?","o":["Allah","Angel","Prophet","Book"],"a":"Allah"},
        {"q":"Holy book of Islam?","o":["Qur'an","Bible","Torah","Zabur"],"a":"Qur'an"}
    ],

    "Articles of Faith": [
        {"q":"How many Articles of Faith are there?","o":["6","5","4","7"],"a":"6"},
        {"q":"Belief in Angels is part of?","o":["Iman","Salah","Zakat","Hajj"],"a":"Iman"},
        {"q":"Last Prophet of Islam?","o":["Muhammad (PBUH)","Isa","Musa","Ibrahim"],"a":"Muhammad (PBUH)"}
    ]
},

# ================= GRADE 8 =================
"Grade 8": {

    "Five Pillars of Islam": [
        {"q":"How many Pillars of Islam?","o":["5","6","4","7"],"a":"5"},
        {"q":"Declaration of faith is called?","o":["Shahada","Salah","Zakat","Sawm"],"a":"Shahada"},
        {"q":"Fasting in Ramadan is called?","o":["Sawm","Hajj","Zakat","Iman"],"a":"Sawm"}
    ],

    "Prayer (Salah)": [
        {"q":"How many daily prayers?","o":["5","3","6","7"],"a":"5"},
        {"q":"Direction of prayer?","o":["Qibla","East","North","Medina"],"a":"Qibla"},
        {"q":"Call to prayer is called?","o":["Adhan","Iqama","Khutba","Dua"],"a":"Adhan"}
    ]
},

# ================= GRADE 9 =================
"Grade 9": {

    "Prophets in Islam": [
        {"q":"Prophet who built the Ark?","o":["Nuh (AS)","Musa (AS)","Isa (AS)","Yusuf (AS)"],"a":"Nuh (AS)"},
        {"q":"Prophet given the Torah?","o":["Musa (AS)","Isa (AS)","Muhammad (PBUH)","Ibrahim (AS)"],"a":"Musa (AS)"},
        {"q":"Prophet known for patience?","o":["Ayyub (AS)","Nuh (AS)","Yunus (AS)","Adam (AS)"],"a":"Ayyub (AS)"}
    ],

    "Islamic Morals": [
        {"q":"Honesty in Islam is called?","o":["Amanah","Zakat","Hajj","Sawm"],"a":"Amanah"},
        {"q":"Helping the poor is done through?","o":["Zakat","Salah","Shahada","Wudu"],"a":"Zakat"},
        {"q":"Good character is called?","o":["Akhlaq","Fiqh","Hadith","Sunnah"],"a":"Akhlaq"}
    ]
}


}


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



class MenuScene:
    def __init__(self, engine, profile, options, next_scene_callback):
        self.engine = engine
        self.profile = profile
        self.next_scene_callback = next_scene_callback

        self.buttons=[]
        y=250
        for opt in options:
            self.buttons.append(Button(400,y,400,60,opt))
            y+=80

    def handle_event(self,event):
        for b in self.buttons:
            if b.clicked(event):
                self.next_scene_callback(b.text)

    def update(self): pass

    def draw(self,screen):
        screen.fill((20,10,50))
        for b in self.buttons:
            b.draw(screen)



class BattleScene:
    def __init__(self,engine,profile,questions):
        self.engine=engine
        self.profile=profile
        self.q_list=questions
        self.index=0

        self.player_hp=200 + profile.data["upgrades"]["hp"]
        self.boss_hp=300 + profile.data["level"]*50

        self.buttons=[]
        self.load_question()

    def load_question(self):
        q=self.q_list[self.index]
        random.shuffle(q["o"])
        self.buttons=[]
        for i,opt in enumerate(q["o"]):
            self.buttons.append(Button(350,420+i*60,500,50,opt))

    def handle_event(self,event):
        for b in self.buttons:
            if b.clicked(event):
                self.answer(b.text)

    def answer(self,choice):
        correct=self.q_list[self.index]["a"]

        if choice==correct:
            dmg=40 + self.profile.data["upgrades"]["damage"]
            if random.random() < 0.1 + self.profile.data["skills"]["critical"]*0.05:
                dmg*=2
            self.boss_hp-=dmg
        else:
            self.player_hp-=30

        self.index+=1

        if self.index>=len(self.q_list) or self.boss_hp<=0 or self.player_hp<=0:
            self.end_battle()
        else:
            self.load_question()

    def end_battle(self):
        self.profile.data["coins"]+=100
        self.profile.add_xp(75)
        self.profile.save()
        self.engine.set_scene(MainMenu(self.engine,self.profile))

    def update(self): pass

    def draw(self,screen):
        screen.fill((15,15,35))

        pygame.draw.rect(screen,(0,220,255),(50,50,300*(self.player_hp/300),20))
        pygame.draw.rect(screen,(170,0,255),(850,50,300*(self.boss_hp/500),20))

        question=pygame.font.Font(None,30).render(
            self.q_list[self.index]["q"],True,(255,255,255)
        )
        screen.blit(question,(350,350))

        for b in self.buttons:
            b.draw(screen)



class MainMenu:
    def __init__(self,engine,profile):
        self.engine=engine
        self.profile=profile

        subjects=list(QUESTIONS.keys())

        self.scene = MenuScene(
            engine,
            profile,
            subjects,
            self.select_subject
        )

    def select_subject(self,subject):
        grades=list(QUESTIONS[subject].keys())

        self.engine.set_scene(
            MenuScene(self.engine,self.profile,grades,
                lambda grade:self.select_grade(subject,grade))
        )

    def select_grade(self,subject,grade):
        strands=list(QUESTIONS[subject][grade].keys())

        self.engine.set_scene(
            MenuScene(self.engine,self.profile,strands,
                lambda strand:self.select_strand(subject,grade,strand))
        )

    def select_strand(self,subject,grade,strand):
        substrands=list(QUESTIONS[subject][grade][strand].keys())

        self.engine.set_scene(
            MenuScene(self.engine,self.profile,substrands,
                lambda sub:self.start_battle(subject,grade,strand,sub))
        )

    def start_battle(self,subject,grade,strand,sub):
        q=QUESTIONS[subject][grade][strand][sub]
        self.engine.set_scene(BattleScene(self.engine,self.profile,q))

    def handle_event(self,event):
        self.scene.handle_event(event)

    def update(self):
        self.scene.update()

    def draw(self,screen):
        self.scene.draw(screen)


if __name__ == "__main__":
    engine = Engine()
    profile = PlayerProfile()
    engine.set_scene(MainMenu(engine,profile))
    engine.run()