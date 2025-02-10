document.getElementById("runButton0").onclick = function() {
            fetch("/run_script")
            .then(response => response.text())
            .then(data => {alert("si giusto")
            });
        };


        document.getElementById("runButton").onclick = function() {
            const ricettaData = {
                nome_ricetta: "per test4",  // Puoi cambiare questi valori con quelli che desideri inviare
                ingredienti: "pasta fatta in casa, zucca, burro, salvia",
                kcal: 230
            };

            fetch("/scrivi_ricetta", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(ricettaData)  // Invia i dati in formato JSON
                })
                .then(response => response.json())  // Assicurati di parsare la risposta come JSON
                .then(data => {
                    const newWindow = window.open();
                    if (data.detail){
                        newWindow.document.write(`<h1 style="text-align: center";>${data.detail}</h1>`);
                    }
                    else{
                        newWindow.document.write(`
                        <h1>${data.nome_ricetta}</h1>
                        <p>Ingredienti: ${data.ingredienti}</p>
                        <p>Calorie: ${data.kcal}</p>`);
                    }

                    newWindow.document.close();
                })
                .catch(error => console.error('Error:', error));
        };

        document.getElementById("runButton1").onclick = function(){
            fetch("/elenco_ricette") // Effettua la richiesta GET all'endpoint
                .then(response => response.json())  // Parsifica la risposta JSON
                .then(data => {
            // Creiamo una nuova finestra per visualizzare i dati delle ricette
                    const newWindow = window.open();
                    data.forEach(ricetta => { // Loop su ogni ricetta
                    newWindow.document.write(`
                    <h1>${ricetta.nome_ricetta}</h1>
                `);
            });
            newWindow.document.close();
            })
                .catch(error => console.error('Errore:', error)); // Gestione degli errori
        };

        document.getElementById("search-button").onclick = function(){ //quando premi il pulsante fai function
            const cercaRicetta = document.getElementById("search-input").value; //prendi il valore dell`input
            if (!cercaRicetta){
                alert("inserisci una ricetta")
            }
            else{
            fetch("/trova_ricetta?nome_ricetta=" + cercaRicetta) // passa il valore come parametro nella richiesta a python
                .then(response => response.json())
                .then(data => {
                    if (data.detail){
                        alert(`${data.detail}`)
                    }else{
                        const newWindow = window.open();
                        newWindow.document.write(`
                        <h1>${data.nome_ricetta}</h1>
                        <p>${data.ingredienti}</p>
                        <p>${data.kcal}</p>
                        `)};
                        newWindow.document.close();
                    })
                .catch(error => console.error("Errore:", error))};
                document.getElementById("search-input").value = ""; //refresh alla barra di ricerca
        };

        document.getElementById("elimina-button").onclick = function(){
            const eliminaRicetta = document.getElementById("search-input").value;
            fetch("/elimina_ricetta?nome_ricetta=" + eliminaRicetta)
                .then(response => response.json())
                .then(data => {
                    if (data.detail){
                        alert(`${data.detail}`)
                    }
                    if (data.messaggio) {
                        alert(`${data.messaggio}`)
                    }
                });
                document.getElementById("search-input").value = "";
        };