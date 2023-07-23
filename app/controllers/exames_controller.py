from ..webapp import db
from flask import Blueprint, render_template, request, redirect, url_for, flash, json
from flask_login import login_required, current_user
from ..models import Turma, Exame, Questao, QuestaoMultiplaEscolha, QuestaoExame, RespostaQuestaoExame, NotasExames, Estudante
from datetime import datetime, timedelta
from app.utils.decorators import load_parent_resource_factory
import json
import re

bp = Blueprint("exames", __name__)
parent_model = Turma


def register_blueprint(parent_blueprint: Blueprint) -> None:
    """Registra essa rota (blueprint) como parte
    da rota do pai. Dessa forma, o rota desse blueprint será
    composta com a rota do pai como prefixo

    Args:
        O blueprint do pai
    """
    parent_blueprint.register_blueprint(
        bp, url_prefix=f"/<int:turma_id>/exames")

# decorator com config especifica para aulas
load_parent = load_parent_resource_factory(parent_model, "turma_id")

@bp.route("/new", methods=["GET"])
@login_required
@load_parent
def new(turma: Turma) -> redirect:
    """Rendereza a pegina de exame passando para o template
    todas as questoes que o professor possui em seu banco de questões

    Args:
        turma: instancia da model Turma de acordo com turma_id receibodo da rota
        e invocado atraves do decorator @load_parent
    Retunrs:
        redireciona para a página de criação de exame
    """
    questoes = Questao.query.filter_by(professor_id=current_user.id).all()

    # transforma questoes em um json para o js acessar
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
def create(turma_id: int) -> redirect:
    """Cria uma instancia de turma e insere no banco de dados
    de acordo com os campos do formlario recebido

    Args:
        turma_id: id da turma que o exame irá estar relacionado 
    Retunrs:
        redireciona para a página de turmas
    """

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
        db.session.flush()  # atualiza 

        # adicionar questoes e seus valores na tabela questao_exame (table associativa)
        for questao in questoes_selecionadas:
            association = QuestaoExame(exame_id=new_exame.id, questao_id=questao["questao_id"],
                            nota_questao=questao["nota_questao"])
            db.session.add(association)

        db.session.commit()
        flash("Exame criado", category="success")
    except Exception as e:
        db.session.rollback()
        print(e)
        flash("Erro ao criar Exame", category="error")

    return redirect(url_for("turmas.show", turma_id=turma_id))


@bp.route("<int:exame_id>/check_date", methods=['GET'])
@login_required
def check_date(turma_id: int, exame_id: int) -> redirect:
    """Verifica a data e/ou o tipo de usuario e então redireciona-o para uma página 
    Se for um professor, irá redirecionar para a rota show
    Se for uma estudante, verifica a data/hora está no prazo do exame
        Se já estiver dentro do prazo, redireciona para a página de realização do exame
        Se o exame já expirou, então verifica se o estudante tem nota, se tiver redireciona ele para
        a pagina de visualização do exame
        Se o exame já expirou e o aluno não tem nota, então exibe mensagem de erro

    Args:
        turma_id: id da turma
        exame_id: id do exame
    Retunrs:
        redireciona para páginas diferentes dependendo do usuario, data/hora
    """

    # Verifica se o usuario é o professor
    if current_user.tipo_usuario == "professor":
        return show(turma_id, exame_id)

    exame = Exame.query.filter_by(id=exame_id).first()
    nota = NotasExames.query.filter_by(estudante_id=current_user.id, exame_id=exame.id).first()
    # Obter a data e hora atual
    data_atual = datetime.now()
    
    
    
    # Verifica se o exame está dentro do prazo de realização
    if exame.data_inicio <= data_atual <= exame.data_fim:
        if nota:
            flash("Você já realizou este exame. Espere prazo de encerramento do mesmo para vizualizar suas respostas e nota!", category="warning")
            return redirect(url_for("turmas.show", turma_id=turma_id))
        else:
            # Caso o exame esteja dentro do prazo, redirecionar para a página do exame
            return show(turma_id, exame_id)

    # Caso o exame já tenha expirado
    elif exame.data_fim < data_atual:
        if nota:
            # Se o aluno já tiver realizado o exame, redirecionar para a página de respostas
            flash("Você já realizou este exame.", category="info")
            return resposta_exame(turma_id, exame_id, estudante_id=current_user.id)
        else:
            # Se o aluno não tiver realizado o exame, redirecionar para a página com a nota e respostas indisponíveis
            flash("Atenção: O prazo para realizar este exame já expirou.", category="warning")
            return redirect(url_for("turmas.show", turma_id=turma_id))
        
    # Exame agendado (data futura)
    elif exame.data_inicio > data_atual:
        flash(f"Este exame está agendado para {exame.data_inicio}. Por favor, aguarde para realizar o exame.", category="warning")
        return redirect(url_for('turmas.show', turma_id=turma_id))

    # Caso de erro desconhecido ou situação inválida
    else:
        flash("Erro desconhecido ao verificar o exame.", category="error")
        return redirect(url_for("turmas.show", turma_id=turma_id))

 
