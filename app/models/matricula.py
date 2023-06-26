from . import db

# Tabela de associação entre Aluno e Turma
association_table = db.Table('matricula',
    db.Column('aluno_id', db.Integer, db.ForeignKey('aluno.id'), primary_key=True),
    db.Column('turma_id', db.Integer, db.ForeignKey('turma.id'), primary_key=True)
)