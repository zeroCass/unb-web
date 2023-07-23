from ..webapp import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Questao, Professor, QuestaoMultiplaEscolha
from typing import Union

bp = Blueprint("questoes", __name__)

@bp.route("/professor/<int:professor_id>", methods=["GET"])
@login_required
def index(professor_id: int) -> render_template:
    """Renderiza a página que lista todas as questões cadastradas
    pelo professor de acordo com seu id

    Args:
        professor_id: id do usuario
    Returns:
        Redireciona para a página de lista questões do professor
    """

    # Verificar se o usuário logado é um professor
    if not isinstance(current_user, Professor):
        flash("Acesso não autorizado", category="warning")
        return render_template("index.jinja2", user=current_user)
    
    # Obtendo as questões relacionadas ao usuário
    questoes = Questao.query.filter_by(professor_id=professor_id).all()
    questoes_multipla_escolha = QuestaoMultiplaEscolha.query.filter_by(professor_id=professor_id).all()

    return render_template('questoes/index.jinja2', questoes=questoes, questoes_multipla_escolha=questoes_multipla_escolha)


@bp.route("/professor/<int:professor_id>/new", methods=["GET"])
@login_required
def new(professor_id: int) -> render_template:
    """Renderiza a página de criação de questão

    Args:
        professor_id: id do usuario
    Returns:
        Redireciona para a página de criação de questão
    """
    return render_template("questoes/new.jinja2", professor_id=professor_id)


@bp.route("/professor/<int:professor_id>/create", methods=["POST"])
@login_required
def create(professor_id: int) -> redirect:
    """Cria uma instancia de questão no banco de dados de acordo
    com os dados passado via formulario

    Args:
        professor_id: id do usuario
    Returns:
        Redireciona para a página de lista questões do professor
    """

    enunciado = request.form['enunciado']
    tipo_questao = request.form['tipo_questao']
    opcao_a = request.form.get('opcao_a')
    opcao_b = request.form.get('opcao_b')
    opcao_c = request.form.get('opcao_c')
    opcao_d = request.form.get('opcao_d')
    resposta = request.form['resposta']
    professor_id = professor_id

    # Cria uma nova instância da classe Questao
    if(tipo_questao == "multipla_escolha"):
        nova_questao = QuestaoMultiplaEscolha(enunciado=enunciado, tipo_questao=tipo_questao, opcao_a=opcao_a, opcao_b=opcao_b, opcao_c=opcao_c, opcao_d=opcao_d, resposta=resposta, professor_id=professor_id)
    else:
        nova_questao = Questao(enunciado=enunciado, tipo_questao=tipo_questao, resposta=resposta, professor_id=professor_id)
    
    # Salva a nova questão no banco de dados
    try:
        db.session.add(nova_questao)
        db.session.commit()
        flash("Questao criada", category="success")
    except Exception:
        db.session.rollback()
        flash("Erro ao criar Questao", category="error")

    return redirect(url_for('questoes.index', professor_id=professor_id))


@bp.route("/professor/<int:professor_id>/edit/<int:questao_id>", methods=['GET', 'POST'])
@login_required
def edit(professor_id: int, questao_id: int) -> Union[redirect,render_template]:
    """Se o tipo de requisição for GET, renderiza a pagina de edição
    Se o tipo de quisição for POST, realiiza a edição de uma questão dado seu id

    Args:
        professor_id: id do usuario
        questao_id: id da questao
    Returns:
        Redireciona para a página de lista questões do professor caso seja um post
        Redireciona para a pagina de edição caso seja um get
    """



    questao = Questao.query.get_or_404(questao_id)
    if request.method == "POST":
        novo_enunciado = request.form.get('enunciado')
        nova_resposta = request.form.get('resposta')

        # Atualizar os campos desejados da questão com os novos valores
        questao.enunciado = novo_enunciado
        if questao.tipo_questao != "dissertativa":
            questao.resposta = nova_resposta
   
        try:
            db.session.commit()
            flash('Questão atualizada com sucesso', 'success')
        except Exception:
            db.session.rollback()
            flash("Erro ao atualizar Questao", category="warning")
        return redirect(url_for('questoes.index', professor_id=professor_id))
    return render_template("questoes/edit.jinja2", professor_id=professor_id, questao=questao)
        
    
@bp.route("/professor/<int:professor_id>/edit/multipla_escolha/<int:questao_id>", methods=['GET', 'POST'])
@login_required
def edit_multipla_escolha(professor_id: int, questao_id: int) -> Union[redirect,render_template]:
    """Se o tipo de requisição for GET, renderiza a pagina de edição 
    Se o tipo de quisição for POST, realiiza a edição de uma questão dado seu id

    Args:
        professor_id: id do usuario
        questao_id: id da questao
    Returns:
        Redireciona para a página de lista questões do professor caso seja um post
        Redireciona para a pagina de edição caso seja um get
    """

    questao_multipla_escolha = QuestaoMultiplaEscolha.query.get_or_404(questao_id)

    if request.method == "POST":
        novo_enunciado = request.form.get('enunciado')
        opcao_a = request.form.get('opcao_a')
        opcao_b = request.form.get('opcao_b')
        opcao_c = request.form.get('opcao_c')
        opcao_d = request.form.get('opcao_d')
        nova_resposta = request.form.get('resposta')

        # Atualizar os campos desejados da questão com os novos valores
        questao_multipla_escolha.enunciado = novo_enunciado
        questao_multipla_escolha.opcao_a = opcao_a
        questao_multipla_escolha.opcao_b = opcao_b
        questao_multipla_escolha.opcao_c = opcao_c
        questao_multipla_escolha.opcao_d = opcao_d
        questao_multipla_escolha.resposta = nova_resposta  

        try:
            db.session.commit()
            flash('Questão atualizada com sucesso', 'success')
        except Exception:
            db.session.rollback()
            flash("Erro ao atualizar Questao", category="warning")
        
        return redirect(url_for('questoes.index', professor_id=professor_id))
    return render_template("questoes/edit_multipla_escolha.jinja2", professor_id=professor_id, questao_multipla_escolha=questao_multipla_escolha)


@bp.route("/professor/<int:professor_id>/delete/<int:questao_id>", methods=['POST'])
@login_required
def delete(professor_id: int, questao_id: int) -> redirect:
    """Delete uma questão do banco de dados dado seu id
    e seu tipo

    Args:
        professor_id: id do usuario
        questao_id: id da questao
    Returns:
        Redireciona para a página de lista questões do professor
    """

    questao = Questao.query.get_or_404(questao_id)

    # Verifica se a questão é uma questão de múltipla escolha
    if (questao.tipo_questao == "multipla_escolha"):
        
        questao_multipla_escolha = QuestaoMultiplaEscolha.query.get_or_404(questao_id)
        # Remove as opções de múltipla escolha associadas à questão
        questao_multipla_escolha.opcao_a = None
        questao_multipla_escolha.opcao_b = None
        questao_multipla_escolha.opcao_c = None
        questao_multipla_escolha.opcao_d = None
        try:
            db.session.delete(questao_multipla_escolha)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash("Erro ao excluir questão de múltipla escolha", category="error")
            return redirect(url_for('questoes.index', professor_id=professor_id))
    else:
        try:
            db.session.delete(questao)
            db.session.commit()
            flash('Questão excluída com sucesso', 'success')
        except Exception:
            db.session.rollback()
            flash("Erro ao excluir questão", category="error")

    return redirect(url_for('questoes.index', professor_id=professor_id))
