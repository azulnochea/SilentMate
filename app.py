from flask import Flask, render_template
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

# DB 파일 경로
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'timetable.db')

@app.route('/')
def home():
    silent = is_silent_now()
    return render_template('index.html', silent=silent)

def get_current_day_time():
    now = datetime.now()
    day = now.strftime('%A')       # 예: Monday
    time = now.strftime('%H:%M')   # 예: 13:45
    return day, time

def is_silent_now():
    day, current_time = get_current_day_time()

    # DB 연결
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # timetable 테이블이 없는 경우 예외처리
    try:
        cur.execute("SELECT start_time, end_time FROM timetable WHERE day = ?", (day,))
        rows = cur.fetchall()
    except sqlite3.OperationalError:
        rows = []

    conn.close()

    # 현재 시간 확인
    for start, end in rows:
        if start <= current_time <= end:
            return True
    return False

if __name__ == '__main__':
    app.run(debug=True)
