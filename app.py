from flask import Flask, request, jsonify, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__, static_folder='public')
DB_FILE = 'cards.db'

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                card_number TEXT NOT NULL,
                expiry TEXT NOT NULL,
                credit_limit REAL NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

init_db()

# --- Static File Routes ---

@app.route('/')
def serve_index():
    return send_from_directory('public', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join('public', path)):
        return send_from_directory('public', path)
    return "Not Found", 404

# --- API Routes ---

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    hashed_pw = generate_password_hash(password)
    with get_db() as conn:
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_pw))
            conn.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Username already exists'}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    with get_db() as conn:
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and check_password_hash(user['password'], password):
            return jsonify({'message': 'Login successful', 'username': username}), 200
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/cards', methods=['GET'])
def get_cards():
    with get_db() as conn:
        cards = conn.execute('SELECT * FROM cards').fetchall()
        return jsonify([dict(row) for row in cards])

@app.route('/api/cards', methods=['POST'])
def add_card():
    data = request.json
    name = data.get('name')
    card_number = data.get('card_number')
    expiry = data.get('expiry')
    credit_limit = data.get('credit_limit')

    if not all([name, card_number, expiry, credit_limit is not None]):
        return jsonify({'error': 'All fields are required'}), 400

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO cards (name, card_number, expiry, credit_limit) VALUES (?, ?, ?, ?)',
            (name, card_number, expiry, credit_limit)
        )
        conn.commit()

        return jsonify({
            'id': cursor.lastrowid,
            'name': name,
            'card_number': card_number,
            'expiry': expiry,
            'credit_limit': credit_limit
        })

@app.route('/api/cards/<int:id>', methods=['DELETE'])
def delete_card(id):
    with get_db() as conn:
        conn.execute('DELETE FROM cards WHERE id = ?', (id,))
        conn.commit()
    return jsonify({'message': 'Card deleted'})

@app.route('/api/cards/search', methods=['GET'])
def search_cards():
    q = request.args.get('q', '')
    with get_db() as conn:
        cards = conn.execute(
            "SELECT * FROM cards WHERE name LIKE ? OR card_number LIKE ?",
            (f'%{q}%', f'%{q}%')
        ).fetchall()
        return jsonify([dict(row) for row in cards])

@app.route('/api/summary', methods=['GET'])
def get_summary():
    with get_db() as conn:
        row = conn.execute('SELECT COUNT(*) as total, COALESCE(SUM(credit_limit), 0) as total_limit FROM cards').fetchone()
        return jsonify(dict(row))

if __name__ == '__main__':
    app.run(port=3000, debug=True)
