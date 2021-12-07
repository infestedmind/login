import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')

conn = psycopg2.connect(database='postgres', 
                        user='postgres', 
                        password='root', 
                        host='localhost',
                        port='5432')
cursor = conn.cursor()

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            try:
                cursor.execute("SELECT * FROM service.users WHERE login=%s AND pass=%s",
                               (str(username), str(password)))
                records = list(cursor.fetchall())
                return render_template('account.html', full_name=records[0][1])
            except:
                return "Введите корректные данные"

        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        if not name.replace(' ', '').isalpha():
            return 'Нельзя использовать цифры в имени'
        login = request.form.get('login')
        password = request.form.get('password')
        cursor.execute("SELECT * FROM service.users WHERE login=%s",
        (str(login),))
        if not cursor.fetchone():
            cursor.execute('INSERT INTO service.users (fullname, login, pass) VALUES (%s, %s, %s);',
            (str(name), str(login), str(password)))
            conn.commit()
        else:
            return "Вы уже зарегистрированны"
        return redirect('/login/')
    return render_template('registration.html')
