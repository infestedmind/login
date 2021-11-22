import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)

conn = psycopg2.connect(database='postgres', 
                        user='postgres', 
                        password='root', 
                        host='localhost',
                        port='5432')
cursor = conn.cursor()

@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("SELECT * FROM service.users WHERE login=%s AND pass=%s", 
                    (str(username), str(password)))
    records = list(cursor.fetchall())
    match (username, password):
        case ('', ''):
            return "ВВЕДИТЕ ДАННЫЕ" 
        case (username, ''):
            return "ВВЕДИТЕ ПАРОЛЬ"
        case ('', password):
            return "ВВЕДИте ЛОГИН"
        case (username, password):
            if not records:
                return ('Неверное имя пользователя или пароль')
            else:
                return render_template('account.html', full_name=records[0][1])
