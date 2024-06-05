from flask import Flask, render_template, request, flash, redirect, url_for, session,jsonify
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegisterForm, PianteForm, TrattamentiForm, EliminaPiantaForm, EliminaUtenteForm, ModificaUtenteForm, AssociaPiantaTrattamentoForm
from datetime import timedelta
from flask_migrate import Migrate

app = Flask(__name__, template_folder='src', static_folder='src')
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Luigi2005@localhost:3306/Projectfinal2024"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecret'
app.secret_key = "27eduCBA09"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# definizioni modelli
user_plant_treatment = db.Table('user_plant_treatment',
    db.Column('user_id', db.Integer, db.ForeignKey('utenza.id'), primary_key=True),
    db.Column('plant_id', db.Integer, db.ForeignKey('piante.id'), primary_key=True),
    db.Column('treatment_id', db.Integer, db.ForeignKey('trattamenti.id'), primary_key=True)
)


class Utenza(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    cognome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    treatments = db.relationship('Trattamenti', backref='utente')

    def __init__(self, tipo, nome, cognome, email, password):
        self.tipo = tipo
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.password = password


class Piante(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    specie = db.Column(db.String(100), nullable=False)
    treatments = db.relationship('Trattamenti', backref='pianta')

    def __init__(self, nome, specie):
        self.nome = nome
        self.specie = specie

class Trattamenti(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pianta_id = db.Column(db.Integer, db.ForeignKey('piante.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('utenza.id'), nullable=True)
    descrizione = db.Column(db.Text, nullable=False)
    data_inizio = db.Column(db.Date, nullable=False)
    data_fine = db.Column(db.Date, nullable=True)

    def __init__(self, pianta_id, user_id, descrizione, data_inizio, data_fine=None):
        self.pianta_id = pianta_id
        self.user_id = user_id
        self.descrizione = descrizione
        self.data_inizio = data_inizio
        self.data_fine = data_fine

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servizi')
def servizi():
    return render_template('servizi.html')

@app.route('/contact')
def contatti():
    return render_template('contatti.html')

@app.route('/dashboardadmin')
def dashboard_admin():
    users = Utenza.query.all()
    piante = Piante.query.all()
    trattamenti = Trattamenti.query.all() 
    return render_template('dashboardadmin.html', users=users, piante=piante, trattamenti=trattamenti)

@app.route('/dashboarduser')
def dashboard_user():
    if 'user_id' not in session:
        flash('Effettua il login per accedere a questa pagina.')
        return redirect(url_for('login'))
    
    utente = Utenza.query.get(session['user_id'])

    if utente is not None:
        trattamenti = utente.treatments
        piante = [trattamento.pianta for trattamento in trattamenti]
        tutte_le_piante = Piante.query.all()  # Aggiungi tutte le piante per il dropdown
        tutti_i_trattamenti = Trattamenti.query.all()  # Aggiungi tutti i trattamenti per il dropdown
        notifiche = ["Notifica 1", "Notifica 2", "Notifica 3"]  # Esempio di notifiche
        return render_template('dashboarduser.html', utente=utente, trattamenti=trattamenti, tutte_le_piante=tutte_le_piante, tutti_i_trattamenti=tutti_i_trattamenti,piante =piante, notifiche=notifiche)
    else:
        flash('Utente non trovato!')
        return redirect(url_for('index'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        utente = Utenza.query.filter_by(email=request.form['email']).first()
        if utente and utente.password == request.form['password']:
            session['user_id'] = utente.id
            session['user_type'] = utente.tipo
            flash('Accesso effettuato con successo!', 'success')
            if utente.tipo == 'Admin':
                return redirect(url_for('dashboard_admin'))
            else:
                return redirect(url_for('dashboard_user'))
        else:
            flash('Credenziali non valide, riprova!', 'error')
    return render_template('login.html', form=form)

@app.route('/registrati', methods=['GET', 'POST'])
def registrati():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = Utenza(
            tipo=form.tipo.data,
            nome=form.nome.data,
            cognome=form.cognome.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account creato con successo!', 'success')
        return redirect(url_for('login'))
    return render_template('registrati.html', form=form)
@app.route('/registrazione', methods=['GET', 'POST'])
def registrazione():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = Utenza(
            tipo=form.tipo.data,
            nome=form.nome.data,
            cognome=form.cognome.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account creato con successo!', 'success')
        return redirect(url_for('login'))
    return render_template('registrazioniadmin.html', form=form)



@app.route('/modifica_pianta/<int:pianta_id>', methods=['GET', 'POST'])
def modifica_pianta(pianta_id):
    pianta = Piante.query.get_or_404(pianta_id)
    form = PianteForm(obj=pianta)
    if form.validate_on_submit():
        pianta.nome = form.nome.data
        pianta.specie = form.specie.data
        db.session.commit()
        flash('Pianta modificata con successo!', 'success')
        return redirect(url_for('dashboard_admin'))
    return render_template('modificapiante.html', form=form)

@app.route('/elimina_pianta/<int:pianta_id>', methods=['GET', 'POST'])
def elimina_pianta(pianta_id):
    pianta = Piante.query.get_or_404(pianta_id)
    form = EliminaPiantaForm()
    if form.validate_on_submit():
        db.session.delete(pianta)
        db.session.commit()
        flash('Pianta eliminata con successo!', 'success')
        return redirect(url_for('dashboard_admin'))
    return render_template('eliminapiante.html', form=form)

@app.route('/add_pianta', methods=['GET', 'POST'])
def add_pianta():
    form = PianteForm()
    if form.validate_on_submit():
        new_pianta = Piante(
            nome=form.nome.data,
            specie=form.specie.data
        )
        db.session.add(new_pianta)
        db.session.commit()
        flash('Nuova pianta aggiunta con successo!', 'success')
        return redirect(url_for('dashboard_admin'))
    return render_template('addpianta.html', form=form)

@app.route('/add_attivita', methods=['GET', 'POST'])
def add_attivita():
    form = TrattamentiForm()
    form.pianta_id.choices = [(pianta.id, pianta.nome) for pianta in Piante.query.all()]
    
    if form.validate_on_submit():
        user_id = session.get('user_id')  # Ottieni l'ID utente dalla sessione, se disponibile
        if not user_id:
            flash('User ID non trovato. Effettua il login per procedere.', 'error')
            return redirect(url_for('login'))
        
        new_trattamento = Trattamenti(
            pianta_id=form.pianta_id.data,
            user_id=user_id,  # Usa l'ID utente dalla sessione
            descrizione=form.descrizione.data,
            data_inizio=form.data_inizio.data,
            data_fine=form.data_fine.data
        )
        db.session.add(new_trattamento)
        db.session.commit()
        flash('Nuova attività aggiunta con successo!', 'success')
        return redirect(url_for('dashboard_admin'))
    return render_template('addattivita.html', form=form)


@app.route('/modifica_utente/<int:user_id>', methods=['GET', 'POST'])
def modifica_utente(user_id):
    utente = Utenza.query.get_or_404(user_id)
    form = ModificaUtenteForm(obj=utente)
    if form.validate_on_submit():
        utente.tipo = form.tipo.data
        utente.nome = form.nome.data
        utente.cognome = form.cognome.data
        utente.email = form.email.data
        db.session.commit()
        flash('Utente modificato con successo!', 'success')
        return redirect(url_for('dashboard_admin'))
    return render_template('modificautente.html', form=form)

@app.route('/elimina_utente/<int:user_id>', methods=['GET', 'POST'])
def elimina_utente(user_id):
    utente = Utenza.query.get_or_404(user_id)
    form = EliminaUtenteForm()
    if form.validate_on_submit():
        db.session.delete(utente)
        db.session.commit()
        flash('Utente eliminato con successo!', 'success')
        return redirect(url_for('dashboard_admin'))
    return render_template('eliminautente.html', form=form)

@app.route('/modifica_trattamento/<int:trattamento_id>', methods=['GET', 'POST'])
def modifica_trattamento(trattamento_id):
    trattamento = Trattamenti.query.get_or_404(trattamento_id)
    form = TrattamentiForm(obj=trattamento)
    form.pianta_id.choices = [(pianta.id, pianta.nome) for pianta in Piante.query.all()]

    if form.validate_on_submit():
        trattamento.pianta_id = form.pianta_id.data
        trattamento.descrizione = form.descrizione.data
        trattamento.data_inizio = form.data_inizio.data
        trattamento.data_fine = form.data_fine.data
        db.session.commit()
        flash('Trattamento modificato con successo!', 'success')
        return redirect(url_for('dashboard_admin'))
    return render_template('modificatrattamento.html', form=form)

@app.route('/elimina_trattamento/<int:trattamento_id>', methods=['GET', 'POST'])
def elimina_trattamento(trattamento_id):
    trattamento = Trattamenti.query.get_or_404(trattamento_id)
    form = EliminaPiantaForm()
    if form.validate_on_submit():
        db.session.delete(trattamento)
        db.session.commit()
        flash('Trattamento eliminato con successo!', 'success')
        return redirect(url_for('dashboard_admin'))
    return render_template('eliminatrattamento.html', form=form)


@app.route('/associa_pianta_trattamento', methods=['GET', 'POST'])
def associa_pianta_trattamento():
    form = AssociaPiantaTrattamentoForm()

    # Ottenere gli utenti, le piante e i trattamenti dal database
    utenti = Utenza.query.all()
    piante = Piante.query.all()
    trattamenti = Trattamenti.query.all()

    if request.method == 'GET':
        # Popolare le scelte nei campi del form
        form.utente_id.choices = [(utente.id, f"{utente.nome} {utente.cognome}") for utente in utenti]
        form.pianta_id.choices = [(pianta.id, pianta.nome) for pianta in piante]
        form.trattamento_id.choices = [(trattamento.id, trattamento.descrizione) for trattamento in trattamenti]
        return render_template('associa_pianta_trattamento.html', form=form, utenti=utenti, piante=piante, trattamenti=trattamenti)

    if form.validate_on_submit():
        # Gestione della sottomissione del form
        nuovo_trattamento = Trattamenti(
            pianta_id=form.pianta_id.data,
            user_id=form.utente_id.data,
            descrizione=form.trattamento_id.data,
            data_inizio=form.data_inizio.data,
            data_fine=form.data_fine.data
        )
        db.session.add(nuovo_trattamento)
        db.session.commit()
        flash('Associazione eseguita con successo!', 'success')
        return redirect(url_for('dashboard_admin'))

    # Ritorno del template anche in caso di errore di validazione del form
    return render_template('associa_pianta_trattamento.html', form=form, utenti=utenti, piante=piante, trattamenti=trattamenti)




if __name__ == "__main__":
    app.run(debug=True)
