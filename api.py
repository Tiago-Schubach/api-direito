from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Modelo de dados para receber a pergunta e resposta corretamente
class PerguntaModelo(BaseModel):
    pergunta: str
    resposta: str

# Função para conectar ao banco de dados
def conectar_bd():
    return sqlite3.connect("dados.db")

# Endpoint para salvar uma pergunta e resposta (Corrigido)
@app.post("/pergunta/")
def salvar_pergunta(dados: PerguntaModelo):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversas (pergunta, resposta) VALUES (?, ?)", (dados.pergunta, dados.resposta))
    conn.commit()
    conn.close()
    return {"mensagem": "Pergunta e resposta salvas com sucesso!"}

# Endpoint para listar todas as perguntas e respostas (Corrigido)
@app.get("/perguntas/")
def listar_perguntas():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id, pergunta, resposta, data FROM conversas")
    perguntas = cursor.fetchall()
    conn.close()

    # Retornar um dicionário corretamente formatado
    return {
        "perguntas": [
            {"id": p[0], "pergunta": p[1], "resposta": p[2], "data": p[3]}
            for p in perguntas
        ]
    }
