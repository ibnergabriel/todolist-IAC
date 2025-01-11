import sqlite3
from datetime import datetime

DB_PATH = 'app/database/db.sqlite3'

def conectar():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = conectar()
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS Usuario (
        ID_Usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT NOT NULL UNIQUE,
        Nome TEXT NOT NULL,
        Email TEXT NOT NULL UNIQUE,
        Senha TEXT NOT NULL
    )
    ''')

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

    conn.commit()
    conn.close()

# Função para verificar se a tarefa está atrasada
def verificar_atraso(data_limite):
    if data_limite and datetime.strptime(data_limite, '%Y-%m-%d').date() < datetime.now().date():
        return "Atrasada"
    return "Pendente"