from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

# Criando a API
app = FastAPI()

# Conectando ao banco de dados SQLite
conn = sqlite3.connect("doutrina.db", check_same_thread=False)
cursor = conn.cursor()

# Criando a tabela para armazenar os textos dos doutrinadores
cursor.execute("""
CREATE TABLE IF NOT EXISTS doutrinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    autor TEXT NOT NULL,
    titulo TEXT NOT NULL,
    conteudo TEXT NOT NULL,
    referencia TEXT NOT NULL
)
""")
conn.commit()

# Modelo de dados para a API
class Doutrina(BaseModel):
    autor: str
    titulo: str
    conteudo: str
    referencia: str

# Rota para adicionar um novo texto doutrinário
@app.post("/add/")
def add_doutrina(doutrina: Doutrina):
    cursor.execute("INSERT INTO doutrinas (autor, titulo, conteudo, referencia) VALUES (?, ?, ?, ?)", 
                   (doutrina.autor, doutrina.titulo, doutrina.conteudo, doutrina.referencia))
    conn.commit()
    return {"message": "Texto adicionado com sucesso!"}

# Rota para listar todas as doutrinas
@app.get("/listar/")
def listar_doutrinas():
    cursor.execute("SELECT id, autor, titulo, conteudo, referencia FROM doutrinas")
    resultados = cursor.fetchall()
    return [{"id": r[0], "autor": r[1], "titulo": r[2], "conteudo": r[3], "referencia": r[4]} for r in resultados]

# Rota para buscar textos por autor
@app.get("/buscar/{autor}")
def buscar_doutrina(autor: str):
    cursor.execute("SELECT id, autor, titulo, conteudo, referencia FROM doutrinas WHERE autor = ?", (autor,))
    resultados = cursor.fetchall()
    if not resultados:
        raise HTTPException(status_code=404, detail="Nenhum texto encontrado para esse autor.")
    return [{"id": r[0], "autor": r[1], "titulo": r[2], "conteudo": r[3], "referencia": r[4]} for r in resultados]

# Iniciar a API usando: `uvicorn main:app --reload`

@app.get("/pesquisa/")
def pesquisa(termo: str):
    cursor.execute("SELECT * FROM doutrinas WHERE conteudo LIKE ?", ('%' + termo + '%',))
    resultados = cursor.fetchall()
    if not resultados:
        raise HTTPException(status_code=404, detail="Nenhum resultado encontrado.")
    return [{"id": r[0], "categoria": r[1], "autor": r[2], "titulo": r[3], "conteudo": r[4], "referencia": r[5]} for r in resultados]
