from flask import request
from flask_restx import Namespace, Resource, fields
from app import api, db
from models import Atividade, Nota
from services.gerenciamento_client import verificar_turma, verificar_professor, verificar_aluno

ns = Namespace('atividades', description='Atividades e Notas')

atividade_model = ns.model('Atividade', {
    'id': fields.Integer(readonly=True),
    'nome_atividade': fields.String(required=True),
    'descricao': fields.String(),
    'peso_porcento': fields.Float(),
    'data_entrega': fields.String(),
    'turma_id': fields.Integer(required=True),
    'professor_id': fields.Integer(required=True)
})

nota_model = ns.model('Nota', {
    'id': fields.Integer(readonly=True),
    'nota': fields.Float(required=True),
    'aluno_id': fields.Integer(required=True),
    'atividade_id': fields.Integer(required=True)
})

@ns.route('/')
class AtividadesList(Resource):
    @ns.marshal_list_with(atividade_model)
    def get(self):
        return [a.to_dict() for a in Atividade.query.all()]

    @ns.expect(atividade_model, validate=True)
    def post(self):
        data = request.json
        if not verificar_professor(data['professor_id']) or not verificar_turma(data['turma_id']):
            return {"message": "Professor ou Turma inválidos ou serviço de gerenciamento indisponível"}, 400
        a = Atividade(
            nome_atividade=data['nome_atividade'],
            descricao=data.get('descricao'),
            peso_porcento=data.get('peso_porcento'),
            data_entrega=data.get('data_entrega'),
            turma_id=data['turma_id'],
            professor_id=data['professor_id']
        )
        db.session.add(a)
        db.session.commit()
        return a.to_dict(), 201

@ns.route('/<int:id>')
class AtividadeResource(Resource):
    @ns.marshal_with(atividade_model)
    def get(self, id):
        a = Atividade.query.get_or_404(id)
        return a.to_dict()

    @ns.expect(atividade_model)
    def put(self, id):
        a = Atividade.query.get_or_404(id)
        data = request.json
        if not verificar_professor(data['professor_id']) or not verificar_turma(data['turma_id']):
            return {"message": "Professor ou Turma inválidos ou serviço de gerenciamento indisponível"}, 400
        a.nome_atividade = data['nome_atividade']
        a.descricao = data.get('descricao')
        a.peso_porcento = data.get('peso_porcento')
        a.data_entrega = data.get('data_entrega')
        a.turma_id = data['turma_id']
        a.professor_id = data['professor_id']
        db.session.commit()
        return a.to_dict()

    def delete(self, id):
        a = Atividade.query.get_or_404(id)
        db.session.delete(a)
        db.session.commit()
        return {"message": "Deletado"}, 204

# Notas
@ns.route('/notas')
class NotasList(Resource):
    @ns.marshal_list_with(nota_model)
    def get(self):
        return [n.to_dict() for n in Nota.query.all()]

    @ns.expect(nota_model, validate=True)
    def post(self):
        data = request.json
        # valida aluno e atividade
        if not verificar_aluno(data['aluno_id']):
            return {"message": "Aluno inválido ou serviço de gerenciamento indisponível"}, 400
        atividade = Atividade.query.get(data['atividade_id'])
        if not atividade:
            return {"message": "Atividade não encontrada"}, 400
        n = Nota(nota=data['nota'], aluno_id=data['aluno_id'], atividade_id=data['atividade_id'])
        db.session.add(n)
        db.session.commit()
        return n.to_dict(), 201

@ns.route('/notas/<int:id>')
class NotaResource(Resource):
    @ns.marshal_with(nota_model)
    def get(self, id):
        n = Nota.query.get_or_404(id)
        return n.to_dict()

    @ns.expect(nota_model)
    def put(self, id):
        n = Nota.query.get_or_404(id)
        data = request.json
        if not verificar_aluno(data['aluno_id']):
            return {"message": "Aluno inválido"}, 400
        atividade = Atividade.query.get(data['atividade_id'])
        if not atividade:
            return {"message": "Atividade não encontrada"}, 400
        n.nota = data['nota']
        n.aluno_id = data['aluno_id']
        n.atividade_id = data['atividade_id']
        db.session.commit()
        return n.to_dict()

    def delete(self, id):
        n = Nota.query.get_or_404(id)
        db.session.delete(n)
        db.session.commit()
        return {"message": "Deletado"}, 204

api.add_namespace(ns, path='/atividades')