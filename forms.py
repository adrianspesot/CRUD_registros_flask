from flask_wtf import FlaskForm
from wtforms import Form, TextField, TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired

class PersonaForm(FlaskForm):
    nombre = StringField('Nombre', validators = [DataRequired()]) #Valor Requerido
    apellido = StringField('Apellido')#valor opcional
    email = StringField('e-mail', validators = [DataRequired()])
    #Agregamos los botones
    enviar = SubmitField('Enviar')