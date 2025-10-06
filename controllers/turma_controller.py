# controllers/turma_controller.py
from flask import Blueprint, request, jsonify
from app import db
from models import Turma

bp = Blueprint('turmas', __name__, url_prefix='/turmas')

@bp.route('/', methods=['GET'])
def get_turmas():
    """
    Listar todas as turmas
    ---
    tags:
      - Turmas
    responses:
      200:
        description: Lista de turmas
    """
    turmas = Turma.query.all()
    return jsonify([t.to_dict() for t in turmas]), 200

@bp.route('/<int:id>', methods=['GET'])
def get_turma(id):
    """
    Buscar turma por ID
    ---
    tags:
      - Turmas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Turma encontrada
    """
    turma = Turma.query.get_or_404(id)
    return jsonify(turma.to_dict()), 200

@bp.route('/', methods=['POST'])
def create_turma():
    """
    Criar nova turma
    ---
    tags:
      - Turmas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            descricao:
              type: string
            professor_id:
              type: integer
            ativo:
              type: boolean
    responses:
      201:
        description: Turma criada
    """
    data = request.get_json()
    turma = Turma(
        descricao=data['descricao'],
        professor_id=data['professor_id'],
        ativo=data.get('ativo', True)
    )
    db.session.add(turma)
    db.session.commit()
    return jsonify(turma.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
def update_turma(id):
    """
    Atualizar turma
    ---
    tags:
      - Turmas
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
            descricao:
              type: string
            professor_id:
              type: integer
            ativo:
              type: boolean
    responses:
      200:
        description: Turma atualizada
    """
    turma = Turma.query.get_or_404(id)
    data = request.get_json()
    
    turma.descricao = data.get('descricao', turma.descricao)
    turma.professor_id = data.get('professor_id', turma.professor_id)
    turma.ativo = data.get('ativo', turma.ativo)
    
    db.session.commit()
    return jsonify(turma.to_dict()), 200

@bp.route('/<int:id>', methods=['DELETE'])
def delete_turma(id):
    """
    Deletar turma
    ---
    tags:
      - Turmas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Turma deletada
    """
    turma = Turma.query.get_or_404(id)
    db.session.delete(turma)
    db.session.commit()
    return '', 204