import re

from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from import_bridge import db


# Creazione della tabella Ricetta
class Ricetta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_ricetta = db.Column(db.String(100), unique=True, nullable=False)
    ingredienti = db.Column(db.String(500), nullable=False)
    kcal = db.Column(db.Integer, nullable=False)
    lavorazioni = db.Column(db.String, nullable=False)
    # image_url = db.Column(db.String(500), nullable=True)  # Aggiungi questo campo per memorizzare l'URL dell'immagine

# Creazione della tabella User
class User(db.Model, UserMixin):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String, nullable=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=True)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw= {"placeholder": "Username"})
    password = StringField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    # assicurarsi che username sia unico
    def validazione_username(self, username):
        user_esistente = User.query.filter_by(username=username.data).first()
        if user_esistente:
            raise ValidationError(
                "nome utente non disponibile, sceglierne un altro")

def password_complexity_check(form, field):
    password = field.data
    if not re.search(r"[A-Z]", password):
        raise ValidationError("La password deve contenere almeno un carattere maiuscolo")
    if not re.search(r"[!@#$%^&*(),.?':{}|<>]", password):
        raise ValidationError("La password deve contenere almeno un carattere speciale")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw= {"placeholder": "Username"})
    password = StringField(validators=[InputRequired(), Length(min=8, max=20), password_complexity_check], render_kw= {"placeholder": "Password"})
    submit = SubmitField("Login")








