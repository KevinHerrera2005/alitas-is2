from models import db

class UsuarioCliente(db.Model):
    __tablename__ = "Usuarios_cliente"

    ID_Usuario_ClienteF = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(100), nullable=True)
    ID_sucursal = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"<UsuarioCliente {self.Username}>"
    