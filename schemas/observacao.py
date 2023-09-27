
from pydantic import BaseModel


class ObservacaoSchema(BaseModel):
    """ Define como uma nova observação a ser inserida deve ser representada
    """
    atividade_id: int = 1
    texto: str = "Só registrar atividade se relamente tiver trabalhado!"


class ListagemObservacoesSchema(BaseModel):
    """ Define como uma nova observação a ser inserida deve ser representada
    """
    observacoes: list[ObservacaoSchema] = []


class ObservacaoViewSchema(BaseModel):
    """ Define como uma nova observação a ser inserida deve ser representada
    """
    id: int = 1
    texto: str = "Só registrar atividade se relamente tiver trabalhado!"
    data_insercao: str = "2021-08-30 00:00:00"
    atividade_id: int = 1


class ObservacaoBuscaAtividadeSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id da atividade.
    """
    id: int = 1

    def to_dict(self):
        return {
            "id": self.id,
            "texto": self.texto,
            "data_insercao": self.data_insercao.strftime("%Y-%m-%d %H:%M:%S"),
            "atividade_id": self.atividade_id
        }
    def serializar(self):
        return self.to_dict()
