from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    silent = is_silent_now()
    manual = get_manual_setting()
    return render_template('index.html', silent=silent, manual=manual)

def get_current_day_time():
    now = datetime.now()
    day = now.strftime('%A')       # 예: Monday
    time = now.strftime('%H:%M')   # 예: 13:45
    return day, time

def is_silent_now():
    day, current_time = get_current_day_time()

    conn = sqlite3.connect('db/timetable.db')
    cur = conn.cursor()
    cur.execute("SELECT start_time, end_time FROM timetable WHERE day = ?", (day,))
    rows = cur.fetchall()
    conn.close()

    for start, end in rows:
        if start <= current_time <= end:
            return True
    return False

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

@app.route('/set_manual', methods=['POST'])
def set_manual_route():
    value = request.form.get('silent') == '1'
    set_manual(value)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
