from . import db

class RespostaQuestaoExame(db.Model):
    __tablename__ = "resposta_questao_exame"

    resposta_estudante = db.Column(db.String(255))
    nota_estudante_questao = db.Column(db.Float)

    # estudante_id armazenará o ID do estudante.
    estudante_id = db.Column(db.Integer, db.ForeignKey('estudante.id'), primary_key=True, nullable=False)
    # exame_id armazenará o ID do exame.
    exame_id = db.Column(db.Integer, db.ForeignKey('exame.id'), primary_key=True, nullable=False)
    # questao_id armazenará o ID da questao.
    questao_id = db.Column(db.Integer, db.ForeignKey('questao.id'), primary_key=True)

    def __repr__(self) -> str:
        return f"<RespostaQuestaoExame> Resposta Estudante:{self.resposta_estudante} \
            - Nota Estudante Questao:{self.nota_estudante_questao} - Exame ID:{self.exame_id} \
            - Estudante ID: {self.estudante_id} - Questao ID: {self.questao_id}"