from ..webapp import db
from flask import Blueprint, render_template, request, redirect, url_for, flash, json
from flask_login import login_required, current_user
from ..models import Turma, Exame, Questao, QuestaoMultiplaEscolha, QuestaoExame, RespostaQuestaoExame, NotasExames
from datetime import datetime
from app.utils.decorators import load_parent_resource_factory
import json
import re

bp = Blueprint("exames", __name__)
parent_model = Turma

def register_blueprint(parent_blueprint: Blueprint):
    parent_blueprint.register_blueprint(
        bp, url_prefix=f"/<int:turma_id>/exames")

# decorator com config especifica para aulas
load_parent = load_parent_resource_factory(parent_model, "turma_id")

@bp.route("/new", methods=["GET"])
@login_required
@load_parent
def new(turma: Turma):
    questoes = Questao.query.filter_by(professor_id=current_user.id).all()
    questoes_json = [{
        "id": questao.id,
        "enunciado": questao.enunciado,
        "resposta": questao.resposta,
        "tipo_questao": questao.tipo_questao
    } for questao in questoes]

    # Acessando o valor do parâmetro 'turma_id' no URL
    return render_template("exames/new.jinja2", turma=turma, questoes=questoes, questoes_json=questoes_json)

@bp.route("/create", methods=["POST"])
@login_required
def create(turma_id):
    # converte o dado das questoes escolhidas em json 
    questoes_selecionadas = json.loads(request.form.get("questoes_selecionadas"))
    nome = request.form.get("nome")
    data_inicio = request.form.get("data_inicio")
    data_fim = request.form.get("data_fim")
    nota_exame = float(request.form.get("nota_exame"))
    professor_id = current_user.id
    data_inicio = datetime.strptime(data_inicio, "%Y-%m-%dT%H:%M")
    data_fim = datetime.strptime(data_fim, "%Y-%m-%dT%H:%M")

    new_exame = Exame(nome=nome, data_inicio=data_inicio, data_fim=data_fim, nota_exame=nota_exame, 
                      professor_id=professor_id, turma_id=turma_id)


    try:
        db.session.add(new_exame)
        db.session.flush()

        # adicionar questoes e seus valores na tabela questao_exame (table associativa)
        for questao in questoes_selecionadas:
            association = QuestaoExame(exame_id=new_exame.id, questao_id=questao["questao_id"],
                            nota_questao=questao["nota_questao"])
            db.session.add(association)

        db.session.commit()
        flash("Exame criado")
    except Exception as e:
        db.session.rollback()
        print(e)
        flash("Erro ao criar Exame")

    return redirect(url_for("turmas.show", turma_id=turma_id))



@bp.route("<int:exame_id>/show", methods=['GET'])
@login_required
def show(turma_id, exame_id):
    exame = Exame.query.filter_by(id=exame_id).first()
    questoes_exame = exame.questoes # tabela associativa

    # Obtendo as opções da questão de múltipla escolha
    for questao_exame in questoes_exame:
        if questao_exame.questao.tipo_questao == "multipla_escolha":
            multipla_escolha = QuestaoMultiplaEscolha.query.filter_by(id=questao_exame.questao.id).all()
            questao_exame.questao.opcoes = multipla_escolha
    return render_template("exames/show.jinja2", turma_id=turma_id, exame=exame, questoes_exame=questoes_exame)



@bp.route("<int:exame_id>/submit", methods=['POST'])
@login_required
def submit(turma_id, exame_id):
    print(request.form)
    nota_exame = 0
    try:
        for questao in request.form:
                questao_id = re.search("\d+$", questao)[0]
                questao_db = Questao.query.filter_by(id=questao_id).first()
                exame_db = Exame.query.filter_by(id=exame_id).first()
                questao_exame = QuestaoExame.query.filter_by(exame_id=exame_id, questao_id=questao_id).first()
                
                resposta_aluno =  request.form[questao]
                nota_aluno_questao = 0

                if questao_db.resposta.lower() == resposta_aluno.lower():
                    nota_exame += questao_exame.nota_questao
                    nota_aluno_questao = questao_exame.nota_questao
                
                # print(f"Questao ID: {questao_db.id} - nota:{questao_exame.nota_questao} \
                #     resposta_aluno: {resposta_aluno} - resposta_questao: {questao_db.resposta} \
                #         acertou: {acertou}")
                
                # print(f"questao[{questao_id}]: {questao} - resposta: {request.form[questao]}")

                resposta_questao_exame = RespostaQuestaoExame(estudante_id=current_user.id, exame_id=exame_id,
                                            questao_id=questao_id, resposta_aluno=resposta_aluno, nota_aluno_questao=nota_aluno_questao)
                db.session.add(resposta_questao_exame)
        notas_exames = NotasExames(exame_id=exame_id, estudante_id=current_user.id, nota_exame=nota_exame)
        db.session.add(notas_exames)
        db.session.commit()
        flash("Exame enviado com sucesso!")
    except Exception as e:
        print(e)
        flash("Erro ao enviar exame")
    return redirect(url_for("turmas.show", turma_id=turma_id))



@bp.route("<int:exame_id>/resposta/<int:estudante_id>", methods=['GET'])
@login_required
def resposta_exame(turma_id, exame_id, estudante_id):
    try:
        exame = Exame.query.filter_by(id=exame_id).first()
        questoes_exame = [] # tabela associativa
        # REFATORAR ISSO AQUI (CODIGO DUPLICADO DE SHOW)
        # Obtendo as opções da questão de múltipla escolha
        

        for questao_exame in  exame.questoes:
            questao = questao_exame.questao
            questao.nota_questao = questao_exame.nota_questao # atribui nota ao objeto

            if questao_exame.questao.tipo_questao == "multipla_escolha":
                multipla_escolha = QuestaoMultiplaEscolha.query.filter_by(id=questao.id).all()
                questao.opcoes = multipla_escolha

            resposta_questao_exame = RespostaQuestaoExame.query.filter_by(estudante_id=estudante_id,exame_id=exame_id, questao_id=questao.id).first()
            
            questao.resposta_aluno = resposta_questao_exame.resposta_aluno
            questao.nota_aluno_questao = resposta_questao_exame.nota_aluno_questao
            questoes_exame.append(questao)
        
        # for questao in questoes_exame:
        #     print(f"id:{questao.id} enunciado {questao.enunciado} \
        #             nota_questao: {questao.nota_questao} nota_aluno: {questao.nota_aluno_questao} \
        #             resposta: {questao.resposta} resposta_aluno: {questao.resposta_aluno}")

        return render_template("exames/resposta_exame.jinja2", turma_id=turma_id, exame=exame, questoes_exame=questoes_exame)
    except Exception as e:
        print(e)
        flash(f"Error: {e}")
        return redirect(url_for("turmas.show", turma_id=turma_id))
    