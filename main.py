from flask import Flask, render_template, request, flash, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="deva"
        )
        print("Connected successfully")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

@app.route('/switch', methods=['GET', 'POST'])
def switch():
    conn = get_db_connection()
    if conn is None:
        flash("Connection Failed", "error")
        return render_template('switch.html', message="Connection Failed", switch1=0, switch2=0)

    if request.method == 'POST':
        switch1 = 1 if request.form.get('switch1') else 0
        switch2 = 1 if request.form.get('switch2') else 0

        try:
            mycursor = conn.cursor()
            mycursor.execute("UPDATE switch SET switch1 = %s, switch2 = %s WHERE ID = 1", (switch1, switch2))
            conn.commit()
            flash("Successfully Updated", "success")
        except Error as e:
            print(f"Error updating data: {e}")
            flash(f"Error: {e}", "error")
        finally:
            mycursor.close()

    try:
        mycursor = conn.cursor(dictionary=True)
        mycursor.execute("SELECT switch1, switch2 FROM switch WHERE ID = 1")
        result = mycursor.fetchone()
        switch1 = result['switch1']
        switch2 = result['switch2']
    except Error as e:
        print(f"Error fetching data: {e}")
        switch1, switch2 = 0, 0
    finally:
        conn.close()

    return render_template('switch.html', message="", switch1=switch1, switch2=switch2)

@app.route('/switch_state', methods=['GET'])
def switch_state():
    conn = get_db_connection()
    if conn is None:
        return "Connection Failed"

    try:
        mycursor = conn.cursor(dictionary=True)
        mycursor.execute("SELECT switch1, switch2 FROM switch WHERE ID = 1")
        result = mycursor.fetchone()
        if result:
            result_str = f"({result['switch1']}-{result['switch2']})"
            return result_str
        else:
            return "No data found"

    except Error as e:
        print(f"Error fetching data: {e}")
        return "Error fetching data"
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host="192.168.29.244", port="5000", debug=True)
