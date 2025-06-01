from flask import Flask, render_template, redirect
from datetime import datetime  
import sqlite3
import os

MANUAL_FILE = 'manual_silent.txt'

def load_manual_state():
    if os.path.exists(MANUAL_FILE):
        with open(MANUAL_FILE, 'r') as f:
            return f.read().strip() == '1'
    return False

def save_manual_state(state: bool):
    with open(MANUAL_FILE, 'w') as f:
        f.write('1' if state else '0')

app = Flask(__name__) 

manual_silent = load_manual_state()

@app.route('/')
def home():
    silent = is_silent_now()  
    return render_template('index.html', silent=silent, manual=manual_silent) 

def get_current_day_time():
    now = datetime.now()  
    day = now.strftime('%A')  
    time = now.strftime('%H:%M')  
    return day, time


def is_silent_now():
    global manual_silent

    if manual_silent:
        return True
    
    day, current_time = get_current_day_time()  

    conn = sqlite3.connect('db/timetable.db')
    cur = conn.cursor()
    cur.execute("SELECT start_time, end_time FROM timetable WHERE day = ?", (day,)) #오늘 수업의 시작/종료 시간을 가져옴
    rows = cur.fetchall()  
    conn.close()

    for start, end in rows:
        if start <= current_time <= end:
            return True  
    return False  

@app.route('/toggle')
def toggle_manual():
    global manual_silent
    manual_silent = not manual_silent
    save_manual_state(manual_silent)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)