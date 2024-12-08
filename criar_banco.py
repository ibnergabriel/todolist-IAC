import sys
import os

# Adiciona o diretório raiz ao caminho do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from app import create_app
from app.database import db

# Criação do aplicativo Flask
app = create_app()

# Cria as tabelas no banco de dados
with app.app_context():
    db.create_all()

print("Banco de dados criado com sucesso!")
