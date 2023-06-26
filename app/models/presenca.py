from . import db

class Presenca(db.Model):
    __tablename__ = "presenca"

    id = db.Column(db.Integer, primary_key=True)
    aula_id = db.Column(db.Integer, db.ForeignKey(
        'aula.id'), nullable=False)
    data = db.Column(db.DateTime, nullable=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey(
        'usuario.id'), nullable=False)
