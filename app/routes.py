from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Usuario, Tarefa, Notificacao, db
from datetime import datetime

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']

        # Busca o usuário pelo username
        usuario = Usuario.query.filter_by(username=username).first()

        # Verifica se o usuário existe e se a senha está correta
        if usuario and usuario.check_password(senha):
            session['usuario_id'] = usuario.id
            session['username'] = usuario.username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('tarefas'))
        else:
            flash('Usuário ou senha incorretos.', 'error')

    return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']

        # Verificar se as senhas coincidem
        if senha != confirmar_senha:
            flash('As senhas não coincidem. Por favor, tente novamente.', 'error')
            return redirect(url_for('registro'))

        # Criar novo usuário e definir a senha com hash
        novo_usuario = Usuario(username=username, nome=nome, email=email)
        novo_usuario.set_password(senha)  # Define o hash da senha

        try:
            db.session.add(novo_usuario)  # Adiciona o usuário ao banco de dados
            db.session.commit()
            flash('Registro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()  # Reverte alterações no banco em caso de erro
            flash('Erro ao registrar. Usuário ou e-mail já existente.', 'error')

    return render_template('registro.html')


    @app.route('/logout')
    def logout():
        session.pop('usuario_id', None)
        session.pop('username', None)
        flash('Logout realizado com sucesso.', 'success')
        return redirect(url_for('index'))

    @app.route('/tarefas')
    def tarefas():
        if 'usuario_id' not in session:
            flash('Você precisa fazer login para acessar esta página.', 'error')
            return redirect(url_for('login'))

        usuario_id = session['usuario_id']
        tarefas = Tarefa.query.filter_by(usuario_id=usuario_id).all()

        return render_template('index.html', tarefas=tarefas)

    @app.route('/tarefa', methods=['POST'])
    def criar_tarefa():
        if 'usuario_id' not in session:
            flash('Você precisa fazer login para acessar esta página.', 'error')
            return redirect(url_for('login'))

        titulo = request.form['titulo']
        descricao = request.form.get('descricao', '')
        data_limite = request.form.get('data_limite', None)
        prioridade = request.form.get('prioridade', 'BAIXA').upper()

        nova_tarefa = Tarefa(
            titulo=titulo,
            descricao=descricao,
            data_hora_limite=data_limite,
            prioridade=prioridade,
            usuario_id=session['usuario_id'],
        )

        db.session.add(nova_tarefa)
        db.session.commit()
        flash('Tarefa criada com sucesso!', 'success')
        return redirect(url_for('tarefas'))

    @app.route('/tarefa/<int:id_tarefa>/status', methods=['POST'])
    def atualizar_status(id_tarefa):
        if 'usuario_id' not in session:
            flash('Você precisa fazer login para acessar esta página.', 'error')
            return redirect(url_for('login'))

        tarefa = Tarefa.query.filter_by(id=id_tarefa, usuario_id=session['usuario_id']).first()

        if not tarefa:
            flash('Tarefa não encontrada.', 'error')
            return redirect(url_for('tarefas'))

        novo_status = request.form['status']
        tarefa.status = novo_status
        if novo_status == 'CONCLUIDA':
            tarefa.data_hora_conclusao = datetime.now()

        db.session.commit()
        flash('Status da tarefa atualizado com sucesso!', 'success')
        return redirect(url_for('tarefas'))

    @app.route('/tarefa/<int:id_tarefa>', methods=['POST'])
    def excluir_tarefa(id_tarefa):
        if 'usuario_id' not in session:
            flash('Você precisa fazer login para acessar esta página.', 'error')
            return redirect(url_for('login'))

        tarefa = Tarefa.query.filter_by(id=id_tarefa, usuario_id=session['usuario_id']).first()

        if not tarefa:
            flash('Tarefa não encontrada.', 'error')
            return redirect(url_for('tarefas'))

        db.session.delete(tarefa)
        db.session.commit()
        flash('Tarefa excluída com sucesso!', 'success')
        return redirect(url_for('tarefas'))
