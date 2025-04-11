from flask import Flask, request, render_template
import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_schema_from_db():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
    schemas = cursor.fetchall()
    conn.close()
    schema_strings = []
    for name, schema in schemas:
        schema_strings.append(f"-- Table name: {name}\n{schema}")
    return "\n".join(schema_strings)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
    import openai
    from openai import OpenAI

    user_prompt = request.form['prompt']
    
    try:
        schema = get_schema_from_db()

        prompt_with_schema = f"""
        Given the following SQLite database schema:

        {schema}

        Write an SQLite SELECT query to answer this question:
        {user_prompt}

        Return ONLY the query without explanation.
        """

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that only returns valid SQLite SELECT queries with no explanations."
                },
                {
                    "role": "user",
                    "content": prompt_with_schema
                }
            ],
            temperature=0.2,
            max_tokens=200
        )

        sql_query = response.choices[0].message.content.strip()
        print("Generated SQL:", repr(sql_query))

        if not sql_query.lower().startswith("select"):
            raise ValueError("AI did not return a valid SELECT query.")

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
