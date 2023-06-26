from ..webapp import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from ..models import Turma, Aula
from datetime import datetime
from app.utils.decorators import load_parent_resource_factory
from .presenca_controller import register_blueprint as register_presenca_blueprint

bp = Blueprint("aulas", __name__)
# registra blueprint de presenca passando aulas como pai
register_presenca_blueprint(bp)


parent_model = Turma


def register_blueprint(parent_blueprint: Blueprint):
    parent_blueprint.register_blueprint(
        bp, url_prefix=f"/<int:turma_id>/aulas")


# decorator com config especifica para aulas
load_parent = load_parent_resource_factory(parent_model, "turma_id")


@bp.route("/", methods=["GET"])
@login_required
@load_parent
def new(turma: Turma):
    # Acessando o valor do parâmetro 'turma_id' no URL
    return render_template("aulas/new.jinja2", turma=turma)


@bp.route("/create", methods=["POST"])
@login_required
def create(turma_id):
    print(
        f"DEBUGG - (metodo create /create em aulas_controller.py): turma_id[{turma_id}]")

    data_aula = request.form['data_aula']

    data_aula = datetime.strptime(data_aula, "%Y-%m-%d").date()

    # Verificar se já existe uma aula agendada para a data informada
    existing_aula = Aula.query.filter_by(
        turma_id=turma_id, data_aula=data_aula).first()
    if existing_aula:
        flash("Já existe uma aula para essa data")
        return redirect(url_for("turmas.show", turma_id=turma_id))

    data_atual = datetime.now().date()
    hora_atual = datetime.now().time()

    turma = Turma.query.get(turma_id)

    if data_aula < data_atual:
        status = "finalizado"
    elif data_aula > data_atual:
        status = "agendado"
    else:
        if hora_atual >= turma.horario_inicio and hora_atual < turma.horario_fim:
            status = "em andamento"
        elif hora_atual > turma.horario_inicio and hora_atual >= turma.horario_fim:
            status = "finalizado"
        else:
            status = "agendado"

    aula = Aula(turma_id=turma_id, data_aula=data_aula, status=status)

    db.session.add(aula)
    db.session.commit()

    return redirect(url_for("turmas.show", turma_id=turma_id))

@bp.route("/<int:aula_id>/edit", methods=['GET', 'POST'])
@login_required
def edit(turma_id, aula_id):
    turma = Turma.query.get_or_404(turma_id)
    aula = Aula.query.get_or_404(aula_id)

    data_atual = datetime.now().date()
    hora_atual = datetime.now().time()

    if request.method == "POST":
        novo_status = request.form.get('novo_status')
        aula.status = novo_status
        db.session.commit()
        return redirect(url_for("turmas.show", id=turma_id))

    return render_template("aulas/edit.jinja2", turma=turma, aula=aula, data_atual=data_atual, hora_atual=hora_atual)