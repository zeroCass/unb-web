from ..webapp import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Turma, Aula
from datetime import datetime
from .aulas_controller import register_blueprint as register_aulas_blueprint

bp = Blueprint("turmas", __name__)
# registra blueprint de aulas passando turmas como pai
register_aulas_blueprint(bp)


@bp.route("/", methods=["GET"])
@login_required
def index():
    turmas = Turma.query.all()
    # user_type = session.get("user_type")

    print(f"Turmas: {turmas}")
    return render_template("turmas/index.jinja2", turmas=turmas, user=current_user)


@bp.route("/new", methods=["GET"])
@login_required
def new():
    return render_template("turmas/new.jinja2")


@bp.route("/validate", methods=["GET", "POST"])
@login_required
def validate():
    if request.method == "POST":
        # senha = request.form.get("senha")
        flash("Você foi matriculado em uma turma")
        return redirect(url_for("turmas.index"))

    return render_template("turmas/validate.jinja2")


@bp.route("/", methods=["POST"])
@login_required
def create():
    nome = request.form.get("nome")
    horario_inicio = request.form.get("horario_inicio")
    horario_fim = request.form.get("horario_fim")
    senha = request.form.get("senha")
    semestre = request.form.get("semestre")
    professor_id = current_user.id

    horario_inicio = datetime.strptime(horario_inicio, "%H:%M").time()
    horario_fim = datetime.strptime(horario_fim, "%H:%M").time()

    print(
        f"Form fields: {nome}, {horario_inicio}, {horario_fim}, {senha}, {semestre}, {professor_id}")

    new_turma = Turma(nome=nome, horario_inicio=horario_inicio, horario_fim=horario_fim, senha=senha,
                      semestre=semestre, professor_id=professor_id)
    try:
        db.session.add(new_turma)
        db.session.commit()
        flash("Turma criada")
    except Exception:
        db.session.rollback()
        flash("Erro ao criar turma")

    return redirect(url_for("turmas.index"))


@bp.route("/<int:turma_id>/show", methods=["GET"])
def show(turma_id):
    turma = db.get_or_404(Turma, turma_id)
    aulas = Aula.query.filter_by(turma_id=turma_id).all()
    if turma not in current_user.turmas:
        return redirect(url_for("turmas.matricular", turma_id=turma_id))
    return render_template("turmas/show.jinja2", turma=turma, aulas=aulas, user=current_user)


@bp.route("/<int:turma_id>/matricular", methods=["GET", "POST"])
def matricular(turma_id):
    print("tentou matricular")
    # se nao for aluno, nao pode prosseguir
    if current_user.tipo_usuario != "aluno":
        flash("Voce não pode realizar esta operação", category="error")
        return redirect(url_for("turmas.index"))

    turma = db.get_or_404(Turma, turma_id)
    print(turma)
    if request.method == "GET":
        print("matricular GET")
        return render_template("turmas/validate.jinja2", turma=turma)

    if request.method == "POST":
        print("matricular POST")
        senha = request.form.get("senha")
        print(f"fom senha: {senha} - senha turma: {turma.senha}")
        if senha == turma.senha:
            try:
                current_user.turmas.append(turma)
                db.session.commit()
                flash(f"Matriculou-se na Turma {turma.nome}")
                return redirect(url_for("turmas.show", turma_id=turma_id))
            except Exception as e:
                print(f"Algo deu erro: {e}")
                flash("Algo deu errado")
        else:
            flash("Senha invalida!", category="error")
            print("senha invalida")
            return render_template("turmas/validate.jinja2", turma=turma)

        return redirect(url_for("turmas.index"))
