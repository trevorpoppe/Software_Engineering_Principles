from flask import Flask, request, render_template
import sqlite3
import pandas as pd
import os

app = Flask(__name__)
db_name = 'bookkeeper.db'

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file.filename.endswith('.csv'):
        path = os.path.join("uploads", "temp.csv")
        file.save(path)
        df = pd.read_csv(path)
        df.to_sql("transactions", sqlite3.connect(db_name), if_exists='replace', index=False)
    return render_template("index.html")

@app.route('/query', methods=['POST'])
def query():
    sql_query = request.form['query']
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description] if cursor.description else []
    except Exception as e:
        return render_template("index.html", results=[], error=str(e))

    conn.close()
    return render_template("index.html", results=[headers] + rows)

if __name__ == '__main__':
    app.run(debug=True)
