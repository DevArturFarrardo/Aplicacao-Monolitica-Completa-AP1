from flask import Flask
from flasgger import Swagger
from models import db
from models.tarefas import Tarefa
from models.avaliacoes import Avaliacao
from config import Config
from controllers.tarefas_controller import TarefaController
from controllers.avaliacoes_controller import AvaliacaoController

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "API Escolar - Tarefas e Avaliações",
        "description": "Microsserviço responsável pelo gerenciamento de tarefas escolares e avaliações dos alunos.",
        "version": "2.0.0"
    },
    "basePath": "/",
    "schemes": ["http"]
})


@app.route("/tarefas", methods=["GET"])
def get_tarefas():
    """Listar todas as tarefas
    ---
    tags: [Tarefas]
    responses:
      200:
        description: Lista de tarefas cadastradas no sistema
    """
    return TarefaController.get_tarefas()

@app.route("/tarefas/<int:tarefa_id>", methods=["GET"])
def get_tarefa_by_id(tarefa_id):
    """Buscar tarefa por ID
    ---
    tags: [Tarefas]
    parameters:
      - name: tarefa_id
        in: path
        type: integer
        required: true
    responses:
      200: {description: Tarefa encontrada}
      404: {description: Tarefa não encontrada}
    """
    return TarefaController.get_tarefa_by_id(tarefa_id)

@app.route("/tarefas", methods=["POST"])
def create_tarefa():
    """Criar nova tarefa
    ---
    tags: [Tarefas]
    consumes: [application/json]
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            nome_tarefa: {type: string}
            descricao: {type: string}
            peso_porcento: {type: integer}
            data_entrega: {type: string, format: date}
            turma_id: {type: integer}
            professor_id: {type: integer}
    responses:
      201: {description: Tarefa criada com sucesso}
      400: {description: Dados inválidos ou campos ausentes}
    """
    return TarefaController.create_tarefa()

@app.route("/tarefas/<int:tarefa_id>", methods=["PUT"])
def update_tarefa(tarefa_id):
    """Atualizar tarefa existente
    ---
    tags: [Tarefas]
    parameters:
      - name: tarefa_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            nome_tarefa: {type: string}
            descricao: {type: string}
            peso_porcento: {type: integer}
            data_entrega: {type: string, format: date}
            turma_id: {type: integer}
            professor_id: {type: integer}
    responses:
      200: {description: Tarefa atualizada com sucesso}
      404: {description: Tarefa não encontrada}
    """
    return TarefaController.update_tarefa(tarefa_id)

@app.route("/tarefas/<int:tarefa_id>", methods=["DELETE"])
def delete_tarefa(tarefa_id):
    """Excluir tarefa
    ---
    tags: [Tarefas]
    parameters:
      - name: tarefa_id
        in: path
        type: integer
        required: true
    responses:
      200: {description: Tarefa removida com sucesso}
      404: {description: Tarefa não encontrada}
    """
    return TarefaController.delete_tarefa(tarefa_id)

@app.route("/avaliacoes", methods=["GET"])
def get_avaliacoes():
    """Listar todas as avaliações
    ---
    tags: [Avaliações]
    responses:
      200:
        description: Lista de avaliações cadastradas
    """
    return AvaliacaoController.get_avaliacoes()

@app.route("/avaliacoes/<int:avaliacao_id>", methods=["GET"])
def get_avaliacao_by_id(avaliacao_id):
    """Buscar avaliação por ID
    ---
    tags: [Avaliações]
    parameters:
      - name: avaliacao_id
        in: path
        type: integer
        required: true
    responses:
      200: {description: Avaliação encontrada}
      404: {description: Avaliação não encontrada}
    """
    return AvaliacaoController.get_avaliacao_by_id(avaliacao_id)

@app.route("/avaliacoes", methods=["POST"])
def create_avaliacao():
    """Criar nova avaliação
    ---
    tags: [Avaliações]
    consumes: [application/json]
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            nota: {type: number}
            aluno_id: {type: integer}
            tarefa_id: {type: integer}
    responses:
      201: {description: Avaliação criada com sucesso}
      400: {description: Dados inválidos}
    """
    return AvaliacaoController.create_avaliacao()

@app.route("/avaliacoes/<int:avaliacao_id>", methods=["PUT"])
def update_avaliacao(avaliacao_id):
    """Atualizar avaliação
    ---
    tags: [Avaliações]
    parameters:
      - name: avaliacao_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
    responses:
      200: {description: Avaliação atualizada}
      404: {description: Avaliação não encontrada}
    """
    return AvaliacaoController.update_avaliacao(avaliacao_id)

@app.route("/avaliacoes/<int:avaliacao_id>", methods=["DELETE"])
def delete_avaliacao(avaliacao_id):
    """Excluir avaliação
    ---
    tags: [Avaliações]
    parameters:
      - name: avaliacao_id
        in: path
        type: integer
        required: true
    responses:
      200: {description: Avaliação removida}
      404: {description: Avaliação não encontrada}
    """
    return AvaliacaoController.delete_avaliacao(avaliacao_id)


def init_db():
    with app.app_context():
        db.create_all()
        print("✅ Base de dados do módulo Tarefas pronta para uso!")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5052, debug=True)