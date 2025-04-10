from flask import Flask, request, render_template
import sqlite3
import pandas as pd
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure to set this in your shell or .env


app = Flask(__name__)
db_name = 'bookkeeper.db'

os.makedirs("uploads", exist_ok=True)

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and file.filename.endswith('.csv'):
        path = os.path.join("uploads", "temp.csv")
        file.save(path)
        df = pd.read_csv(path)
        df.to_sql("sales", sqlite3.connect(db_name), if_exists='replace', index=False)
        
        # Show success message and table preview
        preview = df.head().values.tolist()
        columns = df.columns.tolist()
        return render_template("index.html", uploaded=True, columns=columns, preview=preview)

    return render_template("index.html", error="Invalid file type. Please upload a CSV.")


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

@app.route('/ask', methods=['POST'])
def ask():
    user_prompt = request.form['prompt']

    try:
        # Use the Chat API with gpt-3.5-turbo or gpt-4
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that only returns valid SQLite SELECT queries with no explanations."
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.2,
            max_tokens=200
        )

        sql_query = response.choices[0].message.content.strip()
        print("Generated SQL:", repr(sql_query))

        # Make sure the response starts with SELECT
        if not sql_query.lower().startswith("select"):
            raise ValueError("AI did not return a valid SELECT query.")

        # Execute the SQL
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description] if cursor.description else []
        conn.close()

        return render_template("index.html", ai_query=sql_query, results=[headers] + rows)

    except Exception as e:
        return render_template("index.html", error=f"AI query error: {e}")



if __name__ == '__main__':
    app.run(debug=True)
