from app import db
from datetime import datetime

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_sala = db.Column(db.String(50), nullable=False)
    lab = db.Column(db.String(50))
    data = db.Column(db.String(50), nullable=False)  # ou DateTime conforme preferir
    turma_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "num_sala": self.num_sala,
            "lab": self.lab,
            "data": self.data,
            "turma_id": self.turma_id
        }