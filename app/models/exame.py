from . import db

class Exame(db.Model):
    __tablename__ = "exame"
    
    id = db.Column(db.Integer, primary_key=True)
    data_inicio = db.Column(db.DateTime, nullable=True)
    data_fim = db.Column(db.DateTime, nullable=True)
    nome = db.Column(db.String(255))
    nota_exame = db.Column(db.Float)

    # professor_id armazenará o ID do professor relacionado ao exame.
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    # turma_id armazenará o ID da turma relacionada ao exame.
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    
    notas = db.relationship('NotasExames', backref='exame_notas') #1 to N
    respostas = db.relationship('RespostaQuestaoExame', backref='exame_respostas') #1 to N
    # novo relacionamento com tabela associativa - Mateus creation
    questoes = db.relationship("QuestaoExame", back_populates="exame") # N to N
    
    def __repr__(self) -> str:
        return f"<Exame {self.id}> Nome:{self.nome} - Data de Início:{self.data_inicio} \
            - Data de Fim:{self.data_fim} - Nota do Exame:{self.nota_exame}"