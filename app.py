from flask import Flask, render_template, request, flash, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegisterForm, PianteForm, TrattamentiForm, EliminaPiantaForm
from werkzeug.security import generate_password_hash
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
    pianta_id = db.Column(db.Integer, db.ForeignKey('piante.id'), nullable=True)
    descrizione = db.Column(db.Text, nullable=False)
    data_inizio = db.Column(db.Date, nullable=False)
    data_fine = db.Column(db.Date, nullable=True)

    def __init__(self, pianta_id, descrizione, data_inizio, data_fine=None):
        self.pianta_id = pianta_id
        self.descrizione = descrizione
        self.data_inizio = data_inizio
        self.data_fine = data_fine

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboardadmin')
def dashboard_admin():
    return render_template('dashboardadmin.html')

@app.route('/dashboarduser')
def dashboard_user():
    return render_template('dashboarduser.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        utente = Utenza.query.filter_by(email=request.form['email']).first()
        if utente and utente.password == request.form['password']:
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
            password=form.password.data  # hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account creato con successo!', 'success')
        return redirect(url_for('login'))
    return render_template('registrati.html', form=form)

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
    if form.validate_on_submit():
        new_trattamento = Trattamenti(
            pianta_id=form.pianta_id.data,
            descrizione=form.descrizione.data,
            data_inizio=form.data_inizio.data,
            data_fine=form.data_fine.data
        )
        db.session.add(new_trattamento)
        db.session.commit()
        flash('Nuova attività aggiunta con successo!', 'success')
        return redirect(url_for('dashboard_user'))
    return render_template('addattivita.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
