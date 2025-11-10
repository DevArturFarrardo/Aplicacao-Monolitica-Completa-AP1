from flask import request, jsonify
from models.agendamentos import Agendamento, db
from datetime import datetime

class AgendamentoController:

    @staticmethod
    def _get_json():
        data = request.get_json()
        if not data:
            return None, jsonify({"erro": "Dados inválidos"}), 400
        return data, None, None

    @staticmethod
    def get_agendamentos():
        if request.method != 'GET':
            return jsonify({"erro": "Método não permitido"}), 405

        agendamentos = Agendamento.query.all()
        return jsonify([agendamento.to_dict() for agendamento in agendamentos]), 200

    @staticmethod
    def get_agendamento_by_id(agendamento_id):
        if request.method != 'GET':
            return jsonify({"erro": "Método não permitido"}), 405

        agendamento = Agendamento.query.get(agendamento_id)
        if not agendamento:
            return jsonify({"erro": "Agendamento não encontrado"}), 404
        return jsonify(agendamento.to_dict()), 200

    @staticmethod
    def create_agendamento():
        if request.method != 'POST':
            return jsonify({"erro": "Método não permitido"}), 405

        data, error_response, status = AgendamentoController._get_json()
        if error_response:
            return error_response, status

        if "num_sala" not in data or "lab" not in data or "data" not in data or "turma_id" not in data:
            return jsonify({"erro": "Campos obrigatórios ausentes"}), 400

        try:
            data_agendamento = datetime.fromisoformat(data["data"]).date()
        except ValueError:
            return jsonify({"erro": "Data inválida, use o formato YYYY-MM-DD"}), 400

        novo_agendamento = Agendamento(
            num_sala=data["num_sala"],
            lab=bool(data["lab"]),
            data=data_agendamento,
            turma_id=data["turma_id"],
            hora_inicio=data.get("hora_inicio"),
            hora_fim=data.get("hora_fim")
        )

        db.session.add(novo_agendamento)
        db.session.commit()
        return jsonify(novo_agendamento.to_dict()), 201

    @staticmethod
    def update_agendamento(agendamento_id):
        if request.method != 'PUT':
            return jsonify({"erro": "Método não permitido"}), 405

        agendamento = Agendamento.query.get(agendamento_id)
        if not agendamento:
            return jsonify({"erro": "Agendamento não encontrado"}), 404

        data, error_response, status = AgendamentoController._get_json()
        if error_response:
            return error_response, status

        campos = ["data", "turma_id", "num_sala", "lab", "hora_inicio", "hora_fim"]

        for campo in campos:
            if campo in data:
                if campo == "data" and data[campo]:
                    try:
                        setattr(agendamento, campo, datetime.strptime(data[campo], "%Y-%m-%d").date())
                    except ValueError:
                        return jsonify({"erro": "Formato de data inválido. Use AAAA-MM-DD."}), 400
                else:
                    setattr(agendamento, campo, data[campo])

        db.session.commit()
        return jsonify(agendamento.to_dict()), 200

    @staticmethod
    def delete_agendamento(agendamento_id):
        if request.method != 'DELETE':
            return jsonify({"erro": "Método não permitido"}), 405

        agendamento = Agendamento.query.get(agendamento_id)
        if not agendamento:
            return jsonify({"erro": "Agendamento não encontrado"}), 404

        db.session.delete(agendamento)
        db.session.commit()
        return jsonify({"mensagem": "Agendamento removido com sucesso"}), 200