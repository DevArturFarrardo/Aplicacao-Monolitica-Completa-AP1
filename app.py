# app.py
from flask import Flask, jsonify
from extensions import db, swagger

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///escola.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensões
    db.init_app(app)

    try:
        swagger.init_app(app)
    except Exception:
        try:
            swagger(app)
        except Exception:
            pass

    # Importar e registrar blueprints AQUI para evitar import circular
    from controllers import professor_controller, turma_controller, aluno_controller
    app.register_blueprint(professor_controller.bp)
    app.register_blueprint(turma_controller.bp)
    app.register_blueprint(aluno_controller.bp)

    # Rota raiz amigável que lista os endpoints principais
    @app.route('/', methods=['GET'])
    def index():
        links = {
            'professores': '/professores',
            'turmas': '/turmas',
            'alunos': '/alunos',
            'swagger': '/apidocs'  # flasgger padrão
        }
        return jsonify(links), 200

    # Opcional: imprimir todas as rotas no log para debugging
    print("Rotas registradas:")
    for rule in app.url_map.iter_rules():
        print(rule)

    # Criar tabelas (importar modelos dentro do contexto do app)
    with app.app_context():
        from models import Professor, Turma, Aluno
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)