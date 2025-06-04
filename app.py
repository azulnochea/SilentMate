feature/schedule-ui
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
from flask import Flask, render_template  # flask 웹서버, 템플릿 사용
from datetime import datetime  # 현재시간/날짜 모듈
import sqlite3  # SQLite 데베를 사용

app = Flask(__name__)  # Flask 앱 생성

# 홈페이지 라우터
@app.route('/')
def home():
    silent = is_silent_now()  # 수업 중인지 판단
    print("현재 silent 상태:", silent)
    return render_template('index.html', silent=silent)  # 템플릿 전달, 화면에 표시

# 현재 요일과 시간 가져오는 함수
def get_current_day_time():
    now = datetime.now()  # 현재시간
    day = now.strftime('%A')  # 예: Monday
    time = now.strftime('%H:%M')  # 예: 12:00
    return day, time


#수업시간인지 판단하는 함수
def is_silent_now():
    day, current_time = get_current_day_time()  # 현재 요일과 시간

    conn = sqlite3.connect('db/timetable.db')
    cur = conn.cursor()
    cur.execute("SELECT start_time, end_time FROM timetable WHERE day = ?", (day,)) #오늘 수업의 시작/종료 시간을 가져옴
    rows = cur.fetchall()  #결과 전부 불러와 리스트 저장
    conn.close()

    # rows에 있는 각 수업 시간마다 비교
    for start, end in rows:
        if start <= current_time <= end:
            return True  # 수업중 -> 무음모드
    return False  # 수업중 아님 -> 벨소리 가능

# 앱 실행
if __name__ == '__main__':
    app.run(debug=True)
 main
