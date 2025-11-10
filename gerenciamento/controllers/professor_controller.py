from flask import request, jsonify
from models.professor import Professor, db

class ProfessorController:

    @staticmethod
    def _get_data():
        data = request.get_json()
        if not data:
            return None, jsonify({"error": "Dados inválidos"}), 400
        return data, None, None

    @staticmethod
    def get_professores():
        if request.method != 'GET':
            return jsonify({"error": "Método não permitido"}), 405

        professores = Professor.query.all()
        return jsonify([prof.to_dict() for prof in professores]), 200

    @staticmethod
    def get_professor_by_id(professor_id):
        if request.method != 'GET':
            return jsonify({"error": "Método não permitido"}), 405

        professor = Professor.query.get(professor_id)
        if not professor:
            return jsonify({"error": "Professor não encontrado"}), 404
        return jsonify(professor.to_dict()), 200

    @staticmethod
    def create_professor():
        if request.method != 'POST':
            return jsonify({"error": "Método não permitido"}), 405

        data, error_response, status = ProfessorController._get_data()
        if error_response:
            return error_response, status

        obrigatorios = ["nome", "idade", "materia"]
        for campo in obrigatorios:
            if campo not in data:
                return jsonify({"error": f"Campo obrigatório {campo} ausente"}), 400

        novo_professor = Professor(
            nome=data["nome"],
            idade=data["idade"],
            materia=data["materia"],
            observacoes=data.get("observacoes")
        )

        db.session.add(novo_professor)
        db.session.commit()
        return jsonify(novo_professor.to_dict()), 201

    @staticmethod
    def update_professor(professor_id):
        if request.method != 'PUT':
            return jsonify({"error": "Método não permitido"}), 405

        professor = Professor.query.get(professor_id)
        if not professor:
            return jsonify({"error": "Professor não encontrado"}), 404

        data, error_response, status = ProfessorController._get_data()
        if error_response:
            return error_response, status

        campos = ["nome", "idade", "materia", "observacoes"]
        for campo in campos:
            if campo in data:
                setattr(professor, campo, data[campo])

        db.session.commit()
        return jsonify(professor.to_dict()), 200

    @staticmethod
    def delete_professor(professor_id):
        if request.method != 'DELETE':
            return jsonify({"error": "Método não permitido"}), 405

        professor = Professor.query.get(professor_id)
        if not professor:
            return jsonify({"error": "Professor não encontrado"}), 404

        db.session.delete(professor)
        db.session.commit()
        return jsonify({"message": "Professor deletado com sucesso"}), 200
