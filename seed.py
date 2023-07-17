from datetime import datetime

professores = [
    {"nome": "Fallenzao", "matricula": "456",
        "email": "456@unb.com", "senha": "123", "tipo_usuario": "professor"}
]

estudantes = [
    {"nome": "Joao das Neves", "matricula": "123",
        "email": "123@unb.com", "senha": "123", "tipo_usuario": "estudante"},
    {"nome": "Pedro Pedrosa", "matricula": "321",
        "email": "pedro@unb.com", "senha": "asdfg", "tipo_usuario": "estudante"},
    {"nome": "Ester da Silva", "matricula": "231",
        "email": "ester@unb.com", "senha": "asdfg", "tipo_usuario": "estudante"}
]

turmas = [
    {
        "nome": "OAC",
        "horario_inicio": datetime.strptime("16:00:00", "%H:%M:%S").time(),
        "horario_fim": datetime.strptime("17:50:00", "%H:%M:%S").time(),
        "senha": "123",
        "semestre": "3",
        "professor_id": "1"
    }
]

aulas = [
    {
        "turma_id": "1",
        "data_aula": datetime.strptime("25/05/2023", "%d/%m/%Y").date(),
        "status": "em andamento"
    }
]

questoes = [
    {
        "enunciado": "Joao das neves nao sabia de nada", 
        "resposta": "Verdadeiro", 
        "tipo_questao": "verdadeiro_falso", 
        "professor_id": "1"
    },
    {
        "enunciado": "Luffy é o melhor protagonista de todos ? Por que sim ?", 
        "resposta": "", 
        "tipo_questao": "dissertativa", 
        "professor_id": "1"
    },
    {
        "enunciado": "Em que ano teve o bug do milenio ?", 
        "resposta": "2000", 
        "tipo_questao": "numerica", 
        "professor_id": "1"
    },
    {
        "enunciado": " One Piece é um mangá e anime criado por Akira Toriama.", 
        "resposta": "Falso", 
        "tipo_questao": "verdadeiro_falso", 
        "professor_id": "2"
    },
    {
        "enunciado": "Por que Goldo Roger riu ao chegar a Laught Tale?", 
        "resposta": "", 
        "tipo_questao": "dissertativa", 
        "professor_id": "1"
    }
]

questoes_multipla_escolha = [
    {
        "enunciado": "Assinale a alternativa correta sobre Shanks O Brabo:", 
        "resposta": "A", 
        "tipo_questao": "multipla_escolha", 
        "professor_id": "1",
        "opcao_a": "É ruivo", 
        "opcao_b": "É vilao", 
        "opcao_c": "Tem irmao gemeo", 
        "opcao_d": "É o goldo roger disfarçado"
    },
    {
        "enunciado": "Qual é o nome do primeiro navio dos Chapéus de Palha?", 
        "resposta": "B", 
        "tipo_questao": "multipla_escolha", 
        "professor_id": "2",
        "opcao_a": "Thousand Sunny", 
        "opcao_b": "Going Merry", 
        "opcao_c": "Red Force", 
        "opcao_d": "Whitebeard"
    }
]

exames = [
    {   # exame encerrado e não respondidos
        "data_inicio": datetime.strptime("2023-05-12T16:00", "%Y-%m-%dT%H:%M"),
        "data_fim": datetime.strptime("2023-05-15T16:00", "%Y-%m-%dT%H:%M"),
        "nome": "Prova 1",
        "nota_exame": "10",
        "professor_id": "1",
        "turma_id": "1",
    },
    {   # exame encerrado e respondidos
        "data_inicio": datetime.strptime("2023-06-21T16:00", "%Y-%m-%dT%H:%M"),
        "data_fim": datetime.strptime("2023-06-23T16:00", "%Y-%m-%dT%H:%M"),
        "nome": "Prova 2",
        "nota_exame": "10",
        "professor_id": "1",
        "turma_id": "1",
    },
    {   # exame agendado
        "data_inicio": datetime.strptime("2023-08-01T16:00", "%Y-%m-%dT%H:%M"),
        "data_fim": datetime.strptime("2023-08-03T16:00", "%Y-%m-%dT%H:%M"),
        "nome": "Prova 3",
        "nota_exame": "10",
        "professor_id": "1",
        "turma_id": "1",
    },
    {   # exame em aberto e não respondidos
        "data_inicio": datetime.strptime("2023-07-17T16:00", "%Y-%m-%dT%H:%M"),
        "data_fim": datetime.strptime("2023-07-19T16:00", "%Y-%m-%dT%H:%M"),
        "nome": "Prova 4",
        "nota_exame": "10",
        "professor_id": "1",
        "turma_id": "1",
    },
    {   # exame em aberto e respondidos
        "data_inicio": datetime.strptime("2023-05-15T16:00", "%Y-%m-%dT%H:%M"),
        "data_fim": datetime.strptime("2023-07-17T16:00", "%Y-%m-%dT%H:%M"),
        "nome": "Prova 5",
        "nota_exame": "10",
        "professor_id": "1",
        "turma_id": "1",
    }
]

questoes_exames = [
    { # questoes exame 1
       "exame_id": "1",
       "questao_id": "1",
        "nota_questao": "5" 
    },
    {
       "exame_id": "1",
       "questao_id": "2",
        "nota_questao": "5" 
    },
    { # questoes exame 2
       "exame_id": "2",
       "questao_id": "3",
        "nota_questao": "4.5" 
    },
    {
       "exame_id": "2",
       "questao_id": "4",
        "nota_questao": "5.5" 
    },
    { # questoes exame 3
       "exame_id": "3",
       "questao_id": "5",
        "nota_questao": "3.5" 
    },
    {
       "exame_id": "3",
       "questao_id": "6",
        "nota_questao": "6.5" 
    },
    { # questoes exame 4
       "exame_id": "4",
       "questao_id": "3",
        "nota_questao": "4.5" 
    },
    {
       "exame_id": "4",
       "questao_id": "7",
        "nota_questao": "5.5" 
    },
    { # questoes exame 5
       "exame_id": "5",
       "questao_id": "6",
        "nota_questao": "7.5" 
    },
    {
       "exame_id": "5",
       "questao_id": "2",
        "nota_questao": "2.5" 
    }
]

respostas_questoes_exames = [
    { # respostas ester ao exame 2
        "resposta_estudante": "2000",
        "nota_estudante_questao": "4.5",
        "estudante_id": "4",
        "exame_id": "2",
        "questao_id": "3"
    },
    {
        "resposta_estudante": "Verdadeiro",
        "nota_estudante_questao": "0",
        "estudante_id": "4",
        "exame_id": "2",
        "questao_id": "4"
    },
    { # respostas ester ao exame 5
        "resposta_estudante": "A",
        "nota_estudante_questao": "7.5",
        "estudante_id": "4",
        "exame_id": "5",
        "questao_id": "6"
    },
    {
        "resposta_estudante": "Pq ele é de borracha e estica",
        "nota_estudante_questao": "2.5",
        "estudante_id": "4",
        "exame_id": "5",
        "questao_id": "2"
    },
]

notas_exames = [
    {
        "exame_id": "2",
        "estudante_id": "4",
        "nota_exame": "4.5"
    },
    {
        "exame_id": "5",
        "estudante_id": "4",
        "nota_exame": "10"
    }
]