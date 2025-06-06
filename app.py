from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime  
import sqlite3  

app = Flask(__name__)  


def get_current_day_time():
    now = datetime.now()  
    day = now.strftime('%A')  
    time = now.strftime('%H:%M')  
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
    return bool(result[0]) if result else False

def set_manual(value):
    conn = sqlite3.connect('db/timetable.db')
    cur = conn.cursor()
    cur.execute("UPDATE settings SET silent_mode = ? WHERE id = 1", (int(value),))
    conn.commit()
    conn.close()

@app.route('/set_manual', methods=['POST'])
def set_manual_route():
    value = request.form.get('silent')
    if value is None:
        print("silent 값이 안 넘어왔어요!") 
        return redirect(url_for('home'))

    set_manual(int(value))
    return redirect(url_for('home'))


@app.route('/toggle')
def toggle_manual():
    current = get_manual_setting()
    set_manual(not current)
    return redirect(url_for('home'))

@app.route('/')
def home():
    silent = is_silent_now()
    manual_silent = get_manual_setting()
    return render_template('index.html', silent=silent, manual=manual_silent)


if __name__ == '__main__':
    app.run(debug=True)
