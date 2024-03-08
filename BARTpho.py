from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import mysql.connector
import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from Crypto.PublicKey import RSA
from Crypto.Hash import MD5, SHA1, SHA256, SHA512
from Crypto.Cipher import PKCS1_v1_5
from random import randint

app = Flask(__name__)
app.secret_key = 'vuongquangdai'

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="nln"
)
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")
cursor.execute("CREATE TABLE IF NOT EXISTS user_favorite (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, thesis_id INT, FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (thesis_id) REFERENCES data(id))")
cursor.execute("SELECT * FROM `data`;")
data = cursor.fetchall()

X = [row[0:10] for row in data]
y = [row[11] for row in data]

# Chia dữ liệu thành train và test với tỷ lệ 80-20
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# bert_embeddings = None
bert_embeddings = np.load('bert_embeddings.npy')
tokenizer = AutoTokenizer.from_pretrained("vinai/bartpho-word")
model = AutoModel.from_pretrained("vinai/bartpho-word")


@app.route('/')
def index():
    return render_template('index.html', data=data)


def calculate_similarity(query_embedding, document_embeddings):
    query_embedding = query_embedding.flatten().reshape(1, -1)
    document_embeddings = np.array(document_embeddings).reshape(len(document_embeddings), -1)

    similarities = cosine_similarity(query_embedding, document_embeddings)

    sorted_indices = np.argsort(similarities[0])[::-1]
    sorted_documents = [data[i] for i in sorted_indices]
    return sorted_documents


def sort_documents(keyword):
    keyword_tokens = tokenizer(keyword, return_tensors='pt')['input_ids']
    with torch.no_grad():
        keyword_embedding = model(keyword_tokens).last_hidden_state.mean(dim=1).numpy()
    sorted_documents = calculate_similarity(keyword_embedding, bert_embeddings)
    return sorted_documents


@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')
    sorted_documents = sort_documents(keyword)
    if 'username' in session:
        username = session['username']
        cursor.execute("SELECT data.* FROM data JOIN user_favorite ON data.id = user_favorite.thesis_id JOIN users ON users.id = user_favorite.user_id WHERE users.username = %s", (username,))
        saved_thesis_id = [row[0] for row in cursor.fetchall()]
        return render_template('search_results.html', keyword=keyword, results=sorted_documents, saved_thesis_id=saved_thesis_id)
    return render_template('search_results.html', keyword=keyword, results=sorted_documents)


@app.route('/suggest', methods=['GET'])
def suggest():
    keyword = request.args.get('keyword', '')
    sorted_documents = sort_documents(keyword)
    return jsonify(suggestions=sorted_documents)


@app.route('/detail/<int:id>')
def detail(id):
    cursor.execute("SELECT * FROM `data` WHERE id = %s;", (id,))
    thesis_data = cursor.fetchone()
    if 'username' in session:
        username = session['username']
        cursor.execute("SELECT data.* FROM data JOIN user_favorite ON data.id = user_favorite.thesis_id JOIN users ON users.id = user_favorite.user_id WHERE users.username = %s", (username,))
        saved_thesis_id = [row[0] for row in cursor.fetchall()]
        return render_template('detail.html', data=thesis_data, saved_thesis_id=saved_thesis_id)
    return render_template('detail.html', data=thesis_data)


@app.route('/list')
def list():
    if 'username' in session:
        username = session['username']
        cursor.execute("SELECT data.* FROM data JOIN user_favorite ON data.id = user_favorite.thesis_id JOIN users ON users.id = user_favorite.user_id WHERE users.username = %s", (username,))
        saved_thesis_id = [row[0] for row in cursor.fetchall()]
        return render_template('list.html', data=data, saved_thesis_id=saved_thesis_id)
    return render_template('list.html', data=data)


def hashing(password):
    pw = password.encode()
    func = randint(0, 3)
    if func == 0: result = MD5.new(pw)
    if func == 1: result = SHA1.new(pw)
    if func == 2: result = SHA256.new(pw)
    if func == 3: result = SHA512.new(pw)
    rs = result.hexdigest().upper()
    return rs


def re_hashing(password):
    pw = password.encode()
    result1 = MD5.new(pw)
    result2 = SHA1.new(pw)
    result3 = SHA256.new(pw)
    result4 = SHA512.new(pw)
    rs1 = result1.hexdigest().upper()
    rs2 = result2.hexdigest().upper()
    rs3 = result3.hexdigest().upper()
    rs4 = result4.hexdigest().upper()
    rs = [rs1, rs2, rs3, rs4]
    return rs


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password = hashing(password)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
    
        if existing_user:
            # return "Tên người dùng đã tồn tại! Vui lòng chọn tên người dùng khác."
            return "Username already exists"
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            session['username'] = username
            return redirect(url_for('profile'))    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password = re_hashing(password)
        
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s OR password = %s OR password = %s OR password = %s", (username, password[0], password[1], password[2], password[3]))
        user = cursor.fetchone()
        results = cursor.fetchall() #Đọc cho có để sửa lỗi chứ ko sd

        if user:
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            # return "Đăng nhập không thành công. Vui lòng kiểm tra lại thông tin đăng nhập."
            return "Login unsuccessful"
    return render_template('login.html')


@app.route('/profile')
def profile():
    if 'username' in session:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/thesis/<int:id>/save', methods=['POST'])
def save_thesis(id):
    if 'username' in session:
        thesis_id = id
        username = session['username']
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM user_favorite WHERE user_id = %s AND thesis_id = %s", (user_id, thesis_id))
        already_saved = cursor.fetchone()
        if already_saved:
            return "Luận văn đã được lưu trước đó!"

        cursor.execute("INSERT INTO user_favorite (user_id, thesis_id) VALUES (%s, %s)", (user_id, thesis_id))
        db.commit()
        return "Lưu luận văn yêu thích thành công!"
    else:
        return render_template('login.html')


@app.route('/delete-favorite-thesis/<int:thesis_id>', methods=['POST'])
def delete_favorite_thesis(thesis_id):
    if 'username' in session:
        username = session['username']
        cursor.execute("DELETE FROM user_favorite WHERE user_id = (SELECT id FROM users WHERE username = %s) AND thesis_id = %s", (username, thesis_id))
        db.commit()
        return "Luận văn đã được xóa khỏi danh sách yêu thích."
    else:
        return "Vui lòng đăng nhập để thực hiện thao tác này."


@app.route('/favorite-theses')
def favorite_theses():
    if 'username' in session:
        username = session['username']
        cursor.execute("SELECT data.* FROM data JOIN user_favorite ON data.id = user_favorite.thesis_id JOIN users ON users.id = user_favorite.user_id WHERE users.username = %s", (username,))
        favorite_theses = cursor.fetchall()
        return render_template('profile.html', data=favorite_theses)
    else:
        return render_template('login.html')
    

if __name__ == '__main__':
    app.run(debug=True)