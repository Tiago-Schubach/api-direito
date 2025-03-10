import sqlite3

# Conectar ao banco de dados (ou criar um novo)
conn = sqlite3.connect("dados.db")
cursor = conn.cursor()

# Criar a tabela de perguntas e respostas
cursor.execute('''
CREATE TABLE IF NOT EXISTS conversas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pergunta TEXT NOT NULL,
    resposta TEXT NOT NULL,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Salvar e fechar
conn.commit()
conn.close()

print("Banco de dados criado com sucesso!")
