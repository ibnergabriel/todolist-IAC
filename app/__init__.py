from flask import Flask
from .routes import init_routes

def create_app():
    app = Flask(__name__)
    app.secret_key = 'sua_chave_secreta_aqui'
    
    # Inicializa as rotas
    init_routes(app)
    
    return app