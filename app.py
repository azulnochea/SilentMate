from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    now = datetime.now().strftime('%H:%M')
    return render_template('index.html', time=now)

if __name__ == '__main__':
    app.run(debug=True)

def get_manual_setting():
    conn = sqlite3.connect('db/timetable.db')
    cur = conn.cursor()
    cur.execute("SELECT silent_mode FROM settings WHERE id = 1")
    result = cur.fetchone()
    conn.close()

    if result:
        return bool(result[0])
    return False

def set_manual(value):
    conn = sqlite3.connect('db/timetable.db')
    cur = conn.cursor()
    cur.execute("UPDATE settings SET silent_mode = ? WHERE id = 1", (int(value),))
    conn.commit()
    conn.close()

from flask import request, redirect, url_for

@app.route('/set_manual', methods=['POST'])
def set_manual_route():
    value = request.form.get('silent') == '1'
    set_manual(value)
    return redirect(url_for('home'))
