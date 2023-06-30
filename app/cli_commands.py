from flask.cli import AppGroup
from .webapp import db
from seed import estudantes, professores, turmas, aulas
from .models import Estudante, Professor, Turma, Aula

seed_cli = AppGroup("seed")


@seed_cli.command("estudantes")
def seed_estudantes():
    for estudante in estudantes:
        db.session.add(Estudante(**estudante))
    db.session.commit()


@seed_cli.command("professores")
def seed_professores():
    for professor in professores:
        db.session.add(Professor(**professor))
    db.session.commit()


@seed_cli.command("turmas")
def seed_turmas():
    for turma in turmas:
        db.session.add(Turma(**turma))
    db.session.commit()

@seed_cli.command("aulas")
def seed_aulas():
    for aula in aulas:
        db.session.add(Aula(**aula))
    db.session.commit()