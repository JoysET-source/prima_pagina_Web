import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ricette.db'  # Sostituisci con il tuo URI del database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ricette_path = os.path.join("static", "db_Ricette")

def load_ricette(categoria):
    categoria_path = os.path.join(ricette_path, categoria)
    db_Ricette = []
    if os.path.exists(categoria_path):
        for filename in os.listdir(categoria_path):
            if filename.endswith(".jpg"):
                image_path = os.path.join(categoria_path, filename)
                recipe_txt = filename.replace(".jpg",".txt")
                txt_path = os.path.join(categoria_path, recipe_txt)
                if os.path.exists(txt_path):
                    with open(txt_path, "r") as f:
                        description = f.read()
                        db_Ricette.append({"image": image_path, "description": description})
    return db_Ricette


@app.route('/')
def home():
    return render_template("struttura.html")

@app.route("/categoria/<categoria>")
def categoria(categoria):
    ricette = load_ricette(categoria)
    return render_template("categoria.html", categoria=categoria, ricette=ricette)

