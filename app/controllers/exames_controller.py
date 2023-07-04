from ..webapp import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Turma, Exame, Questao
from datetime import datetime
from app.utils.decorators import load_parent_resource_factory
import json

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
    print(request.form)
    print(request.form.getlist('questoesSelecionadas'))

    # nome = request.form.get("nome")
    # data_inicio = request.form.get("data_inicio")
    # data_fim = request.form.get("data_fim")
    # nota_exame = request.form.get("nota_exame")
    # professor_id = current_user.id

    # data_inicio = datetime.strptime(data_inicio, "%Y-%m-%dT%H:%M")
    # data_fim = datetime.strptime(data_fim, "%Y-%m-%dT%H:%M")

    # new_exame = Exame(nome=nome, data_inicio=data_inicio, data_fim=data_fim, nota_exame=nota_exame, professor_id=professor_id, turma_id=turma_id)
    
    # try:
    #     db.session.add(new_exame)
    #     db.session.commit()
    #     flash("Exame criado")
    # except Exception:
    #     db.session.rollback()
    #     flash("Erro ao criar Exame")

    return redirect(url_for("turmas.show", turma_id=turma_id))