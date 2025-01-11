from . import db
from sqlalchemy.types import Enum
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

# Modelo de Usuário
class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)

    # Método para definir a senha
    def set_password(self, senha):
        self.senha_hash = generate_password_hash(senha)

    # Método para verificar a senha
    def check_password(self, senha):
        return check_password_hash(self.senha_hash, senha)


# Enumerador: Define campos com valores restritos a um conjunto específico
class StatusEnum(Enum):
    PENDENTE = 'Pendente'
    CONCLUIDA = 'Concluida'
    ATRASADA = 'Atrasada'

class PrioridadeEnum(Enum):
    ALTA = 'Alta'
    MEDIA = 'Média'
    BAIXA = 'Baixa'

class RecorrenciaEnum(Enum):
    DIARIA = 'Diária'
    SEMANAL = 'Semanal'
    MENSAL = 'Mensal'
    UNICA = 'Unica'
    
# Modelo de Tarefa
class Tarefa(db.Model):
    __tablename__ = 'Tarefas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, nullable=False, default=func.now()) # Vai pegar o horário atual, na hora que criar
    data_hora_limite = db.Column(db.DateTime)
    recorrencia = db.Column(db.Enum(RecorrenciaEnum))  # Ex: Diária, Semanal, Mensal
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.PENDENTE, nullable=False)
    prioridade = db.Column(db.Enum(PrioridadeEnum), default=PrioridadeEnum.BAIXA, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    notificacoes = db.relationship('Notificacao', backref='tarefa', lazy='dynamic')
    
# Modelo de Notificação
class Notificacao(db.Model):
    __tablename__ = 'Notificacoes'
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    data_hora_disparo = db.Column(db.DateTime, nullable=False)
    tarefa_id = db.Column(db.Integer, db.ForeignKey('tarefas.id'), nullable=False)