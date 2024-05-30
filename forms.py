from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField,PasswordField,HiddenField
from wtforms.validators import InputRequired, DataRequired,Email,Length
from wtforms.fields import DateField

class RegisterForm(FlaskForm):
    tipo = SelectField('Tipo', choices=[ ('user', 'User')], validators=[DataRequired()])
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    cognome = StringField('Cognome', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=255)])
    submit = SubmitField('Registrati')

class PianteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    specie = StringField('Specie', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Invia')

class TrattamentiForm(FlaskForm):
    pianta_id = SelectField('Pianta', coerce=int, validators=[DataRequired()])
    descrizione = StringField('Descrizione', validators=[DataRequired()])
    data_inizio = DateField('Data Inizio', format='%Y-%m-%d', validators=[DataRequired()])
    data_fine = DateField('Data Fine', format='%Y-%m-%d')
    submit = SubmitField('Invia')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])

class EliminaPiantaForm(FlaskForm):
    
    conferma = SubmitField('Conferma Eliminazione')

class ModificaUtenteForm(FlaskForm):
    tipo = SelectField('Tipo', choices=[('Admin', 'Admin'), ('User', 'User')], validators=[DataRequired()])
    nome = StringField('Nome', validators=[DataRequired()])
    cognome = StringField('Cognome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Salva Modifiche')

class EliminaUtenteForm(FlaskForm):
    submit = SubmitField('Conferma Eliminazione')