from flask import Flask, jsonify
from extensions import db, api

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    api.init_app(app)

    @app.route('/', methods=['GET'])
    def index():
        """Exibe os links principais da API de Reservas"""
        links = {
            'reservas': '/reservas',
            'swagger': '/docs'
        }
        return jsonify(links), 200

    with app.app_context():
        import models
        import routes

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)