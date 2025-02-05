from main import db, app


# Definizione del modello Ricetta
class Ricetta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_ricetta = db.Column(db.String(100), unique=True, nullable=False)
    ingredienti = db.Column(db.String(500), nullable=False)
    kcal = db.Column(db.Integer, nullable=False)
    # image_url = db.Column(db.String(500), nullable=True)  # Aggiungi questo campo per memorizzare l'URL dell'immagine

# Creare il database
with app.app_context():
    db.create_all()






