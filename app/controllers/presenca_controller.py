from ..webapp import db
from flask import Blueprint, send_file, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Aula, Presenca, Estudante
from app.utils.qrcode import gerar_qrcode, qrcode_isvalid
from datetime import datetime
from flask_login import login_required, current_user
import base64
from typing import Union

bp = Blueprint("presenca", __name__)


def register_blueprint(parent_blueprint: Blueprint)-> None:
    """Registra essa rota (blueprint) como parte
    da rota do pai. Dessa forma, o rota desse blueprint será
    composta com a rota do pai como prefixo

    Args:
        O blueprint do pai
    """
    parent_blueprint.register_blueprint(
        bp, url_prefix=f"/<int:aula_id>/presenca")


@bp.route("/", methods=["POST", "GET"])
@login_required
def registrar_presenca(turma_id: int, aula_id: int) -> Union[redirect,render_template]:
    """Registra a presenca de uma estudante, caso não haja regristo

    Args:
        turma_id: id da turma
        aula_id: id da aula
    Returns: 
        redireciona para a pagina de exibicao de turma com 
        alguma mensagme de flash indicando o status da operacao
    """
    if request.method == "GET":
        return render_template("qrcode.jinja2", turma_id=turma_id, aula_id=aula_id)

    if request.method == "POST":

        data_atual = datetime.now()
        estudante_id = current_user.id

        # Verifica se o estudante já possui uma presença registrada para essa aula
        presenca_existente = Presenca.query.filter_by(
            aula_id=aula_id, estudante_id=estudante_id).first()
        if presenca_existente:
            flash("Presença já foi registrada", category="warning")
        else:
            qrcode_content = request.form.get("qrcode-content")
            # print(f"PRESENCA: POST {qrcode_content}")
            if qrcode_isvalid(qrcode_content, aula_id):
                presenca = Presenca(
                    aula_id=aula_id, data=data_atual, estudante_id=estudante_id)

                db.session.add(presenca)
                db.session.commit()

                flash("Chamada Assinada", category="sucess")
            else:
                flash("Qrcode inválido", category="error")

        flash("Chamada Assinada", category="sucess")
        return redirect(url_for("turmas.show", turma_id=turma_id))
        
@bp.route("/estudantes", methods=["GET"])
@login_required
def listar_presencas(turma_id: int, aula_id: int) -> render_template:
    """Renderiza a página contendo todos os alunos que assinaram a 
    presençã de uma determina aula

    Args:
        turma_id: id da turma 
        aula_id: id da aula
    Returns:
        Redireciona para a página de presenças
    """

    aula = Aula.query.get(aula_id)
    estudantes = Estudante.query.all()
    presencas = Presenca.query.filter_by(aula_id=aula_id).all()
    
    return render_template("aulas/presencas.jinja2", aula=aula, estudantes=estudantes, presencas=presencas)


@bp.route("/qrcode", methods=["GET"])
@login_required
def qrcode(turma_id: int, aula_id: int) -> send_file:
    """Gera uma imagem qrcode baseado no token da aula
    
    Args:
        turma_id: id da turma
        aula_id: id da aula
    Returns: 
        imagem para ser renderizado no template jinja
    """

    aula = Aula.query.filter_by(id=aula_id).first()
    print(f"aula token: {aula.token} - aula id: {aula.id}")
    qrcode_image = gerar_qrcode(aula.token)

    return send_file(qrcode_image, mimetype="image/png")


@bp.route("/qrcode_page", methods=["GET"])
@login_required
def qrcode_page(turma_id: int, aula_id: int) -> render_template:
    """Gera uma imagem qrcode baseado no token da aula
    
    Args:
        turma_id: id da turma
        aula_id: id da aula
    Returns: 
        template jinja com imagem em base64 como parametro
    """

    aula = Aula.query.filter_by(id=aula_id).first()
    print(f"aula token: {aula.token} - aula id: {aula.id}")
    qrcode_image = gerar_qrcode(aula.token)

    imagem_base64 = base64.b64encode(qrcode_image.getvalue()).decode('utf-8')

    return render_template("aulas/qrcode.jinja2", qrcode_image=imagem_base64)
