from flask import Flask
from flasgger import Swagger
from models import db
from models.agendamentos import Agendamento
from config import Config
from controllers.agendamentos_controller import AgendamentoController

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "API Escolar - Agendamentos de Salas",
        "description": "Microsserviço para gerenciamento de agendamentos de salas e laboratórios.",
        "version": "2.0.0"
    },
    "basePath": "/",
    "schemes": ["http"]
})

@app.route("/agendamentos", methods=["GET"])
def get_agendamentos():
    """Listar todos os agendamentos
    ---
    tags: [Agendamentos]
    responses:
      200:
        description: Lista de agendamentos disponíveis
    """
    return AgendamentoController.get_agendamentos()


@app.route("/agendamentos/<int:agendamento_id>", methods=["GET"])
def get_agendamento_by_id(agendamento_id):
    """Buscar agendamento por ID
    ---
    tags: [Agendamentos]
    parameters:
      - name: agendamento_id
        in: path
        type: integer
        required: true
    responses:
      200: {description: Agendamento encontrado}
      404: {description: Agendamento não encontrado}
    """
    return AgendamentoController.get_agendamento_by_id(agendamento_id)


@app.route("/agendamentos", methods=["POST"])
def create_agendamento():
    """Criar novo agendamento
    ---
    tags: [Agendamentos]
    consumes: [application/json]
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            num_sala: {type: integer}
            lab: {type: boolean}
            data: {type: string, format: date}
            turma_id: {type: integer}
            hora_inicio: {type: string, example: "08:00"}
            hora_fim: {type: string, example: "10:00"}
    responses:
      201: {description: Agendamento criado com sucesso}
      400: {description: Dados inválidos}
    """
    return AgendamentoController.create_agendamento()


@app.route("/agendamentos/<int:agendamento_id>", methods=["PUT"])
def update_agendamento(agendamento_id):
    """Atualizar um agendamento existente
    ---
    tags: [Agendamentos]
    parameters:
      - name: agendamento_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            num_sala: {type: integer}
            lab: {type: boolean}
            data: {type: string, format: date}
            turma_id: {type: integer}
            hora_inicio: {type: string, example: "09:00"}
            hora_fim: {type: string, example: "11:00"}
    responses:
      200: {description: Agendamento atualizado}
      404: {description: Agendamento não encontrado}
    """
    return AgendamentoController.update_agendamento(agendamento_id)


@app.route("/agendamentos/<int:agendamento_id>", methods=["DELETE"])
def delete_agendamento(agendamento_id):
    """Excluir um agendamento
    ---
    tags: [Agendamentos]
    parameters:
      - name: agendamento_id
        in: path
        type: integer
        required: true
    responses:
      200: {description: Agendamento removido com sucesso}
      404: {description: Agendamento não encontrado}
    """
    return AgendamentoController.delete_agendamento(agendamento_id)


def init_db():
    with app.app_context():
        db.create_all()
        print("✅ Base de dados do módulo Agendamentos pronta para uso!")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5051, debug=True)