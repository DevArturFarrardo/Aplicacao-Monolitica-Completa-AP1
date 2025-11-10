from flask import request, jsonify
from datetime import datetime
from models.tarefas import Tarefa, db

class TarefaController:

    @staticmethod
    def _get_data():
        data = request.get_json()
        if not data:
            return None, jsonify({"erro": "Dados inválidos"}), 400
        return data, None, None

    @staticmethod
    def get_tarefas():
        if request.method != 'GET':
            return jsonify({"erro": "Método não permitido"}), 405

        tarefas = Tarefa.query.all()
        return jsonify([tarefa.to_dict() for tarefa in tarefas]), 200

    @staticmethod
    def get_tarefa_by_id(tarefa_id):
        if request.method != 'GET':
            return jsonify({"erro": "Método não permitido"}), 405

        tarefa = Tarefa.query.get(tarefa_id)
        if not tarefa:
            return jsonify({"erro": "Tarefa não encontrada"}), 404

        return jsonify(tarefa.to_dict()), 200

    @staticmethod
    def create_tarefa():
        if request.method != 'POST':
            return jsonify({"erro": "Método não permitido"}), 405

        data, error_response, status = TarefaController._get_data()
        if error_response:
            return error_response, status

        obrigatorios = ["nome_tarefa", "peso_porcento", "data_entrega", "turma_id", "professor_id"]
        for campo in obrigatorios:
            if campo not in data:
                return jsonify({"erro": f"Campo obrigatório '{campo}' ausente"}), 400

        try:
            nova_tarefa = Tarefa(
                nome_tarefa=data["nome_tarefa"],
                descricao=data.get("descricao"),
                peso_porcento=data["peso_porcento"],
                data_entrega=datetime.strptime(data["data_entrega"], "%Y-%m-%d").date(),
                turma_id=data["turma_id"],
                professor_id=data["professor_id"]
            )
            db.session.add(nova_tarefa)
            db.session.commit()
            return jsonify(nova_tarefa.to_dict()), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"erro": f"Erro ao criar tarefa: {str(e)}"}), 500

    @staticmethod
    def update_tarefa(tarefa_id):
        if request.method != 'PUT':
            return jsonify({"erro": "Método não permitido"}), 405

        tarefa = Tarefa.query.get(tarefa_id)
        if not tarefa:
            return jsonify({"erro": "Tarefa não encontrada"}), 404

        data, error_response, status = TarefaController._get_data()
        if error_response:
            return error_response, status

        campos = ["nome_tarefa", "descricao", "peso_porcento", "data_entrega", "turma_id", "professor_id"]
        for campo in campos:
            if campo in data:
                if campo == "data_entrega" and data[campo]:
                    setattr(tarefa, campo, datetime.strptime(data[campo], "%Y-%m-%d").date())
                else:
                    setattr(tarefa, campo, data[campo])

        try:
            db.session.commit()
            return jsonify(tarefa.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"erro": f"Erro ao atualizar tarefa: {str(e)}"}), 500

    @staticmethod
    def delete_tarefa(tarefa_id):
        if request.method != 'DELETE':
            return jsonify({"erro": "Método não permitido"}), 405

        tarefa = Tarefa.query.get(tarefa_id)
        if not tarefa:
            return jsonify({"erro": "Tarefa não encontrada"}), 404

        try:
            db.session.delete(tarefa)
            db.session.commit()
            return jsonify({"mensagem": "Tarefa removida com sucesso"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"erro": f"Erro ao deletar tarefa: {str(e)}"}), 500