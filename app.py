from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Create DB if not exists
def init_db():
    conn = sqlite3.connect('moods.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS moods 
                 (id INTEGER PRIMARY KEY, mood TEXT, note TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mood = request.form['mood']
        note = request.form['note']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        conn = sqlite3.connect('moods.db')
        c = conn.cursor()
        c.execute("INSERT INTO moods (mood, note, timestamp) VALUES (?, ?, ?)", (mood, note, timestamp))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        conn = sqlite3.connect('moods.db')
        c = conn.cursor()
        c.execute("SELECT * FROM moods ORDER BY id DESC")
        entries = c.fetchall()
        conn.close()
        return render_template('index.html', entries=entries)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
