
from flask import Flask, render_template, request, redirect, url_for, session,make_response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pdfkit


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'users'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            name = request.form.get("username")
            email = request.form.get("user_email")
            phone = request.form.get("user_phone")
            html=render_template("pdf_templete.html",name=name,email=email,phone=phone)
            pdf=pdfkit.from_string(html,False)
            response=make_response(pdf)
            response.headers["Content-Disposition"]="inline;filename=output.pdf"
            return response
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)




