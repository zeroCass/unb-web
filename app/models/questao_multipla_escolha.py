from . import db
from .questao import Questao

class QuestaoMultiplaEscolha(Questao):
    __tablename__ = "questao_multipla_escolha"

    id = db.Column(db.Integer, db.ForeignKey('questao.id'), primary_key=True)
    
    opcao_a = db.Column(db.String(255))
    opcao_b = db.Column(db.String(255))
    opcao_c = db.Column(db.String(255))
    opcao_d = db.Column(db.String(255))