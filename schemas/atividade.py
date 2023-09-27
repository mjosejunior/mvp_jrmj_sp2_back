
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time
from schemas import ObservacaoSchema
from flask import jsonify




class AtividadeSchema(BaseModel):
    """Define como uma nova atividade a ser inserida deve ser representada."""
    id: Optional[int] = 1
    data: Optional[date] = date(2023, 1, 1)
    start_time: Optional[time] = time(8, 30)
    end_time: Optional[time] = time(11, 30)
    duracao: Optional[float] = 3.0
    publicacoes: Optional[int] = 3
    videos: Optional[int] = 2
    revisitas: Optional[int] = 1
    estudos: Optional[int] = 1
    latitude: Optional[float] = 25.761431
    longitude: Optional[float] = -80.195080
    endereco: Optional[str] = "Rua X, 123"

    def serializar(self):
        return self.dict()


class UpdateAtividadeSchema(BaseModel):
    """Define como uma atividade pode ser atualizada pelo ID."""

    id: int
    data: date = date(2023, 1, 1)
    start_time: Optional[time] = time(8, 30)
    end_time: Optional[time] = time(11, 30)
    duracao: Optional[float] = 3.0
    publicacoes: Optional[int] = 3
    videos: Optional[int] = 2
    revisitas: Optional[int] = 1
    estudos: Optional[int] = 1
    latitude: Optional[float] = 25.761431
    longitude: Optional[float] = -80.195080
    endereco: Optional[str] = ""
    

    def serialize(self):
        return self.dict()


class AtividadeBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base na data da atividade.
    """
    data: date = date(2023, 1, 1)

    def serializar(self):
        return self.dict()


class AtividadeBuscaIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base na data da atividade.
    """
    id: int = 1

    def serializar(self):
        return self.dict()


class ListagemAtividadesSchema(BaseModel):
    """ Define como uma listagem de atividades será retornada.
    """
    atividades: List[AtividadeSchema]


def apresenta_atividades(atividades_serializadas):
  return {"atividades": atividades_serializadas}





class AtividadeViewSchema(BaseModel):
    """ Define como uma atividade será retornada: atividade + observações.
    """
    id: Optional[int]
    data: Optional[date]
    start_time: Optional[time]
    end_time: Optional[time]
    duracao: Optional[float]
    publicacoes: Optional[int]
    videos: Optional[int]
    revisitas: Optional[int]
    estudos: Optional[int]
    total_observacoes: Optional[int]
    observacoes: List[ObservacaoSchema]


class AtividadeDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    id: int


#def apresenta_atividade(atividade, message):
 #   return jsonify({"atividade": atividade.to_dict(), "message": message})

def apresenta_atividade(atividade, message):
    atividade_data = atividade.to_dict()
    
    # Buscando as observações relacionadas à atividade
    observacoes = atividade.observacoes
    observacoes_data = [obs.to_dict() for obs in observacoes]

    response = {
        "message": message,
        "atividade": atividade_data,
        "observacoes": observacoes_data
    }

    return jsonify(response)


