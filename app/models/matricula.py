from . import db

# Tabela de associação entre estudante e Turma
association_table = db.Table('matricula',
    db.Column('estudante_id', db.Integer, db.ForeignKey('estudante.id'), primary_key=True),
    db.Column('turma_id', db.Integer, db.ForeignKey('turma.id'), primary_key=True)
)

# Adicionando __repr__ a tabela associativa
def association_table_repr(self) -> str:
    return f"<AssociationTableMatricula Estudante Id:{self.estudante_id} - Turma Id:{self.turma_id}>"

# Atribuindo a função __repr__ 
association_table.__repr__ = association_table_repr