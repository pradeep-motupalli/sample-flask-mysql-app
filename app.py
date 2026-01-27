import os
from flask import Flask, jsonify, render_template,url_for
import pymysql

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'test_db')

def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.Cursor
        autocommit=True
    )

def init_db():
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT
        );
    """)
    cur.close()
    connection.close()

@app.route('/')
def hello():
    Connection = get_db_connection()
    cursor = Connection.cursor()
    cursor.execute("select message fFROM messages order by id desc limit 1;")
    result = cursor.fetchall()
    cursor.close()
    Connection.close()
    return render_template('index.html', message=result[0][0] if result else "No messages found.")

@app.route('/submit', methods=['POST'])

def submit():
    Connection = get_db_connection()
    cursor = Connection.cursor()
    cursor.execute("INSERT INTO messages (message) VALUES ('%s');", (new_message,))
    cursor.close()
    Connection.close()
    return jsonify({"status": new_message})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

