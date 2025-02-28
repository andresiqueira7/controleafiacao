import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def criar_banco():
    """Cria o banco de dados e a tabela se não existir"""
    conn = sqlite3.connect("controlebits.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS controlebits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL,
            tipo TEXT NOT NULL,
            marca TEXT NOT NULL,
            afiacao_interna INTEGER,
            afiacao_externa INTEGER,
            operador TEXT NOT NULL,
            data TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/salvar', methods=['POST'])
def salvar_dados():
    """Recebe os dados do formulário e salva no banco"""
    data = request.json
    conn = sqlite3.connect("controlebits.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO controlebits (numero, tipo, marca, afiacao_interna, afiacao_externa, operador, data)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data['numero'], data['tipo'], data['marca'], data['afiacao_interna'], 
          data['afiacao_externa'], data['operador'], data['data']))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Dados salvos com sucesso!"})

@app.route('/dados', methods=['GET'])
def visualizar_dados():
    """Retorna os dados cadastrados no banco"""
    conn = sqlite3.connect("controlebits.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM controlebits")
    dados = cursor.fetchall()
    conn.close()
    return jsonify(dados)

if __name__ == '__main__':
    criar_banco()
    app.run(host='0.0.0.0', port=10000)

from flask import render_template

@app.route('/')
def home():
    return render_template("index.html")
