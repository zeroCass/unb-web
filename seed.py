from datetime import datetime


alunos = [
    {"nome": "Joao das Neves", "matricula": "123",
        "email": "123@unb.com", "senha": "123", "tipo_usuario": "aluno"}
]

professores = [
    {"nome": "Fallenzao", "matricula": "456",
        "email": "456@unb.com", "senha": "123", "tipo_usuario": "professor"}
]

turmas = [
    {
        "nome": "OAC",
        "horario_inicio": datetime.strptime("16:00:00", "%H:%M:%S").time(),
        "horario_fim": datetime.strptime("17:50:00", "%H:%M:%S").time(),
        "senha": "123",
        "semestre": "3",
        "professor_id": "2"
    }
]

aulas = [
    {
        "turma_id" : "1",
        "data_aula": datetime.strptime("25/05/2023", "%d/%m/%Y").date(),
        "status": "em andamento"
    }
]