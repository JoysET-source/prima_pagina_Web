from flask import  request, jsonify
from sqlalchemy.exc import IntegrityError
from models import Ricetta
from main import db, app

@app.route("/run_script")
def run_script():
    # Esegui lo script Python quando il pulsante viene premuto
    # Esegui il tuo script Python qui
    # print("Il pulsante è stato premuto!")
    return 'Script eseguito!'



# Definizione della route per la creazione di una ricetta
@app.route("/scrivi_ricetta", methods=["POST"])
def scrivi_ricetta():
    data = request.get_json()  # Ottieni i dati inviati nella richiesta
    nome_ricetta = data.get('nome_ricetta')
    ingredienti = data.get('ingredienti')
    kcal = data.get('kcal')

    # Verifica se la ricetta esiste già nel database
    existing_ricetta = Ricetta.query.filter_by(nome_ricetta=nome_ricetta).first()
    if existing_ricetta:
        return jsonify({"detail" : "Ricetta gia caricata"}), 400

    # Crea una nuova ricetta
    new_ricetta = Ricetta(
        nome_ricetta=nome_ricetta,
        ingredienti=ingredienti,
        kcal=kcal
    )
    try:
        db.session.add(new_ricetta)
        db.session.commit()
        return jsonify({
            'nome_ricetta': new_ricetta.nome_ricetta,
            'ingredienti': new_ricetta.ingredienti,
            'kcal': new_ricetta.kcal
            })
    except IntegrityError:
        db.session.rollback()
        return jsonify({"detail": "Errore durante il salvataggio della ricetta"}), 500


@app.route("/elenco_ricette", methods=["GET"])
def elenco_ricette():
    elenco_ricette = Ricetta.query.all()
    elenco = []
    for ricetta in elenco_ricette:
        elenco.append({
            "nome_ricetta": ricetta.nome_ricetta,
            "ingredienti": ricetta.ingredienti,
            "kcal": ricetta.kcal
        })
    return jsonify(elenco)

@app.route("/trova_ricetta", methods=["GET"])
def trova_ricetta():
    nome_ricetta = request.args.get("nome_ricetta") # Ottieni il valore del parametro nome_ricetta da JS
    if nome_ricetta is None or nome_ricetta.strip() == "":
        return jsonify({"detail": "Ricetta non caricata"}), 400
    ricetta = Ricetta.query.filter_by(nome_ricetta=nome_ricetta).first()
    if ricetta is None:
        return jsonify({"detail": "Ricetta non trovata"}),404
    return jsonify({
            "nome_ricetta": ricetta.nome_ricetta,
            "ingredienti": ricetta.ingredienti,
            "kcal": ricetta.kcal
            })


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000) questo fa il sito raggiungibile da tutti i connessi in LAN

    # Ora, se il tuo computer è connesso alla rete,
    # altre persone sulla stessa rete locale possono accedere al tuo sito
    # usando l'indirizzo IP del tuo computer, ad esempio: http://<tuo-ip-locale>:5000.




