from ..webapp import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Questao, Professor, QuestaoMultiplaEscolha

bp = Blueprint("questoes", __name__)

@bp.route("/professor/<int:user_id>", methods=["GET"])
@login_required
def index(user_id):
    # Verificar se o usuário logado é um professor
    if not isinstance(current_user, Professor):
        flash("Acesso não autorizado")
        return render_template("index.jinja2", user=current_user)
    
    # Obtendo as questões relacionadas ao usuário
    questoes = Questao.query.filter_by(professor_id=user_id).all()
    questoes_multipla_escolha = QuestaoMultiplaEscolha.query.filter_by(professor_id=user_id).all()

    return render_template('questoes/index.jinja2', questoes=questoes, questoes_multipla_escolha=questoes_multipla_escolha)

@bp.route("/professor/<int:user_id>/new", methods=["GET"])
@login_required
def new(user_id):
    return render_template("questoes/new.jinja2", user_id=user_id)

@bp.route("/professor/<int:user_id>/create", methods=["POST"])
@login_required
def create(user_id):
    return render_template("questoes/new.jinja2", user_id=user_id)