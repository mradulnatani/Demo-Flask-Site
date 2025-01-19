# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# In-memory storage for messages and users
messages = []
users = {}

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', messages=messages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username.strip():
            session['username'] = username
            flash(f'Welcome, {username}!')
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/send', methods=['POST'])
def send_message():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = request.form['message'].strip()
    if message:
        messages.append({
            'username': session['username'],
            'content': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True,post=8000,host='0.0.0.0')
