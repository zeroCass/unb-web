from . import db
from .questao import Questao
class QuestaoMultiplaEscolha(Questao):
    __tablename__ = "questao_multipla_escolha"

    id = db.Column(db.Integer, db.ForeignKey('questao.id'), primary_key=True)
    
    opcao_a = db.Column(db.String(255))
    opcao_b = db.Column(db.String(255))
    opcao_c = db.Column(db.String(255))
    opcao_d = db.Column(db.String(255))

    def __repr__(self) -> str:
        return (f"<QuestaoMultiplaEscolha {self.id}> - Tipo Questao:{self.tipo_questao} \
            - Enunciado:{self.enunciado} - Opção A:{self.opcao_a} \
            - Opção B:{self.opcao_b} - Opção C:{self.opcao_c} \
            - Opção D:{self.opcao_d} - Resposta:{self.resposta}")