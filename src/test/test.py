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
# ======================================================================================================================
# ======================================================================================================================
# front end

# document.getElementById("runButton").onclick = function(){
#     const ricettaData = {
#                   nome_ricetta: "Ravioli di zucca", // Puoi cambiare questi valori con quelli che desideri inviare
#                   ingredienti: "pasta fatta in casa, zucca, burro, salvia",
#                   kcal: 400
#                   };
#
#     fetch("/scrivi_ricetta", {
#     method: "POST",
#     headers: { "Content-Type": "application/json" },
#     body: JSON.stringify(ricettaData) // Invia i dati in formato JSON
#     })
#     .then(response= > response.json()) // Assicurati di parsare la risposta come JSON
#     .then(data= > {
#     const newWindow = window.open();
#     if (data.detail)
#     {
#     newWindow.document.write(` < h1
#     style = "text-align: center"; > ${data.detail} < / h1 > `);
#     }
#     else {
#     newWindow.document.write(`
#          < h1 >${data.nome_ricetta} < / h1 >
#          < p > Ingredienti: ${data.ingredienti} < / p >
#          < p > Calorie: ${
#                data.kcal} < / p > `);
#                }
#
#     newWindow.document.close();
#     })
#     .catch(error= > console.error('Error:', error));
#     };
# ===================== col suo backend============
# Definizione della route per la creazione di una ricetta
# @app.route("/scrivi_ricetta", methods=["POST"])
# def scrivi_ricetta():
#     data = request.get_json()  # Ottieni i dati inviati nella richiesta
#     nome_ricetta = data.get('nome_ricetta')
#     ingredienti = data.get('ingredienti')
#     kcal = data.get('kcal')
#
#     # Verifica se la ricetta esiste già nel database
#     existing_ricetta = Ricetta.query.filter_by(nome_ricetta=nome_ricetta).first()
#     if existing_ricetta:
#         return jsonify({"detail" : "Ricetta gia caricata"}), 400
#
#     # Crea una nuova ricetta
#     new_ricetta = Ricetta(
#         nome_ricetta=nome_ricetta,
#         ingredienti=ingredienti,
#         kcal=kcal
#     )
#     try:
#         db.session.add(new_ricetta)
#         db.session.commit()
#         return jsonify({
#             'nome_ricetta': new_ricetta.nome_ricetta,
#             'ingredienti': new_ricetta.ingredienti,
#             'kcal': new_ricetta.kcal
#             })
#     except IntegrityError:
#         db.session.rollback()
#         return jsonify({"detail": "Errore durante il salvataggio della ricetta"}), 500
# ======================================================================================================================
# ======================================================================================================================
# ================ fare stili dinamici per ogni pagina aperta da ogni pulsante =========================================
# backend
# @app.route("/categoria/<categoria>")
# def categoria(categoria):
#     css_file = f"{categoria}.sfondi"  # File CSS per la categoria
#     ricette = load_ricette(categoria)
#     return render_template("categoria.html", categoria=categoria, ricette=ricette, css_file=css_file)
#frontend
# <link rel="stylesheet" href="{{ url_for('static', filename='sfondi/' + css_file) }}">
# ======================================================================================================================