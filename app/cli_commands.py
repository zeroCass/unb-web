from flask.cli import AppGroup
from .utils.db_seed_functions import * 

seed_cli = AppGroup("seed")


@seed_cli.command("professores")
def professores():
    seed_estudantes()

@seed_cli.command("estudantes")
def estudantes():
    seed_estudantes()

@seed_cli.command("turmas")
def turmas():
    seed_turmas()

@seed_cli.command("aulas")
def aulas():
    seed_aulas()


@seed_cli.command("questoes")
def questoes():
    seed_questoes()

@seed_cli.command("questoes_multipla_escolha")
def questoes_multipla_escolha():
    seed_questoes_multipla_escolha()

@seed_cli.command("seed-all")
def seed_all():
    seed_professores()
    seed_estudantes()
    seed_turmas()
    seed_aulas()
    seed_questoes()
    seed_questoes_multipla_escolha()

