
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your secret key'

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="DevaranjaniAmuth$list"
        )
        message = "Successfully Connected"
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

@app.route('/index')
def index():
    conn = get_db_connection()
    if conn is None:
        return "Error connecting to database"
    
    try:
        mycursor = conn.cursor()
        mycursor.execute("SELECT name, reg, mark FROM list")
        results = mycursor.fetchall()
        conn.close()
        message = "Successfully fetched data"
        return render_template('report.html', results=results, message=message)
    except Error as e:
        conn.close()
        return f"Error: {str(e)}"


@app.route('/addlist')
def addlist():
    return render_template('add list.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    reg = request.form['reg']
    mark = request.form['mark']

    conn = get_db_connection()
    if conn is None:
        return "Error connecting to database"

    try:
        mycursor = conn.cursor()
        mycursor.execute("INSERT INTO list (name, reg, mark) VALUES (%s, %s, %s)", (name, reg, mark))
        conn.commit()
        return redirect(url_for('index'))
    except Error as e:
        return f"Error: {str(e)}"
    finally:
        conn.close()

if __name__== '__main__':
    app.run(port=5000,debug=True)