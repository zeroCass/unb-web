from . import db
from sqlalchemy import Enum
from flask_login import UserMixin
class Usuario(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    matricula = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    tipo_usuario = db.Column(
        Enum("estudante", "professor", name="tipo_usuario"), nullable=False)

    def __repr__(self) -> str:
            return f"<Usuario {self.id}> - Nome:{self.nome} - Matricula:{self.matricula} \
                - Email:{self.email} - Tipo Usuario:{self.tipo_usuario}"
