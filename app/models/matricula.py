from . import db

# Tabela de associação entre estudante e Turma
association_table = db.Table('matricula',
    db.Column('estudante_id', db.Integer, db.ForeignKey('estudante.id'), primary_key=True),
    db.Column('turma_id', db.Integer, db.ForeignKey('turma.id'), primary_key=True)
)