from models import db

class Avaliacao(db.Model):
    __tablename__ = "avaliacoes"
    
    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Float, nullable=False)
    aluno_id = db.Column(db.Integer, nullable=False)
    tarefa_id = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "nota": self.nota,
            "aluno_id": self.aluno_id,
            "tarefa_id": self.tarefa_id
        }