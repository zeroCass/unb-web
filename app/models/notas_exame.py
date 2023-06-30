from . import db

class NotasExames(db.Model):
    __tablename__ = "notas_exames"
    
    exame_id = db.Column(db.Integer, db.ForeignKey('exame.id'), primary_key=True)
    estudante_id = db.Column(db.Integer, db.ForeignKey('estudante.id'), primary_key=True)
    nota_exame = db.Column(db.Float)
    
