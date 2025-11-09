from flask import Blueprint, request, jsonify
from extensions import db            
from models import Professor

bp = Blueprint('professores', __name__, url_prefix='/professores')

@bp.route('/', methods=['GET'])
def get_professores():
    """
    Listar todos os professores
    ---
    tags:
      - Professores
    responses:
      200:
        description: Lista de professores
    """
    professores = Professor.query.all()
    return jsonify([p.to_dict() for p in professores]), 200

@bp.route('/<int:id>', methods=['GET'])
def get_professor(id):
    """
    Buscar professor por ID
    ---
    tags:
      - Professores
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Professor encontrado
      404:
        description: Professor não encontrado
    """
    professor = Professor.query.get_or_404(id)
    return jsonify(professor.to_dict()), 200

@bp.route('/', methods=['POST'])
def create_professor():
    """
    Criar novo professor
    ---
    tags:
      - Professores
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            idade:
              type: integer
            materia:
              type: string
            observacoes:
              type: string
    responses:
      201:
        description: Professor criado
    """
    data = request.get_json() or {}

    professor = Professor(
        nome=data.get('nome'),
        idade=data.get('idade'),
        materia=data.get('materia'),
        observacoes=data.get('observacoes', '')
    )
    db.session.add(professor)
    db.session.commit()
    return jsonify(professor.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
def update_professor(id):
    """
    Atualizar professor
    ---
    tags:
      - Professores
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            idade:
              type: integer
            materia:
              type: string
            observacoes:
              type: string
    responses:
      200:
        description: Professor atualizado
    """
    professor = Professor.query.get_or_404(id)
    data = request.get_json() or {}

    professor.nome = data.get('nome', professor.nome)
    professor.idade = data.get('idade', professor.idade)
    professor.materia = data.get('materia', professor.materia)
    professor.observacoes = data.get('observacoes', professor.observacoes)

    db.session.commit()
    return jsonify(professor.to_dict()), 200

@bp.route('/<int:id>', methods=['DELETE'])
def delete_professor(id):
    """
    Deletar professor
    ---
    tags:
      - Professores
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Professor deletado
    """
    professor = Professor.query.get_or_404(id)
    db.session.delete(professor)
    db.session.commit()
    return '', 204