from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app, title="Reservas API", doc="/docs")

# importa modelos e rotas (após db criado)
import models
import routes

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)