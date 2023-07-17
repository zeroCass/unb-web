from ..webapp import db
from seed import estudantes, professores, turmas, aulas, questoes, questoes_multipla_escolha, exames, questoes_exames, respostas_questoes_exames, notas_exames
from ..models import Estudante, Professor, Turma, Aula, Questao, QuestaoMultiplaEscolha, Exame, QuestaoExame, RespostaQuestaoExame, NotasExames


def seed_estudantes():
    for estudante in estudantes:
        estudante_obj = Estudante(**estudante)
        turma = Turma.query.filter_by(id=1).first() # Carregar a turma do banco de dados
        print(turma)
        estudante_obj.turmas.append(turma)
        db.session.add(estudante_obj)
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


def seed_exames():
    for exame in exames:
        db.session.add(Exame(**exame))
    db.session.flush()
    for questao_exame in questoes_exames:
        db.session.add(QuestaoExame(**questao_exame))
    db.session.commit()


def seed_respostas_questoes_exames():
    for resposta_questao_exame in respostas_questoes_exames:
        db.session.add(RespostaQuestaoExame(**resposta_questao_exame))
    db.session.commit()


def seed_notas_exames():
    for nota_exame in notas_exames:
        nota = NotasExames(**nota_exame)
        db.session.add(nota)
    db.session.commit()