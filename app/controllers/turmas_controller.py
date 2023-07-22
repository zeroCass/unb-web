from ..webapp import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Turma, Aula, Exame, NotasExames
from datetime import datetime
from .aulas_controller import register_blueprint as register_aulas_blueprint
from .exames_controller import register_blueprint as register_exames_blueprint
from typing import Union

bp = Blueprint("turmas", __name__)
# registra blueprint de aulas passando turmas como pai
register_aulas_blueprint(bp)
register_exames_blueprint(bp)

@bp.route("/", methods=["GET"])
@login_required
def index() -> render_template:
    """Renderiza a lista de todas as turmas presentes no banco de dados"""

    turmas = Turma.query.all()
    # print(f"Turmas: {turmas}")
    return render_template("turmas/index.jinja2", turmas=turmas, user=current_user)


@bp.route("/new", methods=["GET"])
@login_required
def new() -> render_template:
    """Renderiza a pagina de criação de turma"""
    return render_template("turmas/new.jinja2")



@bp.route("/", methods=["POST"])
@login_required
def create() -> redirect:
    """Cria uma nova instanacia de turma no banco de dados

    Returns:
        Redireciona para a página de lista turmas
    """

    nome = request.form.get("nome")
    horario_inicio = request.form.get("horario_inicio")
    horario_fim = request.form.get("horario_fim")
    senha = request.form.get("senha")
    semestre = request.form.get("semestre")
    professor_id = current_user.id

    horario_inicio = datetime.strptime(horario_inicio, "%H:%M").time()
    horario_fim = datetime.strptime(horario_fim, "%H:%M").time()

    # print(
    #     f"Form fields: {nome}, {horario_inicio}, {horario_fim}, {senha}, {semestre}, {professor_id}")

    new_turma = Turma(nome=nome, horario_inicio=horario_inicio, horario_fim=horario_fim, senha=senha,
                      semestre=semestre, professor_id=professor_id)
    try:
        db.session.add(new_turma)
        db.session.commit()
        flash("Turma criada", category="success")
    except Exception:
        db.session.rollback()
        flash("Erro ao criar turma", category="error")

    return redirect(url_for("turmas.index"))


@bp.route("/<int:turma_id>/show", methods=["GET"])
@login_required
def show(turma_id: int) -> Union[redirect,render_template]:
    """Renderiza a pagina com informações da turma, dentre elas,
    todos os exames e aulas associados

    Args:
        tumra_id: id da turma
    Returns:
        Redireciona para a página com informações da turma dado seu id
    """

    turma = db.get_or_404(Turma, turma_id)
    if turma not in current_user.turmas:
        return redirect(url_for("turmas.matricular", turma_id=turma_id))

    aulas = Aula.query.filter_by(turma_id=turma_id).all()
    exames = Exame.query.filter_by(turma_id=turma_id).all()
    
    # verifica se o estudante respondeu o exame
    if current_user.tipo_usuario == "estudante":
        for exame in exames:
            nota_exame = NotasExames.query.filter_by(exame_id=exame.id, estudante_id=current_user.id).first()
            if nota_exame:
                exame.respondido = True
                exame.nota_estudante = nota_exame.nota_exame_estudante
    
    return render_template("turmas/show.jinja2", turma=turma, aulas=aulas, exames=exames, user=current_user)


@bp.route("/<int:turma_id>/matricular", methods=["GET", "POST"])
@login_required
def matricular(turma_id: int) -> Union[redirect,render_template]:
    """Matricula um estudante em uma turma
    Caso seja um GET, renderiza a página de validação da turma
    Caso seja um POST, realiza a matricula do estudante na turma

    Returns:
        Redireciona para a pagina de validação caso seja um POST
        Redireciona para a página de informação de turma caso seja um GET
    """
    

    if current_user.tipo_usuario != "estudante":
        flash("Voce não pode realizar esta operação", category="error")
        return redirect(url_for("turmas.index"))

    turma = db.get_or_404(Turma, turma_id)
    if request.method == "GET":
        print("matricular GET")
        return render_template("turmas/validate.jinja2", turma=turma)

    if request.method == "POST":
        senha = request.form.get("senha")
        if senha == turma.senha:
            try:
                current_user.turmas.append(turma)
                db.session.commit()
                flash(f"Matriculou-se na Turma {turma.nome}", category="info")
                return redirect(url_for("turmas.show", turma_id=turma_id))
            except Exception as e:
                print(f"Algo deu erro: {e}")
                flash("Algo deu errado")
        else:
            flash("Senha invalida!", category="error")
            print("senha invalida")
            return render_template("turmas/validate.jinja2", turma=turma)

        return redirect(url_for("turmas.index"))
