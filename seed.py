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
        "resposta": "verdadeiro", 
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
    }
]