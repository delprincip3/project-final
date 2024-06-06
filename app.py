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




class Utenza(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    cognome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
  

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
   

    def __init__(self, nome, specie):
        self.nome = nome
        self.specie = specie

class Trattamenti(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pianta_id = db.Column(db.Integer, db.ForeignKey(Piante.id), nullable=True)
    user_id = db.Column(db.Integer, nullable=True)
    descrizione = db.Column(db.Text, nullable=False)
    data_inizio = db.Column(db.Date, nullable=False)
    data_fine = db.Column(db.Date, nullable=True)


    def __init__(self,user_id, pianta_id, descrizione, data_inizio, data_fine=None):
        
        self.user_id = user_id
        self.pianta_id = pianta_id
        self.descrizione = descrizione
        self.data_inizio = data_inizio
        self.data_fine = data_fine
    
class Piantagione(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    descrizione = db.Column(db.Text, nullable=False)
    data_inizio = db.Column(db.Date, nullable=False)
    data_fine = db.Column(db.Date, nullable=True)
    
    user_id = db.Column(db.Integer,db.ForeignKey(Utenza.id))
    utente = db.relationship(Utenza)
    pianta_id = db.Column(db.Integer, db.ForeignKey(Piante.id))
    pianta = db.relationship(Piante)

    def __init__(self,nome,descrizione,data_inizio,data_fine,user_id,pianta_id):
        self.nome = nome
        self.descrizione = descrizione
        self.data_inizio = data_inizio
        self.data_fine = data_fine
        self.user_id = user_id
        self.pianta_id = pianta_id

    

    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servizi')
def servizi():
    return render_template('servizi.html')

@app.route('/contact')
def contatti():
    return render_template('contatti.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        utente = Utenza.query.filter_by(email=email).first()

        if utente and utente.password == password:
            session['user_id'] = utente.id
            session.permanent = True  # per mantenere la sessione permanente per la durata specificata
            flash('Login eseguito con successo!', 'success')

            if utente.tipo == 'admin':
                return redirect(url_for('dashboard_admin'))
            else:
                return redirect(url_for('dashboard_user'))
        else:
            flash('Email o password non validi. Riprova.', 'danger')

    return render_template('login.html', form=form)


@app.route('/dashboardadmin')
def dashboard_admin():
    users = Utenza.query.all()
    piante = Piante.query.all()
    trattamenti = Trattamenti.query.all() 
    return render_template('dashboardadmin.html', users=users, piante=piante, trattamenti=trattamenti)

@app.route('/dashboarduser', methods=['GET', 'POST'])
def dashboard_user():
    if 'user_id' not in session:
        flash('Effettua il login per accedere a questa pagina.')
        return redirect(url_for('login'))
    
    utente = Utenza.query.get(session['user_id'])

    if utente is not None:
        # Recupera le piantagioni dell'utente
        piantagioni = Piantagione.query.filter_by(user_id=utente.id).all()
        
        # Estrai i trattamenti e le piante
        trattamenti = [trattamento for piantagione in piantagioni for trattamento in Trattamenti.query.filter_by(pianta_id=piantagione.pianta_id).all()]
        piante = [piantagione.pianta for piantagione in piantagioni]

        # Recupera tutte le piante e i trattamenti per i menu a discesa
        tutte_le_piante = Piante.query.all()
        tutti_i_trattamenti = Trattamenti.query.all()
        
        # Esempio di notifiche
        notifiche = ["Notifica 1", "Notifica 2", "Notifica 3"]

        if request.method == 'POST':
            # Gestione della sottomissione del form di associazione
            pianta_id = request.form.get('pianta_id')
            trattamento_id = request.form.get('trattamento_id')
            data_inizio = request.form.get('data_inizio')
            data_fine = request.form.get('data_fine')
            piantagione_id = request.form.get('piantagione_id')
            user_id = request.form.get('user_id')

            nuovo_trattamento = Trattamenti(
                pianta_id=pianta_id,
                user_id= user_id,
                descrizione=trattamento_id,
                data_inizio=data_inizio,
                data_fine=data_fine,
                piantagione_id =piantagione_id
            )
            db.session.add(nuovo_trattamento)
            db.session.commit()

            flash('Trattamento associato con successo!', 'success')
            return redirect(url_for('dashboard_user'))

        return render_template('dashboarduser.html', 
                               utente=utente, 
                               trattamenti=trattamenti, 
                               tutte_le_piante=tutte_le_piante, 
                               tutti_i_trattamenti=tutti_i_trattamenti, 
                               piante=piante, 
                               notifiche=notifiche, 
                               piantagioni=piantagioni)
    else:
        flash('Utente non trovato!')
        return redirect(url_for('index'))



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

@app.route('/elimina_trattamento/<int:trattamento_id>', methods=['POST'])
def elimina_trattamento(trattamento_id):
    trattamento = Trattamenti.query.get(trattamento_id)
    if trattamento:
        db.session.delete(trattamento)
        db.session.commit()
        flash('Trattamento eliminato con successo!', 'success')
    else:
        flash('Trattamento non trovato.', 'error')
    return redirect(url_for('dashboard_user'))



  # Se stai usando Flask-Login per la gestione dell'accesso

app.route('/associa_pianta_trattamento/<int:user_id>', methods=['GET', 'POST'])
def associa_pianta_trattamento(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash('Accesso non autorizzato.')
        return redirect(url_for('login'))
    
    utente = Utenza.query.get(user_id)

    if request.method == 'POST':
        pianta_id = request.form.get('pianta_id')
        trattamento_id = request.form.get('trattamento_id')
        data_inizio = request.form.get('data_inizio')
        data_fine = request.form.get('data_fine')

        nuovo_trattamento = Trattamenti(
            pianta_id=pianta_id,
            descrizione=trattamento_id,
            data_inizio=data_inizio,
            data_fine=data_fine
        )

        # Assegna l'utente al trattamento utilizzando la relazione definita nel modello Trattamenti
        nuovo_trattamento.utente = utente

        db.session.add(nuovo_trattamento)
        db.session.commit()

        flash('Trattamento associato con successo!', 'success')
        return redirect(url_for('dashboard_user'))

@app.route('/crea_piantagione', methods=['GET', 'POST'])
def crea_piantagione():
    if 'user_id' not in session:
        flash('Effettua il login per accedere a questa pagina.')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        user_id = session['user_id']
        descrizione = request.form.get('descrizione')  # Assumi che la descrizione venga inviata tramite il form
        data_inizio = request.form.get('data_inizio')  # Assumi che la data d'inizio venga inviata tramite il form
        data_fine = request.form.get('data_fine')  # Assumi che la data di fine venga inviata tramite il form
        pianta_id = request.form.get('pianta_id')  # Assumi che l'ID della pianta venga inviato tramite il form
        
        nuova_piantagione = Piantagione(nome=nome, descrizione=descrizione, data_inizio=data_inizio, data_fine=data_fine, user_id=user_id, pianta_id=pianta_id)

        db.session.add(nuova_piantagione)
        db.session.commit()
        
        flash('Piantagione creata con successo!', 'success')
        return redirect(url_for('dashboard_user'))
    
    return render_template('crea_piantagione.html')




if __name__ == "__main__":
    app.run(debug=True)
