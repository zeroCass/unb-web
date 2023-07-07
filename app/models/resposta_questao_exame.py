from . import db

class RespostaQuestaoExame(db.Model):
    __tablename__ = "resposta_questao_exame"

    resposta_aluno = db.Column(db.String(255))
    nota_aluno_questao = db.Column(db.Float)

    # estudante_id armazenará o ID do estudante.
    estudante_id = db.Column(db.Integer, db.ForeignKey('estudante.id'), nullable=False)
    # exame_id armazenará o ID do exame.
    exame_id = db.Column(db.Integer, db.ForeignKey('exame.id'), nullable=False)
    # questao_id armazenará o ID da questao.
    questao_id = db.Column(db.Integer, db.ForeignKey('questao.id'), primary_key=True)

    def __repr__(self) -> str:
        return f"<RespostaQuestaoExame> resposta_aluno:{self.resposta_aluno} \
            nota_aluno_questao:{self.nota_aluno_questao} ExameID:{self.exame_id} estudanteID: {self.estudante_id} QuestaoID: {self.questao_id}"