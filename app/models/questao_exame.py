from . import db
class QuestaoExame(db.Model):
    __tablename__ = "questao_exame"
    exame_id = db.Column(db.Integer, db.ForeignKey("exame.id"), primary_key=True)
    questao_id = db.Column(db.Integer, db.ForeignKey("questao.id"), primary_key=True)
    nota_questao = db.Column(db.Float, nullable=False)
    # Campo booleano para indicar se a questão foi anulada
    anulada = db.Column(db.Boolean, default=False)

    # refencia ao atributo exame na tabela Questao
    questao = db.relationship("Questao", back_populates="exames")
    # refencia ao atributo questoes na tabela Exame
    exame = db.relationship("Exame", back_populates="questoes")

    def __repr__(self) -> str:
        return f"<QuestaoExame Exame ID: {self.exame_id}> - Questao ID:{self.questao_id} \
            - Nota Questao:{self.nota_questao} - Anulada:{self.anulada}"