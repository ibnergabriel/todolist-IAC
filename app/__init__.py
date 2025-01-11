from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes import init_routes
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Carrega as configurações do config.py
    
    db.init_app(app)  # Inicializa o db com o app

    with app.app_context():
        from .models import models  # Importa os modelos
        from .routes import init_routes
        db.create_all()  # Cria as tabelas no banco, se não existirem
        init_routes(app) # Inicializa as rotas
    
    return app