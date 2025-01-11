import sqlite3
from datetime import datetime

# Caminho para o banco de dados SQLite
DB_PATH = 'app/database/db.sqlite3'

# Função para conectar ao banco de dados
def conectar():
    """
    Cria uma conexão com o banco de dados SQLite.
    Retorna um objeto de conexão.
    """
    return sqlite3.connect(DB_PATH)

# Função para inicializar o banco de dados
def init_db():
    """
    Inicializa o banco de dados, criando as tabelas 'Usuario' e 'Tarefa' 
    se elas não existirem.
    """
    conn = conectar()
    c = conn.cursor()

    # Criação da tabela Usuario
    c.execute('''
    CREATE TABLE IF NOT EXISTS Usuario (
        ID_Usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT NOT NULL UNIQUE,
        Nome TEXT NOT NULL,
        Email TEXT NOT NULL UNIQUE,
        Senha TEXT NOT NULL
    )
    ''')

    # Criação da tabela Tarefa
    c.execute('''
    CREATE TABLE IF NOT EXISTS Tarefa (
        ID_Tarefa INTEGER PRIMARY KEY AUTOINCREMENT,
        Titulo TEXT NOT NULL,
        Descricao TEXT,
        Data_Limite DATE,
        Data_Conclusao DATE,
        Status TEXT CHECK(Status IN ('Pendente', 'Concluída', 'Atrasada')) DEFAULT 'Pendente',
        Prioridade INTEGER CHECK(Prioridade IN (1, 2, 3)), -- 1: Alta, 2: Média, 3: Baixa
        ID_Usuario INTEGER NOT NULL,
        FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario) ON DELETE CASCADE
    )
    ''')

    # Confirma as alterações no banco de dados
    conn.commit()
    conn.close()

# Função para verificar se a tarefa está atrasada
def verificar_atraso(data_limite):
    """
    Verifica se a data limite da tarefa é anterior à data atual.
    Retorna 'Atrasada' se a data limite for anterior, caso contrário, retorna 'Pendente'.
    """
    if data_limite and datetime.strptime(data_limite, '%Y-%m-%d').date() < datetime.now().date():
        return "Atrasada"
    return "Pendente"
