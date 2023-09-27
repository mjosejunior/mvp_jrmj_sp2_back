from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from model import Base


class Observacao(Base):
    __tablename__ = 'observacao'

    id = Column(Integer, primary_key=True)
    texto = Column(String(4000))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre a observação e uma atividade.
    # Aqui está sendo definido a coluna 'atividade' que vai guardar
    # a referencia a atividade, a chave estrangeira que relaciona
    # uma atividade a observação.
    atividade = Column(Integer, ForeignKey(
        "atividade.pk_atividade"), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'texto': self.texto,
            'data_insercao': self.data_insercao.strftime("%Y-%m-%d %H:%M:%S"),
        }
    def serializar(self):
        return {
            "id": self.id,
            "texto": self.texto,
            "data_insercao": self.data_insercao.strftime("%Y-%m-%d %H:%M:%S")
        }
    def __init__(self, texto: str, data_insercao: Union[DateTime, None] = None):
        """
        Cria uma observação

        Arguments:
            texto: o texto de uma observação.
            data_insercao: data de quando a observação foi feita ou inserida
                           à base
        """
        self.texto = texto
        if data_insercao:
            self.data_insercao = data_insercao
