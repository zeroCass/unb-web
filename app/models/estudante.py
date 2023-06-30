from . import db
from .usuario import Usuario
from .matricula import association_table


class Estudante(Usuario):
    __tablename__ = "estudante"

    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)

    # Criamos uma tabela de associação chamada association_table
    turmas = db.relationship(
        'Turma', secondary=association_table, backref='estudantes_turma') #N to N

    def __repr__(self) -> str:
        return f"<Estudante {self.id}> Nome:{self.nome} - Matricula:{self.matricula} - Email:{self.email} - Turmas:{self.turmas}"
