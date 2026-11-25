from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, make_response
from functools import wraps
import os
import sqlite3
from db import get_db, init_db
from config import PASSWORD, SECRET_KEY

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'bimbambompythonblyat'
app.config['SECRET_KEY'] = SECRET_KEY

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('authorized'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == PASSWORD:
            session['authorized'] = True
            return redirect(url_for('index'))
        flash('НЕПРАВИЛЬНО!!11!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('authorized', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    conn = get_db()
    sellers = conn.execute('SELECT id, nickname, score FROM sellers ORDER BY score DESC').fetchall()
    conn.close()
    return render_template('hallofscumbags.html', sellers=sellers, cnt=len(sellers))

@app.route('/vote/<int:seller_id>', methods=['POST'])
@login_required
def vote(seller_id):
    conn = get_db()
    conn.execute('UPDATE sellers SET score = score + 1 WHERE id = ?', (seller_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/add_seller', methods=['POST'])
@login_required
def add_seller():
    nickname = request.form.get('nickname', '').strip()
    if not nickname:
        flash('ник не может быть пустым)')
        return redirect(url_for('index'))
    conn = get_db()
    try:
        row = conn.execute('SELECT id FROM sellers WHERE nickname = ?', (nickname,)).fetchone()

        if row:
            conn.execute('UPDATE sellers SET score = score + 1 WHERE nickname = ?', (nickname,))
            flash('долбоеб уже учтен в базе')
        else:
            conn.execute('INSERT INTO sellers (nickname, score) VALUES (?, 1)', (nickname,))
            flash('долбоеб успешно добавлен в базу')
        conn.commit()
    finally:
        conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)