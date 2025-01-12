from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import conectar, init_db, verificar_atraso
from datetime import datetime

def init_routes(app):
    @app.route('/')
    def index():
        if 'usuario_id' in session:
            return redirect(url_for('tarefas'))
        return render_template('login.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            senha = request.form['senha']

            conn = conectar()
            c = conn.cursor()
            c.execute('SELECT * FROM Usuario WHERE Username = ?', (username,))
            usuario = c.fetchone()
            conn.close()

            if usuario and check_password_hash(usuario[4], senha):
                session['usuario_id'] = usuario[0]
                session['username'] = usuario[1]
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

            if senha != confirmar_senha:
                flash('As senhas não coincidem. Por favor, tente novamente.', 'error')
                return redirect(url_for('registro'))

            senha_hash = generate_password_hash(senha)

            conn = conectar()
            c = conn.cursor()
            try:
                c.execute('''
                INSERT INTO Usuario (Username, Nome, Email, Senha)
                VALUES (?, ?, ?, ?)
                ''', (username, nome, email, senha_hash))
                conn.commit()
                flash('Registro realizado com sucesso! Faça login.', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError as e:
                flash('Erro ao registrar. Usuário ou e-mail já existente.', 'error')
            finally:
                conn.close()

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

        conn = conectar()
        c = conn.cursor()
        c.execute('''
        SELECT ID_Tarefa, Titulo, Descricao, Data_Limite, Status, Data_Conclusao, Prioridade
        FROM Tarefa
        WHERE ID_Usuario = ?
        ''', (session['usuario_id'],))
        tarefas = c.fetchall()
        conn.close()

        return render_template('index.html', tarefas=tarefas)

    @app.route('/tarefa', methods=['POST'])
    def criar_tarefa():
        if 'usuario_id' not in session:
            flash('Você precisa fazer login para acessar esta página.', 'error')
            return redirect(url_for('login'))

        titulo = request.form['titulo']
        descricao = request.form.get('descricao', '')
        data_limite = request.form.get('data_limite', None)
        status = verificar_atraso(data_limite)
        prioridade = int(request.form.get('prioridade', 3))
        id_usuario = session['usuario_id']

        conn = conectar()
        c = conn.cursor()
        try:
            c.execute('''
            INSERT INTO Tarefa (Titulo, Descricao, Data_Limite, Status, Prioridade, ID_Usuario)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (titulo, descricao, data_limite, status, prioridade, id_usuario))
            conn.commit()
            flash('Tarefa criada com sucesso!', 'success')
        except sqlite3.IntegrityError as e:
            flash('Erro ao criar tarefa.', 'error')
        finally:
            conn.close()

        return redirect(url_for('tarefas'))

    @app.route('/tarefa/<int:id_tarefa>/status', methods=['POST'])
    def atualizar_status(id_tarefa):
        if 'usuario_id' not in session:
            flash('Você precisa fazer login para acessar esta página.', 'error')
            return redirect(url_for('login'))

        novo_status = request.form['status']
        conn = conectar()
        c = conn.cursor()
        c.execute('''
        UPDATE Tarefa
        SET Status = ?, Data_Conclusao = ?
        WHERE ID_Tarefa = ? AND ID_Usuario = ?
        ''', (novo_status, datetime.now().strftime('%Y-%m-%d'), id_tarefa, session['usuario_id']))
        conn.commit()
        conn.close()
        flash('Status da tarefa atualizado com sucesso!', 'success')
        return redirect(url_for('tarefas'))

    @app.route('/tarefa/<int:id_tarefa>', methods=['POST'])
    def excluir_tarefa(id_tarefa):
        if 'usuario_id' not in session:
            flash('Você precisa fazer login para acessar esta página.', 'error')
            return redirect(url_for('login'))

        conn = conectar()
        c = conn.cursor()
        c.execute('DELETE FROM Tarefa WHERE ID_Tarefa = ? AND ID_Usuario = ?', (id_tarefa, session['usuario_id']))
        conn.commit()
        conn.close()
        flash('Tarefa excluída com sucesso!', 'success')
        return redirect(url_for('tarefas'))
#  rota para lidar com a edição de tarefas.
    @app.route('/tarefa/<int:id_tarefa>/editar', methods=['POST'])
    def editar_tarefa(id_tarefa):
        if 'usuario_id' not in session:
            flash('Você precisa fazer login para acessar esta página.', 'error')
            return redirect(url_for('login'))

        titulo = request.form['titulo']
        descricao = request.form.get('descricao', '')
        data_limite = request.form.get('data_limite', None)
        prioridade = int(request.form.get('prioridade', 3))

        conn = conectar()
        c = conn.cursor()
        try:
            c.execute('''
            UPDATE Tarefa
            SET Titulo = ?, Descricao = ?, Data_Limite = ?, Prioridade = ?
            WHERE ID_Tarefa = ? AND ID_Usuario = ?
            ''', (titulo, descricao, data_limite, prioridade, id_tarefa, session['usuario_id']))
            conn.commit()
            flash('Tarefa atualizada com sucesso!', 'success')
        except sqlite3.IntegrityError as e:
            flash('Erro ao atualizar tarefa.', 'error')
        finally:
            conn.close()

        return redirect(url_for('tarefas')) 