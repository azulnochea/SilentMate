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