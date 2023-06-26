import qrcode
from app.models.aula import Aula
from io import BytesIO


def gerar_qrcode(data: str):
    """
    gera um qrcode com base no dado 'data' e 
    retorna um buffer contendo uma imagem

    :data: string do dado que o qrcode vai ser gerado
    :return: Image Buffer
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    return img_buffer


def qrcode_isvalid(qrcode_data: str, aula_id: int) -> bool:
    """
    verifica se o qrcode eh igual ao token da aula

    :qrcode_data: dado extraido do qrcode
    :aula_id: id da aula em questao
    :return: boolean
    """
    aula = Aula.query.filter_by(id=aula_id).first()
    return aula.token == qrcode_data
