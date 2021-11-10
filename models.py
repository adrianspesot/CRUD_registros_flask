from database import db

class Persona(db.Model): # En la base de datos crea una tabla que se llama "persona" 
    id = db.Column(db.Integer, primary_key =True)
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))
    email = db.Column(db.String(250))

    def __str__(self) -> str:
        return (
            f'Id: {self.id}, '
            f'Nombre: {self.nombre}, '
            f'Apellido: {self.apellido}, '
            f'email: {self.email}'
        )