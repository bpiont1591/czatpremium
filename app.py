from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('set_user_category')
def handle_set_user_category(data):
    session['username'] = data['username']
    session['category'] = data['category']
    emit('message', {'username': 'System', 'message': f"{session['username']} dołączył do czatu w kategorii {session['category']}.", 'category': 'System'}, broadcast=True)

@socketio.on('message')
def handle_message(data):
    username = session.get('username', 'Anonimowy')
    category = session.get('category', 'ogólna')
    emit('message', {'username': username, 'message': data['message'], 'category': category}, broadcast=True)

@socketio.on('connect')
def handle_connect():
    username = session.get('username', 'Anonimowy')
    category = session.get('category', 'ogólna')
    emit('message', {'username': 'System', 'message': f"{username} dołączył do czatu w kategorii {category}.", 'category': 'System'}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username', 'Anonimowy')
    category = session.get('category', 'ogólna')
    emit('message', {'username': 'System', 'message': f"{username} opuścił czat w kategorii {category}.", 'category': 'System'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
