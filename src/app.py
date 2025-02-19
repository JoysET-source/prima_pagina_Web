import os

from flask import Flask, render_template
from flask import  request, jsonify, url_for, redirect
from flask_login import login_user, login_required, logout_user, LoginManager
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from models import Ricetta, User, LoginForm, RegisterForm
from import_bridge import db, bcrypt, login_manager


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
# questo e' per criptare la password user

# Inizializzazione estensioni
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

# Creazione del database all'avvio
with app.app_context():
    db.create_all()


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

@app.route("/dettaglio_ricette/<categoria>/<nome_ricetta>")
def dettaglio_ricetta(categoria, nome_ricetta):
    image = request.args.get("image")  # Recupera il parametro dell'immagine
    ricetta = Ricetta.query.filter_by(nome_ricetta=nome_ricetta).first()
    # passa i parametri specificati a dettaglio_ricetta.html
    return render_template("dettaglio_ricetta.html", categoria=categoria, ricetta=ricetta, image=image)

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/run_script")
def run_script():
    # Esegui lo script Python quando il pulsante viene premuto
    # Esegui il tuo script Python qui
    # print("Il pulsante è stato premuto!")
    return 'Script eseguito!'

@app.route("/elenco_ricette", methods=["GET"])
def elenco_ricette():
    elenco_ricette = Ricetta.query.all()
    elenco = []
    for ricetta in elenco_ricette:
        elenco.append({
            "nome_ricetta": ricetta.nome_ricetta,
        })
    return jsonify(elenco)

@app.route("/trova_ricetta", methods=["GET"])
def trova_ricetta():
    nome_ricetta = request.args.get("nome_ricetta") # Ottieni il valore del parametro nome_ricetta da JS
    ricetta = Ricetta.query.filter_by(nome_ricetta=nome_ricetta).first()
    if ricetta is None:
        return jsonify({"detail": "Ricetta non trovata"}),404
    return jsonify({
            "nome_ricetta": ricetta.nome_ricetta,
            "ingredienti": ricetta.ingredienti,
            "kcal": ricetta.kcal
            })

@app.route("/elimina_ricetta", methods=["GET"])
def elimina_ricetta():
    nome_ricetta = request.args.get("nome_ricetta")
    ricetta = Ricetta.query.filter_by(nome_ricetta=nome_ricetta).first()
    if ricetta is None:
        return jsonify({"detail": "La ricetta inserita non esiste"}), 404

    db.session.delete(ricetta)
    db.session.commit()
    return jsonify({"messaggio":"ricetta cancellata"}), 200

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() # questo serve per controllare se user gia presente in db o no
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):# questo controlla che la password appartiene a user
                login_user(user) # e quindi ti logga dentro
                redirect(url_for("dashboard"))# e ti rimanda alla pagina dashboard in templates(struttura a pagamento per me)
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(username=form.username.data, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000) questo fa il sito raggiungibile da tutti i connessi in LAN

    # Ora, se il tuo computer è connesso alla rete,
    # altre persone sulla stessa rete locale possono accedere al tuo sito
    # usando l'indirizzo IP del tuo computer, ad esempio: http://<tuo-ip-locale>:5000.




