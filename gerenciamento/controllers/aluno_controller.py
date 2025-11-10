from flask import request, jsonify
from datetime import datetime
from models.aluno import Aluno, db

class AlunoController:

    @staticmethod
    def _get_data():
        data = request.get_json()
        if not data:
            return None, jsonify({"error": "Dados inválidos"}), 400
        return data, None, None

    @staticmethod
    def get_alunos():
        if request.method != 'GET':
            return jsonify({"error": "Método não permitido"}), 405
        alunos = Aluno.query.all()
        return jsonify([aluno.to_dict() for aluno in alunos]), 200

    @staticmethod
    def get_aluno_by_id(aluno_id):
        if request.method != 'GET':
            return jsonify({"error": "Método não permitido"}), 405
        aluno = Aluno.query.get(aluno_id)
        if not aluno:
            return jsonify({"error": "Aluno não encontrado"}), 404
        return jsonify(aluno.to_dict()), 200

    @staticmethod
    def create_aluno():
        if request.method != 'POST':
            return jsonify({"error": "Método não permitido"}), 405

        data, error_response, status = AlunoController._get_data()
        if error_response:
            return error_response, status

        obrigatorios = ["nome", "idade", "data_nascimento", "turma_id"]
        for campo in obrigatorios:
            if campo not in data:
                return jsonify({"error": f"Campo obrigatório {campo} ausente"}), 400

        novo_aluno = Aluno(
            nome=data["nome"],
            idade=data["idade"],
            data_nascimento=datetime.strptime(data["data_nascimento"], "%Y-%m-%d").date(),
            turma_id=data["turma_id"],
            nota_primeiro_semestre=data.get("nota_primeiro_semestre"),
            nota_segundo_semestre=data.get("nota_segundo_semestre"),
            media_final=data.get("media_final")
        )

        db.session.add(novo_aluno)
        db.session.commit()
        return jsonify(novo_aluno.to_dict()), 201

    @staticmethod
    def update_aluno(aluno_id):
        if request.method != 'PUT':
            return jsonify({"error": "Método não permitido"}), 405

        aluno = Aluno.query.get(aluno_id)
        if not aluno:
            return jsonify({"error": "Aluno não encontrado"}), 404

        data, error_response, status = AlunoController._get_data()
        if error_response:
            return error_response, status

        campos = [
            "nome", "idade", "data_nascimento",
            "turma_id", "nota_primeiro_semestre",
            "nota_segundo_semestre", "media_final"
        ]
        for campo in campos:
            if campo in data:
                if campo == "data_nascimento" and data[campo]:
                    setattr(aluno, campo, datetime.strptime(data[campo], "%Y-%m-%d").date())
                else:
                    setattr(aluno, campo, data[campo])

        db.session.commit()
        return jsonify(aluno.to_dict()), 200

    @staticmethod
    def delete_aluno(aluno_id):
        if request.method != 'DELETE':
            return jsonify({"error": "Método não permitido"}), 405

        aluno = Aluno.query.get(aluno_id)
        if not aluno:
            return jsonify({"error": "Aluno não encontrado"}), 404

        db.session.delete(aluno)
        db.session.commit()
        return jsonify({"message": "Aluno deletado com sucesso"}), 200
