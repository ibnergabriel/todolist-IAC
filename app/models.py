from app.database import db

# Modelo de Usuário
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

    tarefas = db.relationship('Tarefa', backref='usuario', lazy=True)

# Modelo de Tarefa
class Tarefa(db.Model):
    __tablename__ = 'tarefas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    data_limite = db.Column(db.Date)
    hora_limite = db.Column(db.Time)
    recorrencia = db.Column(db.String(50))  # Ex: Diária, Semanal, Mensal
    status = db.Column(db.String(20), default='Pendente')
    prioridade = db.Column(db.String(30), nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    notificacoes = db.relationship('Notificacao', backref='tarefa', lazy=True)

# Modelo de Notificação
class Notificacao(db.Model):
    __tablename__ = 'notificacoes'
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    data_horario = db.Column(db.DateTime, nullable=False)

    tarefa_id = db.Column(db.Integer, db.ForeignKey('tarefas.id'), nullable=False)