@bp.route("<int:exame_id>/show", methods=['GET'])
@login_required
def show(turma_id: int, exame_id: int) -> render_template:
    """Renderiza a página de visualização do exame,
    onde será possivel realizar o exame caso o usuario seja estudante

    Args:
        turma_id: id da turma
        exame_id: id do exame
    Retunrs:
        redireciona para página de visualização do exame
    """

    exame = Exame.query.filter_by(id=exame_id).first()

    # cria json com informcaoes do horario de realizacao do exame para acessar no js
    exame_horario = json.dumps({
        "dataInicio": exame.data_inicio.strftime("%Y-%m-%d %H:%M:%S"),
        "dataFim": exame.data_fim.strftime("%Y-%m-%d %H:%M:%S"),
    })

    questoes_exame = exame.questoes # tabela associativa
    
    # Obtendo as opções da questão de múltipla escolha
    for questao_exame in questoes_exame:
        if questao_exame.questao.tipo_questao == "multipla_escolha":
            multipla_escolha = QuestaoMultiplaEscolha.query.filter_by(id=questao_exame.questao.id).all()
            questao_exame.questao.opcoes = multipla_escolha
    return render_template("exames/show.jinja2", turma_id=turma_id, exame=exame, questoes_exame=questoes_exame, exame_horario=exame_horario)


@bp.route("<int:exame_id>/submit", methods=['POST'])
@login_required
def submit(turma_id: int, exame_id: int) -> redirect:
    """Faz o submit do formulario do exame com as respostas
    do estudante

    Args:
        turma_id: id da turma
        exame_id: id do exame
    Retunrs:
        redireciona para páginas diferentes dependendo do usuario, data/hora
    """

   
    exame = Exame.query.filter_by(id=exame_id).first()
    # verifica se a sumissão é valida
    if not time_is_in_rage(exame.data_inicio, exame.data_fim):
        flash("Erro ao enviar exame", category="error")
        return redirect(url_for("turmas.show", turma_id=turma_id))

    try:
        nota_exame = 0
        for questao in request.form:
                questao_id = re.search("\d+$", questao)[0]  # extrai somente os ultimos numeros de uma string
                questao_db = Questao.query.filter_by(id=questao_id).first()
                questao_exame = QuestaoExame.query.filter_by(exame_id=exame_id, questao_id=questao_id).first()
                
                resposta_estudante =  request.form[questao]
                nota_estudante_questao = 0

                if questao_db.tipo_questao == "dissertativa":
                    if resposta_estudante and resposta_estudante.strip() != "":
                        nota_exame += questao_exame.nota_questao
                        nota_estudante_questao = questao_exame.nota_questao
                elif questao_db.resposta.lower() == resposta_estudante.lower():
                    nota_exame += questao_exame.nota_questao
                    nota_estudante_questao = questao_exame.nota_questao
                
                # print(f"Questao ID: {questao_db.id} - nota:{questao_exame.nota_questao} \
                #     resposta_estudante: {resposta_estudante} - resposta_questao: {questao_db.resposta} \
                #         acertou: {acertou}")
                
                # print(f"questao[{questao_id}]: {questao} - resposta: {request.form[questao]}")

                resposta_questao_exame = RespostaQuestaoExame(estudante_id=current_user.id, exame_id=exame_id,
                                            questao_id=questao_id, resposta_estudante=resposta_estudante, 
                                            nota_estudante_questao=nota_estudante_questao)
                db.session.add(resposta_questao_exame)
        notas_exames = NotasExames(exame_id=exame_id, estudante_id=current_user.id, nota_exame_estudante=nota_exame)
        db.session.add(notas_exames)
        db.session.commit()
        flash("Exame enviado com sucesso!", category="success")
    except Exception as e:
        print(e)
        flash("Erro ao enviar exame", category="error")
    return redirect(url_for("turmas.show", turma_id=turma_id))


def time_is_in_rage(data_inicio: datetime, data_fim: datetime) -> bool:
    """  pure function usada para verificar se a data de submit
    está no range + 30s
    
    Args: 
        data_inicio: data de inicio do exame
        data_fim: data de fim do exame
        
    Retuns:
        Boolean indicando se a data atual está no range
    """
    new_data_fim = data_fim + timedelta(seconds=30)
    return data_inicio <= datetime.now() <= new_data_fim


