from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

db = SQLAlchemy()
api = Api(title="Atividades API", doc="/docs")