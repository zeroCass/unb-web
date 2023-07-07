from . import db
from sqlalchemy import Enum

class Questao(db.Model):
    __tablename__ = "questao"
    id = db.Column(db.Integer, primary_key=True)
    enunciado = db.Column(db.String(255))
    resposta = db.Column(db.String(255))
    tipo_questao = db.Column(
        Enum("multipla_escolha", "verdadeiro_falso", "numerica", "dissertativa", name="tipo_questao"), nullable=False)
    
    # professor_id armazenará o ID do professor relacionado à questão.
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    respostas = db.relationship('RespostaQuestaoExame', backref='questao_respostas') #1 to N
    exames = db.relationship("QuestaoExame", back_populates="questao") # tabela associativa N to N

    def __repr__(self) -> str:
        return f"<Questao ID: {self.id}> Enunciado:{self.enunciado} \
            Tipo_questao:{self.tipo_questao} Resposta:{self.resposta}"
