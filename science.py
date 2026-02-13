import random
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hydrozoa_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hydrozoa.db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

APPROVAL_CODE = "HYDRO2026"

# =====================
# DATABASE MODELS
# =====================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20))
    total_score = db.Column(db.Integer, default=0)
    shield = db.Column(db.Boolean, default=True)
    mission_count = db.Column(db.Integer, default=0)
    region = db.Column(db.String(50), default="")

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    grade = db.Column(db.Integer)
    strand = db.Column(db.String(100))
    score = db.Column(db.Integer, default=0)

class StrandProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    grade = db.Column(db.Integer)
    strand = db.Column(db.String(100))
    completed = db.Column(db.Boolean, default=False)

class Badges(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    badge_name = db.Column(db.String(50))
    earned = db.Column(db.Boolean, default=False)

# =====================
# LOGIN MANAGER
# =====================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# =====================
# CBC STRANDS
# =====================

cbc_strands = {
    7: ["Living Things and Environment", "Matter", "Energy and Forces"],
    8: ["Human Body Systems", "Electricity and Magnetism", "Environment and Conservation"],
    9: ["Chemical Reactions", "Forces and Motion", "Earth and Space"]
}

# =====================
# FULL QUESTION BANK FOR GRADES 7-9
# =====================

question_bank = {
    "Living Things and Environment": [
        {"q":"What part of a plant makes food?","options":["Root","Stem","Leaf","Flower"],"answer":"Leaf","difficulty":"easy"},
        {"q":"Which organ pumps blood?","options":["Lungs","Heart","Brain","Kidney"],"answer":"Heart","difficulty":"easy"},
        {"q":"What is the basic unit of life?","options":["Atom","Cell","Molecule","Organ"],"answer":"Cell","difficulty":"easy"},
        {"q":"Which process do plants use to make food?","options":["Respiration","Photosynthesis","Digestion","Excretion"],"answer":"Photosynthesis","difficulty":"medium"},
        {"q":"Which gas is produced during photosynthesis?","options":["Oxygen","Carbon dioxide","Nitrogen","Hydrogen"],"answer":"Oxygen","difficulty":"medium"},
        {"q":"Which kingdom do mushrooms belong to?","options":["Plantae","Fungi","Animalia","Protista"],"answer":"Fungi","difficulty":"medium"}
    ],
    "Matter": [
        {"q":"Which state of matter has fixed shape?","options":["Liquid","Gas","Solid","Plasma"],"answer":"Solid","difficulty":"easy"},
        {"q":"Water boiling point is?","options":["0°C","50°C","100°C","150°C"],"answer":"100°C","difficulty":"easy"},
        {"q":"Which is a mixture?","options":["Salt","Air","Water","Oxygen"],"answer":"Air","difficulty":"medium"},
        {"q":"Density = Mass / ?", "options":["Volume","Length","Area","Weight"],"answer":"Volume","difficulty":"medium"},
        {"q":"Melting point of ice is?","options":["0°C","32°C","100°C","273°C"],"answer":"0°C","difficulty":"easy"},
        {"q":"Which particle has negative charge?","options":["Proton","Electron","Neutron","Photon"],"answer":"Electron","difficulty":"medium"}
    ],
    "Energy and Forces": [
        {"q":"What force pulls objects to Earth?","options":["Magnetism","Friction","Gravity","Electricity"],"answer":"Gravity","difficulty":"easy"},
        {"q":"Which energy is stored in food?","options":["Kinetic","Potential","Chemical","Electrical"],"answer":"Chemical","difficulty":"medium"},
        {"q":"Friction always...","options":["Speeds motion","Slows motion","Has no effect","Creates mass"],"answer":"Slows motion","difficulty":"easy"},
        {"q":"Unit of force is?","options":["Newton","Joule","Watt","Pascal"],"answer":"Newton","difficulty":"medium"},
        {"q":"Energy can neither be created nor...","options":["Used","Destroyed","Transferred","Measured"],"answer":"Destroyed","difficulty":"medium"}
    ],
    "Human Body Systems": [
        {"q":"Which organ pumps blood?","options":["Heart","Lungs","Kidney","Brain"],"answer":"Heart","difficulty":"easy"},
        {"q":"Which system carries oxygen?","options":["Digestive","Respiratory","Circulatory","Excretory"],"answer":"Circulatory","difficulty":"easy"},
        {"q":"Which organ filters blood?","options":["Liver","Kidney","Heart","Lungs"],"answer":"Kidney","difficulty":"medium"},
        {"q":"The brain is part of which system?","options":["Nervous","Circulatory","Respiratory","Digestive"],"answer":"Nervous","difficulty":"medium"}
    ],
    "Electricity and Magnetism": [
        {"q":"Unit of electric current?","options":["Ampere","Volt","Ohm","Watt"],"answer":"Ampere","difficulty":"easy"},
        {"q":"Opposite poles of a magnet...","options":["Attract","Repel","Disappear","Merge"],"answer":"Attract","difficulty":"easy"},
        {"q":"What is resistance measured in?","options":["Ohms","Watts","Joules","Volts"],"answer":"Ohms","difficulty":"medium"}
    ],
    "Environment and Conservation": [
        {"q":"Which is renewable energy?","options":["Coal","Solar","Oil","Gas"],"answer":"Solar","difficulty":"easy"},
        {"q":"Deforestation leads to...","options":["More oxygen","Loss of biodiversity","Cooler climate","Less erosion"],"answer":"Loss of biodiversity","difficulty":"medium"},
        {"q":"Which gas causes global warming?","options":["Oxygen","Carbon dioxide","Nitrogen","Hydrogen"],"answer":"Carbon dioxide","difficulty":"medium"}
    ],
    "Chemical Reactions": [
        {"q":"Water + Sodium gives?","options":["Salt + H2","Salt + O2","Hydrogen + Oxygen","None"],"answer":"Salt + H2","difficulty":"medium"},
        {"q":"Rusting is a reaction with...","options":["Oxygen","Hydrogen","Carbon","Nitrogen"],"answer":"Oxygen","difficulty":"easy"}
    ],
    "Forces and Motion": [
        {"q":"What is acceleration?","options":["Change in velocity","Speed","Force","Mass"],"answer":"Change in velocity","difficulty":"medium"},
        {"q":"F = ma is called?","options":["Newton's 2nd law","Newton's 1st law","Gravity formula","Hooke's law"],"answer":"Newton's 2nd law","difficulty":"medium"}
    ],
    "Earth and Space": [
        {"q":"Earth revolves around?","options":["Moon","Sun","Mars","Venus"],"answer":"Sun","difficulty":"easy"},
        {"q":"The moon's gravity causes?","options":["Wind","Tides","Rain","Earthquakes"],"answer":"Tides","difficulty":"medium"}
    ]
}

# =====================
# QUESTION GENERATORS
# =====================

def generate_question(grade, strand):
    return random.choice(question_bank.get(strand, []))

def generate_ai_question(user_id, grade, strand):
    user_progress = StrandProgress.query.filter_by(user_id=user_id, grade=grade, strand=strand).first()
    if user_progress and user_progress.completed:
        difficulty = "hard"
    elif user_progress and not user_progress.completed:
        difficulty = "medium"
    else:
        difficulty = "easy"
    question_pool = [q for q in question_bank.get(strand, []) if q['difficulty']==difficulty]
    return random.choice(question_pool) if question_pool else {}

# =====================
# AUTH ROUTES
# =====================

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        code = request.form.get("code")
        if role=="school" and code != APPROVAL_CODE:
            flash("Invalid School Approval Code")
            return redirect(url_for("register"))
        hashed_password = generate_password_hash(password)
        new_user = User(username=username,password=hashed_password,role=role)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully!")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid login details")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# =====================
