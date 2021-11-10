from logging import error

from flask import Flask, request
from flask.helpers import url_for
from flask.templating import render_template
from flask.wrappers import Request
from flask_migrate import Migrate
from werkzeug.utils import redirect

from database import db
from forms import PersonaForm
from models import Persona

app = Flask(__name__) #__name__ es el valor del nombre del archivo app.py

#Configuracion de la bd
USER_DB = 'postgres'
PASS_DB = 'root'
URL_DB = 'localhost'
NAME_DB = 'sap_flask_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

#Configuracion del objeto
app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB #Conecta la DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Evita modificaciones constantemente

#Inicializamos el objeto
db.init_app(app) #con esto se evita un problema circular

#Configurar flask-migrate
#Esto realiza las migraciones 
migrate = Migrate()
migrate.init_app(app, db)

#Configurar flask-wtf
app.config [ 'SECRET_KEY' ] = 'llave_secreta'


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def inicio():
    #Listado de personas
    personas = Persona.query.all()
    total_personas = Persona.query.count()
    #app.logger.debug(f'Listado Personas: {personas}')
    #app.logger.debug(f'Listado Total Personas: {total_personas}')
    app.logger.warning(f'Listado Personas: {personas}')
    app.logger.warning(f'Listado Total Personas: {total_personas}')
    return render_template('index.html', personas = personas, total_personas = total_personas)

@app.route('/ver/<int:id>')
#Se especifica el tipo de dato y el nombre: <int:id> int: integer(por default es str) y id: nombre de variable
def ver_detalle(id):
    #Recuperamos la persona segun el id proporcionado
    persona = Persona.query.get_or_404(id)
    app.logger.warning(f'Ver Persona: {persona}')
    return render_template('detalle.html', persona=persona)

@app.route('/agregar', methods = ['GET', 'POST'])
def agregar_persona():
    persona = Persona()
    personaForm = PersonaForm(obj = persona) #obj especifica la clase de modelo a utilizar
    if request.method == 'POST':
        if personaForm.validate_on_submit:
            personaForm.populate_obj(persona) #se carga el objeto persona con los datos del formulario
            app.logger.warning(f'Persona Agregada: {persona}')
            #Insertamos el nuevo REGISTRO
            db.session.add(persona)
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('agregar.html', forma = personaForm)

@app.route('/editar/<int:id>', methods = ['GET', 'POST'])
def editar_persona(id):
    persona = Persona.query.get_or_404(id)
    personaForm = PersonaForm(obj = persona)
    
    if request.method == 'POST':
        if personaForm.validate_on_submit:
            personaForm.populate_obj(persona)
            app.logger.warning(f'Persona Editada: {persona}')
            db.session.commit()
            return redirect(url_for('inicio'))
           
    return render_template('editar.html', forma = personaForm)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    persona = Persona.query.get_or_404(id)
    db.session.delete(persona)
    db.session.commit()

    return redirect(url_for('inicio'))