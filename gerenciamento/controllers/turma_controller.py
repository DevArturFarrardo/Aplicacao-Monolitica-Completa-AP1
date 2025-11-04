# controllers/turma_controller.py
from flask import Blueprint, request, jsonify
from extensions import db
from models import Turma

bp = Blueprint('turmas', __name__, url_prefix='/turmas')

@bp.route('/', methods=['GET'])
def get_turmas():
    turmas = Turma.query.all()
    return jsonify([t.to_dict() for t in turmas]), 200

@bp.route('/<int:id>', methods=['GET'])
def get_turma(id):
    turma = Turma.query.get_or_404(id)
    return jsonify(turma.to_dict()), 200

@bp.route('/', methods=['POST'])
def create_turma():
    data = request.get_json() or {}

    turma = Turma(
        descricao=data.get('descricao'),
        professor_id=data.get('professor_id'),
        ativo=data.get('ativo', True)
    )
    db.session.add(turma)
    db.session.commit()
    return jsonify(turma.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
def update_turma(id):
    turma = Turma.query.get_or_404(id)
    data = request.get_json() or {}

    turma.descricao = data.get('descricao', turma.descricao)
    turma.professor_id = data.get('professor_id', turma.professor_id)
    turma.ativo = data.get('ativo', turma.ativo)

    db.session.commit()
    return jsonify(turma.to_dict()), 200

@bp.route('/<int:id>', methods=['DELETE'])
def delete_turma(id):
    turma = Turma.query.get_or_404(id)
    db.session.delete(turma)
    db.session.commit()
    return '', 204