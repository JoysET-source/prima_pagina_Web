# import os
# from flask import Flask, request, jsonify
# from werkzeug.utils import secure_filename
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ricette.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['UPLOAD_FOLDER'] = 'uploads/'  # Cartella dove salvare le immagini
# app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Estensioni supportate
# db = SQLAlchemy(app)
#
# # Modello Ricetta
# class Ricetta(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nome_ricetta = db.Column(db.String(100), unique=True, nullable=False)
#     ingredienti = db.Column(db.String(500), nullable=False)
#     kcal = db.Column(db.Integer, nullable=False)
#     image_path = db.Column(db.String(200), nullable=False)
#
# # Funzione per controllare le estensioni dei file
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
#
# @app.route("/aggiungi_ricetta", methods=["POST"])
# def aggiungi_ricetta():
#     if 'image' not in request.files:
#         return jsonify({"detail": "No image part"}), 400
#     file = request.files['image']
#     if file.filename == '':
#         return jsonify({"detail": "No selected file"}), 400
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)
#
#         # Ottieni i dati della ricetta dal form
#         nome_ricetta = request.form['nome_ricetta']
#         ingredienti = request.form['ingredienti']
#         kcal = request.form['kcal']
#
#         # Crea una nuova ricetta nel database
#         new_ricetta = Ricetta(
#             nome_ricetta=nome_ricetta,
#             ingredienti=ingredienti,
#             kcal=kcal,
#             image_path=file_path  # Salva il percorso dell'immagine
#         )
#
#         db.session.add(new_ricetta)
#         db.session.commit()
#
#         return jsonify({"detail": "Ricetta aggiunta con successo!"}), 200
#     else:
#         return jsonify({"detail": "File non valido"}), 400
#
# if __name__ == '__main__':
#     app.run(debug=True)
