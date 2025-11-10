from flask import request, jsonify
from models.avaliacoes import Avaliacao, db

class AvaliacaoController:

    @staticmethod
    def _get_data():
        data = request.get_json()
        if not data:
            return None, jsonify({"erro": "Dados inválidos"}), 400
        return data, None, None

    @staticmethod
    def get_avaliacoes():
        avaliacoes = Avaliacao.query.all()
        return jsonify([a.to_dict() for a in avaliacoes]), 200

    @staticmethod
    def get_avaliacao_by_id(avaliacao_id):
        avaliacao = Avaliacao.query.get(avaliacao_id)
        if not avaliacao:
            return jsonify({"erro": "Avaliação não encontrada"}), 404
        return jsonify(avaliacao.to_dict()), 200

    @staticmethod
    def create_avaliacao():
        data, error_response, status = AvaliacaoController._get_data()
        if error_response:
            return error_response, status

        obrigatorios = ["nota", "aluno_id", "tarefa_id"]
        for campo in obrigatorios:
            if campo not in data:
                return jsonify({"erro": f"Campo obrigatório '{campo}' ausente"}), 400

        try:
            nova_avaliacao = Avaliacao(
                nota=data["nota"],
                aluno_id=data["aluno_id"],
                tarefa_id=data["tarefa_id"]
            )
            db.session.add(nova_avaliacao)
            db.session.commit()
            return jsonify(nova_avaliacao.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"erro": f"Erro ao criar avaliação: {str(e)}"}), 500

    @staticmethod
    def update_avaliacao(avaliacao_id):
        avaliacao = Avaliacao.query.get(avaliacao_id)
        if not avaliacao:
            return jsonify({"erro": "Avaliação não encontrada"}), 404

        data, error_response, status = AvaliacaoController._get_data()
        if error_response:
            return error_response, status

        try:
            if "nota" in data:
                avaliacao.nota = data["nota"]
            if "aluno_id" in data:
                avaliacao.aluno_id = data["aluno_id"]
            if "tarefa_id" in data:
                avaliacao.tarefa_id = data["tarefa_id"]

            db.session.commit()
            return jsonify(avaliacao.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"erro": f"Erro ao atualizar avaliação: {str(e)}"}), 500

    @staticmethod
    def delete_avaliacao(avaliacao_id):
        avaliacao = Avaliacao.query.get(avaliacao_id)
        if not avaliacao:
            return jsonify({"erro": "Avaliação não encontrada"}), 404

        try:
            db.session.delete(avaliacao)
            db.session.commit()
            return jsonify({"mensagem": "Avaliação removida com sucesso"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"erro": f"Erro ao deletar avaliação: {str(e)}"}), 500