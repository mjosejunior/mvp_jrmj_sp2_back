![MVP PUC-Rio - José Rodrigues Matos Junior](./img/banner_repo.png)
#
&nbsp;
&nbsp;

***MVP PUC-Rio-JRMJ SP2 - Backend***

🚀 Bem-vindo ao repositório do backend do sistema de controle de atividades de serviço de campo! Este projeto é o marco de conclusão da Sprint 2 do Curso de Desenvolvimento Full Stack na PUC-Rio.

# Sobre o MVP
Desenvolvemos esta aplicação para auxiliar o "Publicador de Boas Novas" a registrar suas atividades diárias de trabalho. Utilizando a  [OpenStreetMap (OSM) Nominatim API](https://nominatim.org/release-docs/develop/api/Overview/) é possível obter nomes de lugares e detalhes com base nas coordenadas do local. 

## Tecnologias Utilizadas
- ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=Python&logoColor=white)
- ![Flask](https://img.shields.io/badge/-Flask-000000?style=flat-square&logo=Flask&logoColor=white)
- ![OpenAPI](https://img.shields.io/badge/-OpenAPI-6BA539?style=flat-square&logo=OpenAPI-Initiative&logoColor=white)
- ![SQLite](https://img.shields.io/badge/-SQLite-003B57?style=flat-square&logo=SQLite&logoColor=white)
- ![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-8C2D19?style=flat-square&logo=SQLAlchemy&logoColor=white)
- ![HTML5](https://img.shields.io/badge/-HTML5-E34F26?style=flat-square&logo=HTML5&logoColor=white)
- ![CSS3](https://img.shields.io/badge/-CSS3-1572B6?style=flat-square&logo=CSS3&logoColor=white)
- ![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat-square&logo=JavaScript&logoColor=black)
- ![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=Docker&logoColor=white)
- ![Nginx](https://img.shields.io/badge/-Nginx-269539?style=flat-square&logo=Nginx&logoColor=white)


## Como executar?

- > 🎬 [Vídeo de Visão Geral do Projeto](https://youtu.be/elgTpzwykfo)

A aplicação está dividida em 2 repositórios, sendo:

- Back-end (Este repositório)

- > [Front-end] https://github.com/mjosejunior/mvp_jrmj_sp1_front


### Instalação e Execução Local

#### Pré-requisitos
* Python e suas libs listadas em `requirements.txt`.
* **Recomendado**: Utilize ambientes virtuais, como `virtualenv`.

### Passo a Passo

1. Clone o repositório.
2. Navegue até o diretório raiz do projeto através do terminal.
3. Configure e ative seu ambiente virtual (caso esteja usando um).
4. Instale as dependências/bibliotecas:
```bash
(env)$ pip install -r requirements.txt
```

1. Execute o servidor:
```bash
(env)$ flask run --host 0.0.0.0 --port 5001
```
**Dica**: Em modo de desenvolvimento, utilize o parâmetro `--reload` para reiniciar o servidor automaticamente após alterações:

```bash
(env)$ flask run --host 0.0.0.0 --port 5001 --reload
```
Acesse `http://localhost:5001/#/` em seu navegador para conferir a API em execução.

## Como Executar com Docker

**Para ter uma visão completa e integrada com o backend**:

1. Certifique-se de ter o Docker e o Docker Compose instalados.

2. Clone ambos os repositórios (backend e frontend).

3. No diretório principal, onde o `docker-compose.yml` está localizado, execute: 
```bash
docker-compose up --build.
```
Acesse `http://localhost` para ver o frontend em ação e `http://localhost:5001` para o backend.


Em caso de dificuldades, por favor, entre em contato.