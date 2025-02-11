import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required
from dotenv import load_dotenv
from models import User

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ricette.db'  # Sostituisci con il tuo URI del database
# il seguente comando serve per gestire piu di un db.
app.config['SQLALCHEMY_BINDS'] = {'users': 'sqlite:///users.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = os.getenv("SECRET_KEY")

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

ricette_path = os.path.join("static", "Ricette")

def load_ricette(categoria):
    categoria_path = os.path.join(ricette_path, categoria)
    ricette = []
    if os.path.exists(categoria_path):
        for filename in os.listdir(categoria_path):
            if filename.endswith(".jpg"):
                image_path = f"Ricette/{categoria}/{filename}"  # Rimuovi "static" dal percorso
                recipe_txt = filename.replace(".jpg", ".txt")
                txt_path = os.path.join(categoria_path, recipe_txt)
                if os.path.exists(txt_path):
                    with open(txt_path, "r") as f:
                        description = f.read()
                        ricette.append({"image": image_path, "description": description})
                        # print(f"Immagine trovata: {image_path}")
                        # print(f"Caricata ricetta: {filename}, descrizione: {description}") questi print aiutano il debug se non passano i dati richiesti
    # else:
        # print(f"Categoria '{categoria}' non trovata in {categoria_path}") come altro print
    return ricette

@app.route('/')
def home():
    return render_template("struttura.html")

@app.route("/categoria/<categoria>")
def categoria(categoria):
    ricette = load_ricette(categoria)
    return render_template("categoria.html", categoria=categoria, ricette=ricette)

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

