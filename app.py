from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
import psycopg2
from passlib.hash import sha256_crypt


db = SQLAlchemy()

app = Flask(__name__)

# Конфигурация базы данных
db_config = {
    'host': '127.0.0.1',
    'database': '///',
    'user': '////',
    'password': '123'
}


def connect_db():
    return psycopg2.connect(**db_config)

def dbClose(cursor,connection):
    cursor.close()
    connection.close()

# Подключение к базе данных
def connect_db():
    return psycopg2.connect(**db_config)



# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Страница Регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Проверка пустых значений
        if not username or not password:
            flash('Please fill in all fields', 'error')
            return redirect(url_for('register'))

        # Проверка на наличие пользователя
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
                existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
 # Хеширование
        hashed_password = sha256_crypt.hash(password)

        # Сохранение пароля и имени в бд
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))

    return render_template('register.html')



