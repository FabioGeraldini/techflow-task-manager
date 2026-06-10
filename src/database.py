import sqlite3

# Caminho do banco de dados
DATABASE = 'tasks.db'

def get_connection():
    """Retorna uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
    return conn

def init_db():
    """Cria a tabela de tarefas se ela não existir."""
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            title    TEXT    NOT NULL,
            status   TEXT    NOT NULL DEFAULT 'A Fazer',
            priority TEXT    NOT NULL DEFAULT 'Média'
        )
    ''')
    conn.commit()
    conn.close()
