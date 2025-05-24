from flask import Flask, render_template, request
import mysql.connector
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/feedback', methods=['POST'])
def feedback():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    conn = mysql.connector.connect(
        host='db',
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
    conn.commit()
    cursor.close()
    conn.close()

    return "Thanks for your feedback!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)