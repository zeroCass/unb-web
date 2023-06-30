from . import db
from .usuario import Usuario

class Professor(Usuario):
    __tablename__ = "professor"

    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)

    turmas = db.relationship('Turma', backref='prof_turmas', lazy=True) #1 to N
    questoes = db.relationship('Questao', backref='prof_questoes', lazy=True) #1 to N
    exames = db.relationship('Exame', backref='prof_exames', lazy=True) #1 to N

    def __repr__(self) -> str:
        return f"<Professor {self.id}> Nome:{self.nome} - Matricula:{self.matricula} - Email:{self.email} - Turmas:{self.turmas}"
