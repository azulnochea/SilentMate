from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import sqlite3
import os

app = Flask(__name__)

# DB 경로
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'timetable.db')

# 현재 요일, 시간 반환
def get_current_day_time():
    now = datetime.utcnow() + timedelta(hours=9)
    day = now.strftime('%A')
    time = now.strftime('%H:%M')
    return day, time

# 무음 모드 판단
def is_silent_now():
    day, current_time = get_current_day_time()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("SELECT start_time, end_time FROM timetable WHERE day = ?", (day,))
        rows = cur.fetchall()
    except sqlite3.OperationalError:
        rows = []
    conn.close()

    for start, end in rows:
        if start <= current_time <= end:
            return True
    return False

# 수동 무음 설정 읽기
def get_manual_setting():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT silent_mode FROM settings WHERE id = 1")
    result = cur.fetchone()
    conn.close()
    return bool(result[0]) if result else False

# 수동 무음 설정 저장
def set_manual(value):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE settings SET silent_mode = ? WHERE id = 1", (int(value),))
    conn.commit()
    conn.close()

# 홈 화면
@app.route('/')
def home():
    silent = is_silent_now()
    manual = get_manual_setting()
    auto_silent_active = silent

    final_silent = manual or silent

    return render_template('index.html',
                            silent=final_silent,
                            manual=manual,
                            auto_silent_active=auto_silent_active) 

   
@app.route('/toggle')
def toggle_manual():
    current = get_manual_setting()
    set_manual(not current)
    return redirect(url_for('home'))

# 수동 설정 라디오버튼 처리
@app.route('/set_manual', methods=['POST'])
def set_manual_route():
    value = request.form.get('silent')
    if value is None:
        return redirect(url_for('home'))
    set_manual(int(value))
    return redirect(url_for('home'))

# 시간표 입력 폼 페이지
@app.route('/add')
def add_schedule():
    return render_template('add.html')

# 시간표 입력 처리
@app.route('/submit', methods=['POST'])
def submit_schedule():
    try:
        day = request.form['day']
        start = request.form['start_time']
        end = request.form['end_time']

        if not os.path.exists('db'):
            os.makedirs('db')

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # 테이블 생성 (없는 경우만)
        cur.execute('''CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT,
            start_time TEXT,
            end_time TEXT
        )''')

        cur.execute("INSERT INTO timetable (day, start_time, end_time) VALUES (?, ?, ?)", (day, start, end))
        conn.commit()
        conn.close()

        return redirect('/success')
    
    except Exception as e:
        return f"<h2>오류 발생: {e}</h2>"

# 등록 성공 페이지
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

