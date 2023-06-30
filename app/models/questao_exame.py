from . import db

# Tabela de associação entre questao e exame
questao_exame = db.Table('questao_exame',
    db.Column('id_exame', db.Integer, db.ForeignKey('exame.id'), primary_key=True),
    db.Column('id_questao', db.Integer, db.ForeignKey('questao.id'), primary_key=True),
    db.Column('nota_questao', db.Float)
)