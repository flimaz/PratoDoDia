import os
import sqlite3

def init_db():
    # Cria a pasta db se não existir
    os.makedirs("db", exist_ok=True)

    # Caminho do banco de dados
    db_path = "db/PratoDoDia.db"
    
    # Conecta ou cria o banco
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tabela de pedidos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cidade TEXT NOT NULL,
        nome TEXT NOT NULL,
        descricao TEXT NOT NULL,
        criado_em TEXT NOT NULL
    )
    """)

    # Tabela de ofertas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ofertas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cidade TEXT NOT NULL,
        nome TEXT NOT NULL,
        descricao TEXT NOT NULL,
        criado_em TEXT NOT NULL
    )
    """)
    
    # Tabela de Avisos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avisos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cidade TEXT,
        mensagem TEXT,
        criado_em TEXT
    )
    """)


    conn.commit()
    conn.close()

# Executa se rodar diretamente (opcional)
if __name__ == "__main__":
    init_db()
