import psycopg2
import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# URL de conexão do PostgreSQL (substitua pela sua do Supabase)
DATABASE_URL = os.getenv("DATABASE_URL", "postgres://user:password@host:port/dbname")

def criar_banco():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS controlebits (
            id SERIAL PRIMARY KEY,
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
    try:
        data = request.get_json()
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO controlebits (numero, tipo, marca, afiacao_interna, afiacao_externa, operador, data)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (data['numero'], data['tipo'], data['marca'], data['afiacao_interna'],
              data['afiacao_externa'], data['operador'], data['data']))
        conn.commit()
        conn.close()
        return jsonify({"mensagem": "Dados salvos com sucesso!"})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/dados', methods=['GET'])
def visualizar_dados():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM controlebits")
    dados = cursor.fetchall()
    conn.close()
    return jsonify(dados)

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    criar_banco()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
