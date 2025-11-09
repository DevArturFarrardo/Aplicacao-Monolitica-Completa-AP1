from flask import Blueprint, request, jsonify
from extensions import db            
from models import Aluno
from datetime import datetime

bp = Blueprint('alunos', __name__, url_prefix='/alunos')

@bp.route('/', methods=['GET'])
def get_alunos():
    """
    Listar todos os alunos
    ---
    tags:
      - Alunos
    responses:
      200:
        description: Lista de alunos
    """
    alunos = Aluno.query.all()
    return jsonify([a.to_dict() for a in alunos]), 200

@bp.route('/<int:id>', methods=['GET'])
def get_aluno(id):
    """
    Buscar aluno por ID
    ---
    tags:
      - Alunos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Aluno encontrado
    """
    aluno = Aluno.query.get_or_404(id)
    return jsonify(aluno.to_dict()), 200

@bp.route('/', methods=['POST'])
def create_aluno():
    """
    Criar novo aluno
    ---
    tags:
      - Alunos
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
            turma_id:
              type: integer
            data_nascimento:
              type: string
              format: date
            nota_primeiro_semestre:
              type: number
            nota_segundo_semestre:
              type: number
    responses:
      201:
        description: Aluno criado
    """
    data = request.get_json() or {}

    nota1 = data.get('nota_primeiro_semestre')
    nota2 = data.get('nota_segundo_semestre')
    media = None
    if nota1 is not None and nota2 is not None:
        try:
            media = (float(nota1) + float(nota2)) / 2
        except (TypeError, ValueError):
            media = None

    aluno = Aluno(
        nome=data.get('nome'),
        idade=data.get('idade'),
        turma_id=data.get('turma_id'),
        data_nascimento=datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date() if data.get('data_nascimento') else None,
        nota_primeiro_semestre=nota1,
        nota_segundo_semestre=nota2,
        media_final=media
    )
    db.session.add(aluno)
    db.session.commit()
    return jsonify(aluno.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
def update_aluno(id):
    """
    Atualizar aluno
    ---
    tags:
      - Alunos
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
            turma_id:
              type: integer
            data_nascimento:
              type: string
              format: date
            nota_primeiro_semestre:
              type: number
            nota_segundo_semestre:
              type: number
    responses:
      200:
        description: Aluno atualizado
    """
    aluno = Aluno.query.get_or_404(id)
    data = request.get_json() or {}

    aluno.nome = data.get('nome', aluno.nome)
    aluno.idade = data.get('idade', aluno.idade)
    aluno.turma_id = data.get('turma_id', aluno.turma_id)

    if 'data_nascimento' in data and data.get('data_nascimento'):
        aluno.data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()

    if 'nota_primeiro_semestre' in data:
        aluno.nota_primeiro_semestre = data.get('nota_primeiro_semestre')

    if 'nota_segundo_semestre' in data:
        aluno.nota_segundo_semestre = data.get('nota_segundo_semestre')

    if aluno.nota_primeiro_semestre is not None and aluno.nota_segundo_semestre is not None:
        try:
            aluno.media_final = (float(aluno.nota_primeiro_semestre) + float(aluno.nota_segundo_semestre)) / 2
        except (TypeError, ValueError):
            aluno.media_final = None

    db.session.commit()
    return jsonify(aluno.to_dict()), 200

@bp.route('/<int:id>', methods=['DELETE'])
def delete_aluno(id):
    """
    Deletar aluno
    ---
    tags:
      - Alunos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Aluno deletado
    """
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    return '', 204