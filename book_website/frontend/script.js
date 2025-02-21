
// د کتابونو لیست ترلاسه کول
async function loadBooks() {
    const response = await fetch('http://127.0.0.1:5000/api/books');
    const books = await response.json();
    const bookList = document.getElementById('bookList');
    
    bookList.innerHTML = books.map(book => `
        <div class="book">
            <h3>${book.title}</h3>
            <p>لیکوال: ${book.author}</p>
            <a href="http://127.0.0.1:5000/uploads/${book.file_path}" target="_blank">ولولئ</a>
            ${book.uploaded_by === 'admin' ? `<button onclick="deleteBook(${book.id})">ډیلیټ</button>` : ''}
        </div>
    `).join('');
}

// د کتاب ډیلیټ کول (یوازې اډمین)
async function deleteBook(bookId) {
    const response = await fetch(`http://127.0.0.1:5000/api/books/${bookId}`, {
        method: 'DELETE',
        headers: { 'Authorization': 'Bearer ADMIN_TOKEN' } // دلته د اډمین توکن اضافه کړئ
    });
    if (response.ok) loadBooks();
}

// د اپلوډ فورم پروسس
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('title', document.getElementById('title').value);
    formData.append('author', document.getElementById('author').value);
    formData.append('file', document.getElementById('bookFile').files[0]);

    await fetch('http://127.0.0.1:5000/api/upload', { method: 'POST', body: formData });
    loadBooks();
});

// پیل کې کتابونه وګورئ
loadBooks();
