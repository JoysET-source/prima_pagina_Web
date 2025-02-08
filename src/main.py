import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ricette.db'  # Sostituisci con il tuo URI del database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
db = SQLAlchemy(app)

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

