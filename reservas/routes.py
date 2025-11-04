from flask import request
from flask_restx import Namespace, Resource, fields
from app import api, app, db
from models import Reserva
from services.gerenciamento_client import verificar_turma

ns = Namespace('reservas', description='Gerenciamento de reservas')

reserva_model = ns.model('Reserva', {
    'id': fields.Integer(readonly=True),
    'num_sala': fields.String(required=True),
    'lab': fields.String(),
    'data': fields.String(required=True),
    'turma_id': fields.Integer(required=True)
})

@ns.route('/')
class ReservaList(Resource):
    @ns.marshal_list_with(reserva_model)
    def get(self):
        return [r.to_dict() for r in Reserva.query.all()]

    @ns.expect(reserva_model, validate=True)
    def post(self):
        data = request.json
        ok, _ = verificar_turma(data['turma_id'])
        if not ok:
            return {"message": "Turma inválida ou serviço de gerenciamento indisponível"}, 400
        r = Reserva(num_sala=data['num_sala'], lab=data.get('lab'), data=data['data'], turma_id=data['turma_id'])
        db.session.add(r)
        db.session.commit()
        return r.to_dict(), 201

@ns.route('/<int:id>')
class ReservaResource(Resource):
    @ns.marshal_with(reserva_model)
    def get(self, id):
        r = Reserva.query.get_or_404(id)
        return r.to_dict()

    @ns.expect(reserva_model)
    def put(self, id):
        r = Reserva.query.get_or_404(id)
        data = request.json
        ok, _ = verificar_turma(data['turma_id'])
        if not ok:
            return {"message": "Turma inválida ou serviço de gerenciamento indisponível"}, 400
        r.num_sala = data['num_sala']
        r.lab = data.get('lab')
        r.data = data['data']
        r.turma_id = data['turma_id']
        db.session.commit()
        return r.to_dict(), 200

    def delete(self, id):
        r = Reserva.query.get_or_404(id)
        db.session.delete(r)
        db.session.commit()
        return {"message": "Deletado"}, 204

api.add_namespace(ns, path='/reservas')