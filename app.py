from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

# 현재 요일, 시간 반환
def get_current_day_time():
    now = datetime.now()
    day = now.strftime('%A')   # 예: Monday
    time = now.strftime('%H:%M')  # 예: 14:30
    return day, time

# 무음 모드 판단
def is_silent_now():
    day, current_time = get_current_day_time()

    if not os.path.exists('db/timetable.db'):
        return False

    conn = sqlite3.connect('db/timetable.db')
    cur = conn.cursor()
    try:
        cur.execute("SELECT start_time, end_time FROM timetable WHERE day = ?", (day,))
        rows = cur.fetchall()
    except Exception as e:
        print("🔥 DB 조회 에러:", e)
        conn.close()
        return False
    conn.close()

    for start, end in rows:
        if start <= current_time <= end:
            return True
    return False

# 홈 화면 (현재 상태 표시)
@app.route('/')
def home():
    silent = is_silent_now()
    return render_template('index.html', silent=silent)

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

        print(f"👉 입력값: {day}, {start}, {end}")

        if not os.path.exists('db'):
            os.makedirs('db')

        conn = sqlite3.connect('db/timetable.db')
        cur = conn.cursor()

        # 테이블이 없으면 생성
        cur.execute('''CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT,
            start_time TEXT,
            end_time TEXT
        )''')

        # 데이터 삽입
        cur.execute("INSERT INTO timetable (day, start_time, end_time) VALUES (?, ?, ?)", (day, start, end))
        conn.commit()
        conn.close()

        print("✅ DB 저장 성공!")
        return redirect('/')
    
    except Exception as e:
        print("🔥 에러 발생:", e)
        return f"<h2>오류 발생: {e}</h2>"

# 앱 실행
if __name__ == '__main__':
    app.run(debug=True)
