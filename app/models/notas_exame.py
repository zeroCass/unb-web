from . import db

class NotasExames(db.Model):
    __tablename__ = "notas_exames"
    
    exame_id = db.Column(db.Integer, db.ForeignKey('exame.id'), primary_key=True)
    estudante_id = db.Column(db.Integer, db.ForeignKey('estudante.id'), primary_key=True)
    nota_exame = db.Column(db.Float) # renomear este atributo pois esta confuso -> nota que o estudante obteve no exame
    
    def __repr__(self) -> str:
        return f"<NotasExames> exame_id:{self.exame_id} estudante_id: {self.estudante_id}"