from flask import Flask, jsonify
from extensions import db, swagger
from controllers import professor_controller, turma_controller, aluno_controller

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/escola.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SWAGGER'] = {
        'title': 'Gerenciamento Escolar API',
        'uiversion': 3
    }

    # inicializa extensões
    db.init_app(app)          # ✅ apenas uma vez
    swagger.init_app(app)

    # registra blueprints
    app.register_blueprint(professor_controller.bp)
    app.register_blueprint(turma_controller.bp)
    app.register_blueprint(aluno_controller.bp)

    @app.route('/', methods=['GET'])
    def index():
        links = {
            'professores': '/professores',
            'turmas': '/turmas',
            'alunos': '/alunos',
            'swagger': '/apidocs'
        }
        return jsonify(links), 200

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