# DASHBOARD
# =====================

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

# =====================
# GRADE & STRAND SELECTION
# =====================

@app.route("/select_grade")
@login_required
def select_grade():
    return render_template("select_grade.html")

@app.route("/select_strand/<int:grade>")
@login_required
def select_strand(grade):
    strands = cbc_strands.get(grade, [])
    return render_template("select_strand.html", grade=grade, strands=strands)

# =====================
# MISSION ROUTE WITH PROGRESS BAR
# =====================

@app.route("/mission/<int:grade>/<strand>", methods=["GET","POST"])
@login_required
def mission(grade, strand):
    if request.method=="POST":
        selected = request.form.get("answer")
        correct = request.form.get("correct")
        if selected == correct:
            current_user.total_score += 10
        else:
            if current_user.shield:
                current_user.shield = False
            else:
                current_user.total_score -= 5
        current_user.mission_count += 1
        db.session.commit()
        if current_user.mission_count >=5:
            current_user.mission_count = 0
            db.session.commit()
            return redirect(url_for("boss_battle", grade=grade, strand=strand))
    question = generate_question(grade,strand)
    progress_percent = (current_user.mission_count / 5) * 100
    return render_template("mission.html", grade=grade, strand=strand, question=question, progress_percent=progress_percent)

# =====================
# BOSS BATTLE
# =====================

@app.route("/boss/<int:grade>/<strand>", methods=["GET","POST"])
@login_required
def boss_battle(grade, strand):
    if "boss_hp" not in session:
        session["boss_hp"] = 100
    if request.method=="POST":
        selected = request.form.get("answer")
        correct = request.form.get("correct")
        if selected==correct:
            session["boss_hp"] -= 20
            current_user.total_score += 20
        else:
            if current_user.shield:
                current_user.shield=False
            else:
                current_user.total_score -= 10
        db.session.commit()
        if session["boss_hp"]<=0:
            session.pop("boss_hp")
            completed = StrandProgress(user_id=current_user.id, grade=grade, strand=strand, completed=True)
            db.session.add(completed)
            db.session.commit()
            return render_template("victory.html")
    question = generate_question(grade,strand)
    return render_template("boss.html", question=question, hp=session["boss_hp"])

# =====================
# LEADERBOARDS
# =====================

@app.route("/leaderboard")
@login_required
def leaderboard():
    users = User.query.order_by(User.total_score.desc()).all()
    return render_template("leaderboard.html", users=users)

@app.route("/leaderboard/<region>")
@login_required
def leaderboard_region(region):
    if region=="national":
        users = User.query.order_by(User.total_score.desc()).limit(50).all()
    else:
        users = User.query.filter_by(region=region).order_by(User.total_score.desc()).all()
    return render_template("leaderboard.html", users=users, region=region)

# =====================
# SCHOOL DASHBOARD
# =====================

@app.route("/school_dashboard")
@login_required
def school_dashboard():
    if current_user.role!="school":
        return redirect(url_for("dashboard"))
    students = User.query.filter_by(role="student").all()
    return render_template("school_dashboard.html", students=students)

# =====================
# RUN APP
# =====================

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
