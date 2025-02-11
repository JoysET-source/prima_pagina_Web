import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__) # engine flask app.py

# collega il database principale
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ricette.db'  # Sostituisci con il tuo URI del database
# il seguente comando serve per gestire piu di un db.
app.config['SQLALCHEMY_BINDS'] = {'users': 'sqlite:///users.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
# questo serve a flask per gestire le librerie wtf e quindi la sicurezza degli user
app.secret_key = os.getenv("SECRET_KEY")
# questo e' per criptare la secret key
bcrypt = Bcrypt(app)
# questo crea il database
db = SQLAlchemy(app)

# specifica il path contenente le ricette caricate
ricette_path = os.path.join("static", "Ricette")

# carica le ricette in categoria.html per la visualizzazione grafica e restituisce json
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
                        ricette.append({"image": image_path, "description": description}) # restituzione json
                        # questo serve per il debugging se non carica immagini e/o testo inserito
                        # print(f"Immagine trovata: {image_path}")
                        # print(f"Caricata ricetta: {filename}, descrizione: {description}") questi print aiutano il debug se non passano i dati richiesti
    # else:
        # print(f"Categoria '{categoria}' non trovata in {categoria_path}") come altro print
    return ricette

#  questo chiama struttura come file per interfaccia
@app.route('/')
def home():
    return render_template("struttura.html")

# questo chiama categoria come interfaccia per le ricette uploadate
@app.route("/categoria/<categoria>")
def categoria(categoria):
    ricette = load_ricette(categoria)
    return render_template("categoria.html", categoria=categoria, ricette=ricette)



