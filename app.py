from flask import Flask, redirect, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "redirect.db"

# Inicializa o banco de dados na primeira execução
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS redirect (id INTEGER PRIMARY KEY, url TEXT)")
        conn.execute("INSERT OR IGNORE INTO redirect (id, url) VALUES (1, 'https://www.ujamaatech.com.br/')")
        conn.commit()

@app.route('/')
def redirecionar():
    """Redireciona automaticamente para a URL salva no banco de dados."""
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT url FROM redirect WHERE id = 1")
        url = cur.fetchone()
    return redirect(url[0] if url else "https://www.ujamaatech.com.br/")

@app.route('/update', methods=['POST'])
def update_url():
    """Atualiza o destino do QR Code via API."""
    new_url = request.json.get("url")
    if not new_url:
        return jsonify({"error": "URL inválida"}), 400

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE redirect SET url = ? WHERE id = 1", (new_url,))
        conn.commit()
    return jsonify({"message": "Destino atualizado!", "new_url": new_url})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
