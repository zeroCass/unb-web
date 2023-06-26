from . import db

class Turma(db.Model):
    __tablename__ = "turma"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    semestre = db.Column(db.Integer, nullable=False)
    
    # professor_id armazenará o ID do professor relacionado à turma.
    professor_id = db.Column(db.Integer, db.ForeignKey(
        'professor.id'), nullable=False)
    
    aulas = db.relationship('Aula', backref=db.backref('turma_aulas', lazy=True)) #1 to N

    # token_presenca

    def __repr__(self) -> str:
        return "<Turma %r>" % self.id
