from flask import request, jsonify
from models.turma import Turma, db

class TurmaController:

    @staticmethod
    def _get_json():
        data = request.get_json()
        if not data:
            return None, jsonify({"error": "Dados inválidos"}), 400
        return data, None, None

    @staticmethod
    def get_turmas():
        if request.method != 'GET':
            return jsonify({"error": "Método não permitido"}), 405

        turmas = Turma.query.all()
        return jsonify([turma.to_dict() for turma in turmas]), 200

    @staticmethod
    def get_turma_by_id(turma_id):
        if request.method != 'GET':
            return jsonify({"error": "Método não permitido"}), 405

        turma = Turma.query.get(turma_id)
        if not turma:
            return jsonify({"error": "Turma não encontrada"}), 404
        return jsonify(turma.to_dict()), 200

    @staticmethod
    def create_turma():
        if request.method != 'POST':
            return jsonify({"error": "Método não permitido"}), 405

        data, error_response, status = TurmaController._get_json()
        if error_response:
            return error_response, status

        if "descricao" not in data or "professor_id" not in data:
            return jsonify({"error": "Campos obrigatórios ausentes"}), 400

        nova_turma = Turma(
            descricao=data["descricao"],
            professor_id=data["professor_id"],
            ativo=data.get("ativo", True)
        )
        db.session.add(nova_turma)
        db.session.commit()
        return jsonify(nova_turma.to_dict()), 201

    @staticmethod
    def update_turma(turma_id):
        if request.method != 'PUT':
            return jsonify({"error": "Método não permitido"}), 405

        turma = Turma.query.get(turma_id)
        if not turma:
            return jsonify({"error": "Turma não encontrada"}), 404

        data, error_response, status = TurmaController._get_json()
        if error_response:
            return error_response, status

        turma.descricao = data.get("descricao", turma.descricao)
        turma.professor_id = data.get("professor_id", turma.professor_id)
        turma.ativo = data.get("ativo", turma.ativo)

        db.session.commit()
        return jsonify(turma.to_dict()), 200

    @staticmethod
    def delete_turma(turma_id):
        if request.method != 'DELETE':
            return jsonify({"error": "Método não permitido"}), 405

        turma = Turma.query.get(turma_id)
        if not turma:
            return jsonify({"error": "Turma não encontrada"}), 404

        db.session.delete(turma)
        db.session.commit()
        return jsonify({"message": "Turma deletada com sucesso"}), 200
