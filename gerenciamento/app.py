from flask import Flask
from flasgger import Swagger
from models import db
from models.aluno import Aluno
from models.turma import Turma
from models.professor import Professor
from config import Config
from controllers.aluno_controller import AlunoController
from controllers.turma_controller import TurmaController
from controllers.professor_controller import ProfessorController

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "API de gerenciamento escolar",
        "description": "API que realiza o gerenciamento de alunos, turmas e professores.",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http"]
})

@app.route("/alunos", methods=["GET"])
def get_alunos():
    """Listar todos os alunos
    ---
    tags: [Alunos]
    responses:
      200:
        description: Lista de alunos
    """
    return AlunoController.get_alunos()

@app.route("/alunos/<int:aluno_id>", methods=["GET"])
def get_aluno_by_id(aluno_id):
    """Buscar aluno por ID
    ---
    tags: [Alunos]
    parameters:
      - name: aluno_id
        in: path
        type: integer
        required: true
    responses:
      200: {description: Aluno encontrado}
      404: {description: Aluno nÃ£o encontrado}
    """
    return AlunoController.get_aluno_by_id(aluno_id)

@app.route("/alunos", methods=["POST"])
def create_aluno():
    """Criar novo aluno
    ---
    tags: [Alunos]
    consumes: [application/json]
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            nome: {type: string}
            idade: {type: integer}
            data_nascimento: {type: string, format: date}
            turma_id: {type: integer}
            nota_primeiro_semestre: {type: number, format: float}
            nota_segundo_semestre: {type: number, format: float}
            media_final: {type: number, format: float}
    responses:
      201: {description: Aluno criado com sucesso}
    """
    return AlunoController.create_aluno()

@app.route("/alunos/<int:aluno_id>", methods=["PUT"])
def update_aluno(aluno_id):
    """Atualizar aluno
    ---
    tags: [Alunos]
    parameters:
      - name: aluno_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
    responses:
      200: {description: Aluno atualizado}
      404: {description: Aluno nÃ£o encontrado}
    """
    return AlunoController.update_aluno(aluno_id)

@app.route("/alunos/<int:aluno_id>", methods=["DELETE"])
def delete_aluno(aluno_id):
    """Excluir aluno
    ---
    tags: [Alunos]
    parameters:
      - name: aluno_id
        in: path
        type: integer
        required: true
    responses:
      204: {description: Aluno removido}
      404: {description: Aluno nÃ£o encontrado}
    """
    return AlunoController.delete_aluno(aluno_id)

@app.route("/turmas", methods=["GET"])
def get_turmas():
    """Listar todas as turmas
    ---
    tags: [Turmas]
    responses:
      200: {description: Lista de turmas}
    """
    return TurmaController.get_turmas()

@app.route("/turmas/<int:turma_id>", methods=["GET"])
def get_turma_by_id(turma_id):
    """Buscar turma por ID
    ---
    tags: [Turmas]
    parameters:
      - name: turma_id
        in: path
        type: integer
        required: true
    responses:
      200: {description: Turma encontrada}
      404: {description: Turma nÃ£o encontrada}
    """
    return TurmaController.get_turma_by_id(turma_id)

@app.route("/turmas", methods=["POST"])
def create_turma():
    """Criar nova turma
    ---
    tags: [Turmas]
    consumes: [application/json]
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            descricao: {type: string}
            professor_id: {type: integer}
            ativo: {type: boolean}
    responses:
      201: {description: Turma criada}
    """
    return TurmaController.create_turma()

@app.route("/turmas/<int:turma_id>", methods=["PUT"])
def update_turma(turma_id):
    """Atualizar turma
    ---
    tags: [Turmas]
    parameters:
      - name: turma_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        schema: {type: object}
    responses:
      200: {description: Turma atualizada}
      404: {description: Turma nÃ£o encontrada}
    """
    return TurmaController.update_turma(turma_id)

@app.route("/turmas/<int:turma_id>", methods=["DELETE"])
def delete_turma(turma_id):
    """Excluir turma
    ---
    tags: [Turmas]
    parameters:
      - name: turma_id
        in: path
        type: integer
        required: true
    responses:
      204: {description: Turma deletada}
      404: {description: Turma nÃ£o encontrada}
    """
    return TurmaController.delete_turma(turma_id)

@app.route("/professores", methods=["GET"])
def get_professores():
    """Listar todos os professores
    ---
    tags: [Professores]
    responses:
      200: {description: Lista de professores}
    """
    return ProfessorController.get_professores()

@app.route("/professores/<int:professor_id>", methods=["GET"])
def get_professor_by_id(professor_id):
    """Buscar professor por ID
    ---
    tags: [Professores]
    parameters:
      - name: professor_id
        in: path
        type: integer
        required: true
    responses:
      200: {description: Professor encontrado}
      404: {description: Professor nÃ£o encontrado}
    """
    return ProfessorController.get_professor_by_id(professor_id)

@app.route("/professores", methods=["POST"])
def create_professor():
    """Criar novo professor
    ---
    tags: [Professores]
    consumes: [application/json]
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            nome: {type: string}
            idade: {type: integer}
            materia: {type: string}
            observacoes: {type: string}
    responses:
      201: {description: Professor criado}
    """
    return ProfessorController.create_professor()

@app.route("/professores/<int:professor_id>", methods=["PUT"])
def update_professor(professor_id):
    """Atualizar professor
    ---
    tags: [Professores]
    parameters:
      - name: professor_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        schema: {type: object}
    responses:
      200: {description: Professor atualizado}
      404: {description: Professor nÃ£o encontrado}
    """
    return ProfessorController.update_professor(professor_id)

@app.route("/professores/<int:professor_id>", methods=["DELETE"])
def delete_professor(professor_id):
    """Excluir professor
    ---
    tags: [Professores]
    parameters:
      - name: professor_id
        in: path
        type: integer
        required: true
    responses:
      204: {description: Professor deletado}
      404: {description: Professor nÃ£o encontrado}
    """
    return ProfessorController.delete_professor(professor_id)

def init_db():
    with app.app_context():
        db.create_all()
        print("Banco de dados inicializado!")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5050, debug=True)
