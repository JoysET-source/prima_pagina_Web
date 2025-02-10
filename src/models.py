from main import db, app


# Definizione del modello Ricetta
class Ricetta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_ricetta = db.Column(db.String(100), unique=True, nullable=False)
    ingredienti = db.Column(db.String(500), nullable=False)
    kcal = db.Column(db.Integer, nullable=False)
    lavorazioni = db.Column(db.String, nullable=False)
    # image_url = db.Column(db.String(500), nullable=True)  # Aggiungi questo campo per memorizzare l'URL dell'immagine

class User(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    password = db.Column(db.String(80), nullable=True)


# Creare il database
with app.app_context():
    db.create_all()






