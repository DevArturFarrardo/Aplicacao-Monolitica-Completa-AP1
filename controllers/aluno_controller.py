# controllers/aluno_controller.py
from flask import Blueprint, request, jsonify
from app import db
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
    data = request.get_json()
    
    # Calcular média final
    nota1 = data.get('nota_primeiro_semestre', 0)
    nota2 = data.get('nota_segundo_semestre', 0)
    media = (nota1 + nota2) / 2 if nota1 and nota2 else None
    
    aluno = Aluno(
        nome=data['nome'],
        idade=data['idade'],
        turma_id=data['turma_id'],
        data_nascimento=datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date(),
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
    data = request.get_json()
    
    aluno.nome = data.get('nome', aluno.nome)
    aluno.idade = data.get('idade', aluno.idade)
    aluno.turma_id = data.get('turma_id', aluno.turma_id)
    
    if 'data_nascimento' in data:
        aluno.data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
    
    if 'nota_primeiro_semestre' in data:
        aluno.nota_primeiro_semestre = data['nota_primeiro_semestre']
    
    if 'nota_segundo_semestre' in data:
        aluno.nota_segundo_semestre = data['nota_segundo_semestre']
    
    # Recalcular média
    if aluno.nota_primeiro_semestre and aluno.nota_segundo_semestre:
        aluno.media_final = (aluno.nota_primeiro_semestre + aluno.nota_segundo_semestre) / 2
    
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