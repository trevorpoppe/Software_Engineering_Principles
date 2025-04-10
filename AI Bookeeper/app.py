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
        # Ask OpenAI to generate a SQL query
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Only return a valid SQLite SELECT query for this request: {user_prompt}",
            max_tokens=150,
            temperature=0.2
        )

        # Get and clean the SQL
        raw_response = response.choices[0].text.strip()
        print("Raw OpenAI response:", raw_response)

        # Optional: Strip explanation if included
        sql_lines = raw_response.splitlines()
        sql_query = "\n".join(line for line in sql_lines if line.strip().upper().startswith("SELECT"))

        if not sql_query.lower().startswith("select"):
            raise ValueError("The AI did not return a valid SELECT query.")

        # Run the query
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
