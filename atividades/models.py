from app import db

class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_atividade = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text)
    peso_porcento = db.Column(db.Float)
    data_entrega = db.Column(db.String(50))
    turma_id = db.Column(db.Integer, nullable=False)
    professor_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome_atividade": self.nome_atividade,
            "descricao": self.descricao,
            "peso_porcento": self.peso_porcento,
            "data_entrega": self.data_entrega,
            "turma_id": self.turma_id,
            "professor_id": self.professor_id
        }

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Float, nullable=False)
    aluno_id = db.Column(db.Integer, nullable=False)
    atividade_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nota": self.nota,
            "aluno_id": self.aluno_id,
            "atividade_id": self.atividade_id
        }