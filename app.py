# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///escola.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

swagger = Swagger(app)

# Importar models
from models import Professor, Turma, Aluno

# Importar controllers
from controllers import professor_controller, turma_controller, aluno_controller

# Registrar blueprints
app.register_blueprint(professor_controller.bp)
app.register_blueprint(turma_controller.bp)
app.register_blueprint(aluno_controller.bp)

# Criar tabelas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)