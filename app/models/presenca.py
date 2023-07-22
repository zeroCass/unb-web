from . import db

class Presenca(db.Model):
    __tablename__ = "presenca"

    id = db.Column(db.Integer, primary_key=True)
    aula_id = db.Column(db.Integer, db.ForeignKey(
        'aula.id'), nullable=False)
    data = db.Column(db.DateTime, nullable=True)
    estudante_id = db.Column(db.Integer, db.ForeignKey(
        'usuario.id'), nullable=False)

    def __repr__(self) -> str:
        return f"<Presenca {self.id}> - Aula ID:{self.aula_id} - Data:{self.data} \
            - Estudante ID:{self.estudante_id}"