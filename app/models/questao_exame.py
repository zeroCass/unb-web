from . import db


class QuestaoExame(db.Model):
    __tablename__ = "questao_exame"
    exame_id = db.Column(db.Integer, db.ForeignKey("exame.id"), primary_key=True)
    questao_id = db.Column(db.Integer, db.ForeignKey("questao.id"), primary_key=True)
    nota_questao = db.Column(db.Float, nullable=False)

    questao = db.relationship("Questao", back_populates="exames") # refencia ao atributo exame na tabela Questao
    exame = db.relationship("Exame", back_populates="questoes") # refencia ao atributo questoes na tabela Exame

    def __repr__(self) -> str:
        return f"<QuestaoExame ExameID: {self.exame_id}> QuestaoID:{self.questao_id} \
            Nota_Questao:{self.nota_questao}"
