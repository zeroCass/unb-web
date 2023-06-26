import threading
from ..models import Aula, Turma
from ..webapp import db
from datetime import datetime
import time
from app import logger

# Função para verificar e atualizar o status das aulas


def verificar_status_aulas(app):
    with app.app_context():
        logger.info("Thread para verificar status das aulas iniciada")
        while True:
            # Obter a data e hora atual
            now = datetime.now()

            # Verificar todas as aulas do dia atual
            aulas_do_dia = Aula.query.filter_by(data_aula=now.date()).all()
            for aula in aulas_do_dia:
                logger.info(
                    f"Aula: {aula.id} - {aula.token} -m {aula.turma_id}")

                if aula.status == "finalizado":
                    continue

                turma = Turma.query.filter_by(id=aula.turma_id).first()

                logger.info(
                    f"A turma da aula {aula.id} eh: turma: {turma.id} - {turma.nome}")

                horario_inicio = datetime.combine(
                    now.date(), turma.horario_inicio)
                horario_fim = datetime.combine(now.date(), turma.horario_fim)

                # Verificar o status da aula e atualizá-lo conforme necessário
                if horario_inicio <= now <= horario_fim:
                    aula.status = "em andamento"
                elif now > horario_fim:
                    aula.status = "finalizado"

            # Salvar as alterações no banco de dados
            db.session.commit()

            time.sleep(30)
