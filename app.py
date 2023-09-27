from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, jsonify
from sqlalchemy.exc import SQLAlchemyError
import traceback
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Atividade, Observacao
from logger import logger
from schemas import *
from flask_cors import CORS
import requests

info = Info(title="Controle de Atividades - API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
atividade_tag = Tag(
    name="Atividade", description="Adição, visualização, Atualização e remoção de atividades à base")
observacao_tag = Tag(
    name="Observação", description="Adição de uma observação à uma atividade cadastrada na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


def geocodificacao_reversa(lat, lon):
    base_url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["display_name"]
    return None


@app.post('/atividade', tags=[atividade_tag],
          responses={"200": AtividadeViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_atividade(form: AtividadeSchema):
    """Adiciona uma nova Atividade à base de dados

    Retorna uma representação das atividades e observações associadas.
    """
    endereco = geocodificacao_reversa(form.latitude, form.longitude)
    if not endereco:
        return {"message": "Erro ao obter endereço."}, 400

    atividade = Atividade(
        data=form.data,
        start_time=form.start_time,
        end_time=form.end_time,
        duracao=form.duracao,
        publicacoes=form.publicacoes,
        videos=form.videos,
        revisitas=form.revisitas,
        estudos=form.estudos,
        latitude=form.latitude,
        longitude=form.longitude,
        endereco=endereco,
    )

    try:
        # criando conexão com a base
        session = Session()
        # adicionando atividade
        session.add(atividade)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado atividade de data: '{atividade.data}'")
        return apresenta_atividade(atividade, "Atividade adicionada com sucesso."), 200

    except IntegrityError as e:
        # como a duplicidade da data é a provável razão do IntegrityError
        error_msg = "Atividasde de mesma data já salva na base :/"
        logger.warning(
            f"Erro ao adicionar atividade '{atividade.data}', {error_msg}")
        return {"mesage": error_msg}, 409

    except SQLAlchemyError as e:
        # caso um erro no SQLAlchemy
        error_msg = "Erro no SQLAlchemy :/"
        logger.warning(
            f"Erro ao adicionar atividade '{atividade.data}', {error_msg}")
        return {"mesage": error_msg}, 400

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/ "
        logger.warning(
            f"Erro ao adicionar atividade '{atividade.data}', {error_msg}")
        logger.error(str(e))
        logger.error(e.__traceback__)
        logger.error(e.__cause__)
        logger.error(e.__context__)
        logger.error(e.__dict__)
        logger.error(traceback.print_exc())
        return jsonify({"message": error_msg, "error": str(e)}), 400


@app.get('/atividades', tags=[atividade_tag],
         responses={"200": ListagemAtividadesSchema, "404": ErrorSchema})
def get_atividades():
    """Faz a busca por todas as Atividades cadastradas

    Retorna uma representação da listagem de atividades.
    """
    logger.debug(f"Coletando atividades ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    # atividades = session.query(Atividade).all()
    atividades = session.query(Atividade).all()

    if not atividades:
        # se não há atividades cadastradas
        return {"atividades": []}, 200
    else:
        logger.debug(f"%d atividades encontradas" % len(atividades))

        # converte o objeto time em uma string antes de retornar a resposta JSON

        atividades_serializadas = [atividade.serializar()
                                   for atividade in atividades]
        # print(atividades_serializadas)
        return apresenta_atividades(atividades_serializadas), 200


@app.get('/atividade', tags=[atividade_tag],
         responses={"200": AtividadeViewSchema, "404": ErrorSchema})
def get_atividade(query: AtividadeBuscaIdSchema):
    """Faz a busca por uma Atividade a partir do id da atividade

    Retorna uma representação das atividades e observações associadas.
    """
    atividade_id = query.id
    logger.debug(f"Coletando dados sobre atividade #{atividade_id}")

    # criando conexão com a base
    session = Session()

    # fazendo a busca
    atividade = session.query(Atividade).filter(
        Atividade.id == atividade_id).first()

    if not atividade:
        # se a atividade não foi encontrada
        error_msg = "Atividade não encontrada na base :/"
        logger.warning(
            f"Erro ao buscar atividade '{atividade_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Atividade encontrada: '{atividade.data}'")
        # retorna a representação de produto
        return apresenta_atividade(atividade, 'Atividade Encontrada com sucesso!'), 200


@app.put('/atividade', tags=[atividade_tag], responses={"200": AtividadeViewSchema, "404": ErrorSchema})
def update_atividade(form: UpdateAtividadeSchema):
    """Atualiza os dados de uma atividade existente.

    Retorna uma representação atualizada da atividade.
    """
    atividade_id = getattr(
        form, "id")  # Acesso ao atributo 'id' do objeto 'form'
    logger.debug(f"Atualizando dados da atividade #{atividade_id}")

    # Criando conexão com a base
    session = Session()

    # Fazendo a busca pela atividade
    atividade = session.query(Atividade).get(atividade_id)

    if not atividade:
        # Se a atividade não foi encontrada
        error_msg = "Atividade não encontrada na base :/"
        logger.warning(
            f"Erro ao atualizar atividade #{atividade_id}: {error_msg}")
        return {"message": error_msg}, 404

    # Atualize os dados da atividade com base nos valores recebidos no formulário
    atividade.data = getattr(form, "data")
    atividade.start_time = getattr(form, "start_time")
    atividade.end_time = getattr(form, "end_time")
    atividade.duracao = getattr(form, "duracao")
    atividade.publicacoes = getattr(form, "publicacoes")
    atividade.videos = getattr(form, "videos")
    atividade.revisitas = getattr(form, "revisitas")
    atividade.estudos = getattr(form, "estudos")
    atividade.latitude = getattr(form, "latitude")
    atividade.longitude = getattr(form, "longitude")
    atividade.endereco = getattr(form, "endereco")

    try:
        # Efetue o commit das alterações no banco de dados
        session.commit()
        logger.debug(f"Atividade atualizada: {atividade_id}")
        return apresenta_atividade(atividade, "Atividade atualizada com sucesso!"), 200

    except Exception as e:
        # Caso ocorra um erro não previsto
        error_msg = "Não foi possível atualizar a atividade :/"
        logger.warning(
            f"Erro ao atualizar atividade #{atividade_id}: {error_msg}")
        return {"message": error_msg}, 400


@app.delete('/atividade', tags=[atividade_tag], responses={"200": AtividadeDelSchema, "404": ErrorSchema})
def del_atividade(query: AtividadeBuscaIdSchema):
    """Deleta uma Atividade a partir data da atividade informada

    Retorna uma mensagem de confirmação da remoção.
    """
    atividade_id = query.id
    print(atividade_id)
    logger.debug(f"Deletando dados sobre atividade #{atividade_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    atividade = session.query(Atividade).filter(
        Atividade.id == atividade_id).first()
    if atividade:
        session.delete(atividade)
        session.commit()
        # retorna a representação da mensagem de confirmação
        logger.debug(
            f"Deletado atividade #{atividade_id} e todas as suas observações.")
        return {"message": "Atividade e suas observações foram removidas", "data": atividade_id}
    else:
        # se a atividade não foi encontrada
        error_msg = "Atividade não encontrada na base :/"
        logger.warning(
            f"Erro ao deletar atividade #'{atividade_id}', {error_msg}")
        return {"message": error_msg}, 404


@app.post('/observacao', tags=[observacao_tag],
          responses={"200": AtividadeViewSchema, "404": ErrorSchema})
def add_observacao(form: ObservacaoSchema):
    """Adiciona uma nova observação à uma atividade cadastrada na base identificada pelo id

    Retorna uma representação das atividades e observações associados.
    """
    atividade_id = form.atividade_id
    logger.debug(f"Adicionando observações a atividade #{atividade_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pela atividade
    atividade = session.query(Atividade).filter(
        Atividade.id == atividade_id).first()

    if not atividade:
        # se atividade não encontrada
        error_msg = "Atividade não encontrada na base :/"
        logger.warning(
            f"Erro ao adicionar observação a atividade '{atividade_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando uma observação
    texto = form.texto
    observacao = Observacao(texto)

    # adicionando uma observação a atividade
    atividade.adiciona_observacao(observacao)
    session.commit()

    logger.debug(f"Adicionado observação a atividade #{atividade_id}")

    # retorna a representação da atividade
    return apresenta_atividade(atividade, 'Observação adicionada com sucesso!'), 200
