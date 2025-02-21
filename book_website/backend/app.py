
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import mysql.connector

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads'

# د MySQL اتصال
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Moh123@#$",
    database="library"
)

@app.route('/api/books', methods=['GET'])
def get_books():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return jsonify(books)

@app.route('/api/upload', methods=['POST'])
def upload_book():
    title = request.form.get('title')
    author = request.form.get('author')
    file = request.files['file']
    
    if file.filename.endswith(('.pdf', '.epub')):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, file_path, uploaded_by) VALUES (%s, %s, %s, %s)",
            (title, author, file.filename, 'user')
        )
        db.commit()
        return jsonify({"message": "کتاب اپلوډ شو!"}), 201
    else:
        return jsonify({"error": "ناسم فایل فورمټ!"}), 400

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    # د اډمین توکن وګورئ (د مثال لپاره)
    auth_header = request.headers.get('Authorization')
    if auth_header != 'Bearer ADMIN_TOKEN':
        return jsonify({"error": "اجازه نشته!"}), 403
    
    cursor = db.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    db.commit()
    return jsonify({"message": "کتاب ډیلیټ شو!"})

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)