@bp.route("<int:exame_id>/resposta/<int:estudante_id>", methods=['GET'])
@login_required
def resposta_exame(turma_id: int, exame_id: int, estudante_id: int) -> redirect:
    """ Consulta os dados de exame para passar para o template
    montar o exame com as respostas do estudante
    
    Args: 
        turma_id: id da turma
        exame_id: id do exame
        estudante_id: id do estudante
        
    Retuns:
        Redireciona para a página do exame contendo as resposta do estudante
    """

    try:
        exame = Exame.query.filter_by(id=exame_id).first()
        questoes_exame = [] # tabela associativa

        for questao_exame in  exame.questoes:
            questao = questao_exame.questao
            questao.nota_questao = questao_exame.nota_questao # atribui nota ao objeto
            questao.anulada = questao_exame.anulada
            
            print(f"Questao: {questao}")

            if questao_exame.questao.tipo_questao == "multipla_escolha":
                multipla_escolha = QuestaoMultiplaEscolha.query.filter_by(id=questao.id).all()
                questao.opcoes = multipla_escolha

            resposta_questao_exame = RespostaQuestaoExame.query.filter_by(
                estudante_id=estudante_id,exame_id=exame_id, questao_id=questao.id).first()
            
            questao.resposta_estudante = resposta_questao_exame.resposta_estudante
            questao.nota_estudante_questao = resposta_questao_exame.nota_estudante_questao
            questoes_exame.append(questao)
        
        # for questao in questoes_exame:
        #     print(f"id:{questao.id} enunciado {questao.enunciado} \
        #             nota_questao: {questao.nota_questao} nota_estudante: {questao.nota_estudante_questao} \
        #             resposta: {questao.resposta} resposta_estudante: {questao.resposta_estudante}")
        
        return render_template("exames/resposta_exame.jinja2", turma_id=turma_id, exame=exame, estudante_id=estudante_id, questoes_exame=questoes_exame)
        # return render_template("exames/resposta_exame.jinja2", turma_id=turma_id, exame=exame, questoes_exame=questoes_exame)
    except Exception as e:
        print(e)
        flash(f"Error: {e}", category="error")
        return redirect(url_for("turmas.show", turma_id=turma_id))


@bp.route("<int:exame_id>/notas", methods=['GET'])
@login_required
def notas(turma_id: int, exame_id: int) -> render_template:
    """ Consulta as notas de todos os estudantes que realizaram um
    determinado exame
    
    Args: 
        turma_id: id da turma
        exame_id: id do exame
        
    Retuns:
        Redireciona para a página de notas
    """

    # preveni o estudante de acessar a rota
    if current_user.tipo_usuario == "estudante":
        flash("Você não tem permissão realizar esta operação")
        return redirect(url_for("turmas.show", turma_id=turma_id))

    notas_exame = db.session.query(NotasExames, Estudante).join(Estudante).filter(NotasExames.exame_id == exame_id).all()
    exame = Exame.query.filter_by(id=exame_id).first()
    return render_template("exames/notas_exame.jinja2", notas_exame=notas_exame, exame=exame, turma_id=turma_id)


@bp.route("<int:exame_id>/delete", methods=['GET'])
@login_required
def delete(turma_id: int, exame_id: int):
    exame = Exame.query.get_or_404(exame_id)
    
    # Verificar se existem respostas e notas atribuidas a um exame
    if exame.respostas and exame.notas:
        # Se existirem, não é permitido a exclusão
        flash("Não é possível excluir o exame porque já foi respondido por estudantes.", category="error")
        return redirect(url_for("turmas.show", turma_id=turma_id))
    
    try:
        #Se nao tenta fazer a exclusão do exame
        db.session.delete(exame)
        db.session.commit()
        flash("Exame excluido com sucesso.", category="success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir o exame: {e}", category="error")
    return redirect(url_for("turmas.show", turma_id=turma_id))


@bp.route("<int:exame_id>/editar_nota_estudante/<int:estudante_id>/questao/<int:questao_id>", methods=['POST'])
@login_required
def editar_questao_exame(turma_id: int, exame_id: int, estudante_id: int, questao_id: int) -> redirect:
    """ Edita a nota do estuante em uma questao ed um exame especifico,
        ou anula uma questao com base as informações submetidas pelo formulário no modal
    
    Args:
        turma_id: id da turma
        exame_id: id do exame
        estudante_id: id do estudante
        questao_id: id da questão no exame
        
    Returns:
        Redireciona para a página de exame com as respostas atualizadas
    """
    try:
        exame = Exame.query.get(exame_id)

        if exame.data_fim >= datetime.now():
            flash("Não foi possivel aplicas as alterações pois o tempo de realização do exame ainda não expirou.", category="error")
            return redirect(url_for("turmas.exames.resposta_exame", turma_id=turma_id, exame_id=exame_id, estudante_id=estudante_id))

        nova_nota_estudante = float(request.form['nota_estudante'])
        questao_anulada = request.form['questao_anulada']

        questao_exame = QuestaoExame.query.filter_by(exame_id=exame_id, questao_id=questao_id).first()
        # Recupera a resposta da questão a ser editada
        resposta_questao_exame = RespostaQuestaoExame.query.filter_by(
            estudante_id=estudante_id, exame_id=exame_id, questao_id=questao_id).first()

        # Atualiza os valores com as informações do formulário
        if questao_anulada == "True":
            resposta_questao_exame.nota_estudante_questao = questao_exame.nota_questao
            questao_exame.anulada = True
        else:
            resposta_questao_exame.nota_estudante_questao = nova_nota_estudante
            questao_exame.anulada = False

        # Salva as alterações no banco de dados
        db.session.commit()

        flash("Alterações feitas com sucesso!", category="success")

    except Exception as e:
        print(e)
        flash(f"Erro ao editar questão: {e}", category="error")

    # Redireciona para a página de exame
    return redirect(url_for("turmas.exames.resposta_exame", turma_id=turma_id, exame_id=exame_id, estudante_id=estudante_id))
