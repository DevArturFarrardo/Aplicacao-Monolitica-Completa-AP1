from models import db
from datetime import date

class Agendamento(db.Model):
    __tablename__ = "agendamentos"
    
    id = db.Column(db.Integer, primary_key=True)
    num_sala = db.Column(db.Integer, nullable=False)
    lab = db.Column(db.Boolean, default=False)
    data = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, nullable=False)
    hora_inicio = db.Column(db.String(5), nullable=True)
    hora_fim = db.Column(db.String(5), nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "num_sala": self.num_sala,
            "lab": self.lab,
            "data": self.data.isoformat() if self.data else None,
            "turma_id": self.turma_id,
            "hora_inicio": self.hora_inicio,
            "hora_fim": self.hora_fim
        }