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
        Enum("aluno", "professor", name="tipo_usuario"), nullable=False)
