from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

messages_file = 'messages.json'  # Mesajların saklanacağı dosya
channels = {'general': []}  # Kanal sistemi
current_channel = 'general'
active_users = set()  # Aktif kullanıcıları takip et

# Mesajları yükle
def load_messages():
    if os.path.exists(messages_file):
        with open(messages_file) as f:
            return json.load(f)
    return []

# Mesajları kaydet
def save_messages(messages):
    with open(messages_file, 'w') as f:
        json.dump(messages, f)

# Kullanıcıları yükle
def load_users():
    if os.path.exists('users.json'):
        with open('users.json') as f:
            return json.load(f)
    return []

# Kullanıcıları kaydet
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', messages=load_messages(), channels=channels.keys(), current_channel=current_channel, active_users=list(active_users))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                active_users.add(username)  # Kullanıcıyı aktif olarak ekle
                return redirect(url_for('index'))
        return "Hatalı kullanıcı adı veya şifre", 403
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        users.append({'username': username, 'password': password})
        save_users(users)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/send', methods=['POST'])
def send():
    message = request.form['message']
    username = session['username']
    new_message = f"{username}: {message}"  # Mesajı oluştur
    messages = load_messages()  # Mevcut mesajları yükle
    messages.append(new_message)  # Mesajı ekle
    save_messages(messages)  # Mesajları dosyaya kaydet
    channels[current_channel].append(new_message)  # Mesajı kanala ekle
    return jsonify({'status': 'success', 'message': new_message})

@app.route('/dm', methods=['POST'])
def dm():
    recipient = request.form['recipient']
    message = request.form['message']
    sender = session['username']
    dm_message = f"DM from {sender} to {recipient}: {message}"  # DM mesajı oluştur
    messages = load_messages()  # Mevcut mesajları yükle
    messages.append(dm_message)  # DM mesajını ekle
    save_messages(messages)  # Mesajları dosyaya kaydet
    return jsonify({'status': 'success', 'message': dm_message})

@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(load_messages())  # Tüm mesajları döndür

@app.route('/create_channel', methods=['POST'])
def create_channel():
    channel_name = request.form['channel_name']
    if channel_name not in channels:
        channels[channel_name] = []  # Yeni kanalı oluştur
    return jsonify({'status': 'success', 'channel': channel_name})

@app.route('/switch_channel', methods=['POST'])
def switch_channel():
    global current_channel
    current_channel = request.form['channel_name']
    return jsonify({'status': 'success', 'channel': current_channel})

@app.route('/logout')
def logout():
    active_users.discard(session['username'])  # Kullanıcıyı aktif listeden çıkar
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
