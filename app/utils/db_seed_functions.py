from ..webapp import db
from seed import estudantes, professores, turmas, aulas, questoes, questoes_multipla_escolha
from ..models import Estudante, Professor, Turma, Aula, Questao, QuestaoMultiplaEscolha



def seed_estudantes():
    for estudante in estudantes:
        db.session.add(Estudante(**estudante))
    db.session.commit()



def seed_professores():
    for professor in professores:
        db.session.add(Professor(**professor))
    db.session.commit()



def seed_turmas():
    for turma in turmas:
        db.session.add(Turma(**turma))
    db.session.commit()


def seed_aulas():
    for aula in aulas:
        db.session.add(Aula(**aula))
    db.session.commit()



def seed_questoes():
    for questao in questoes:
        db.session.add(Questao(**questao))
    db.session.commit()


def seed_questoes_multipla_escolha():
    for questao in questoes_multipla_escolha:
        print(questao)
        db.session.add(QuestaoMultiplaEscolha(**questao))
    db.session.commit()



