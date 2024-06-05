from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo,Optional

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    tipo = SelectField('Tipo', choices=[ ('User', 'User')], validators=[DataRequired()])
    nome = StringField('Nome', validators=[DataRequired()])
    cognome = StringField('Cognome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
   
    submit = SubmitField('Registrati')

class PianteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    specie = StringField('Specie', validators=[DataRequired()])
    submit = SubmitField('Salva')

class TrattamentiForm(FlaskForm):
    pianta_id = SelectField('Pianta', coerce=int, validators=[DataRequired()])
    descrizione = TextAreaField('Descrizione', validators=[DataRequired()])
    data_inizio = DateField('Data Inizio', validators=[DataRequired()])
    data_fine = DateField('Data Fine', validators=[Optional()])
    submit = SubmitField('Salva')

class EliminaPiantaForm(FlaskForm):
    submit = SubmitField('Elimina')

class EliminaUtenteForm(FlaskForm):
    submit = SubmitField('Elimina')

class ModificaUtenteForm(FlaskForm):
    tipo = SelectField('Tipo', choices=[('Admin', 'Admin'), ('User', 'User')], validators=[DataRequired()])
    nome = StringField('Nome', validators=[DataRequired()])
    cognome = StringField('Cognome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Salva')

class AssociaPiantaTrattamentoForm(FlaskForm):
    utente_id = SelectField('Utente', coerce=int, validators=[DataRequired()])
    pianta_id = SelectField('Pianta', coerce=int, validators=[DataRequired()])
    trattamento_id = SelectField('Trattamento', coerce=int, validators=[DataRequired()])
    data_inizio = DateField('Data Inizio', validators=[DataRequired()])
    data_fine = DateField('Data Fine', validators=[Optional()])
    submit = SubmitField('Associa')


