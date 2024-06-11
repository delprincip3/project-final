# Projectfinal2024

## Descrizione

Projectfinal2024 è un'applicazione web per la gestione delle piantagioni e dei trattamenti. L'app consente agli utenti di registrarsi, effettuare il login, e gestire le proprie piantagioni e trattamenti. Gli amministratori possono inoltre gestire utenti, piantagioni e trattamenti.

## Funzionalità

- *Registrazione e Login:* Gli utenti possono registrarsi e accedere al proprio account.
- *Dashboard Utente:* Gli utenti possono visualizzare e gestire le proprie piantagioni e trattamenti.
- *Dashboard Amministratore:* Gli amministratori possono gestire utenti, piantagioni e trattamenti.
- *Previsioni Meteo:* Integrazione con l'API di Open-Meteo per visualizzare le condizioni meteo correnti.

## Tecnologie Utilizzate

- Python
- Flask
- SQLAlchemy
- MySQL
- HTML/CSS

## Installazione

1. Clonare il repository:
    bash
    git clone https://github.com/username/Projectfinal2024.git
    cd Projectfinal2024
    

2. Creare un ambiente virtuale e attivarlo:
    bash
    python -m venv venv
    source venv/bin/activate  # Su Windows: venv\Scripts\activate
    

3. Installare le dipendenze:
    bash
    pip install -r requirements.txt
    

4. Configurare il database:
    - Assicurarsi di avere MySQL installato e avviato.
    - Creare un database chiamato Projectfinal2024.
    - Aggiornare la stringa di connessione al database nel file app.py se necessario.

5. Eseguire le migrazioni del database:
    bash
    flask db init
    flask db migrate
    flask db upgrade
    

## Esecuzione dell'Applicazione

1. Assicurarsi che l'ambiente virtuale sia attivo.

2. Eseguire l'applicazione Flask:
    bash
    flask run
    

3. Aprire un browser e navigare a http://127.0.0.1:5000.

## Struttura del Progetto

- app.py: Il file principale dell'applicazione Flask.
- models.py: Definisce i modelli di database utilizzando SQLAlchemy.
- forms.py: Definisce i moduli di registrazione, login e gestione delle piante e trattamenti.
- templates/: Contiene i file HTML per le diverse pagine dell'applicazione.
- static/: Contiene file statici come CSS e JavaScript.

## API

L'applicazione fornisce anche alcune API per accedere ai dati delle piantagioni e dei trattamenti degli utenti.

- *GET /api/piantagioni_utente:* Restituisce le piantagioni dell'utente loggato.
- *GET /api/trattamenti_utente:* Restituisce i trattamenti dell'utente loggato.
- *POST /api/associa_pianta_piantagione:* Associa una pianta ad una piantagione.

## Contributi

Sono benvenuti contributi di qualsiasi tipo. Si prega di aprire una issue o fare una pull request.

## Licenza

Questo progetto è rilasciato sotto la licenza MIT. Vedi il file [LICENSE](LICENSE) per maggiori dettagli.
