from models import db
from datetime import date

class Tarefa(db.Model):
    __tablename__ = "tarefas"
    
    id = db.Column(db.Integer, primary_key=True)
    nome_tarefa = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    peso_porcento = db.Column(db.Integer, nullable=False)
    data_entrega = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, nullable=False)
    professor_id = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome_tarefa": self.nome_tarefa,
            "descricao": self.descricao,
            "peso_porcento": self.peso_porcento,
            "data_entrega": self.data_entrega.isoformat() if self.data_entrega else None,
            "turma_id": self.turma_id,
            "professor_id": self.professor_id
        }