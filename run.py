from app import create_app
from app.models import init_db

app = create_app()

if __name__ == '__main__':
    init_db()
    
    # Limpa a sessão ao reiniciar a aplicação
    with app.app_context():
        app.secret_key = 'sua_chave_secreta_aqui'  # Certifique-se de usar a mesma chave secreta
        app.permanent_session_lifetime = 0  # Sessão expira quando o navegador é fechado

    app.run(debug=True)