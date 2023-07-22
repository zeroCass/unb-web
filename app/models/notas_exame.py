from . import db

class NotasExames(db.Model):
    __tablename__ = "notas_exames"
    
    exame_id = db.Column(db.Integer, db.ForeignKey('exame.id'), primary_key=True)
    estudante_id = db.Column(db.Integer, db.ForeignKey('estudante.id'), primary_key=True)
    nota_exame_estudante = db.Column(db.Float)
    
    def __repr__(self) -> str:
        return f"<NotasExames> Exame Id:{self.exame_id} - Estudante Id:{self.estudante_id} \
            - Nota Exame Estudante:{self.nota_exame_estudante}"