# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

db = SQLAlchemy()
swagger = Swagger()   # instância; será inicializada no create_app()