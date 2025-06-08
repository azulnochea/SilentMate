from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)

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

@app.route('/')
def home():
    now = datetime.now().strftime('%H:%M')
    silent = get_manual_setting()
    day = datetime.now().strftime('%A')
    return render_template('index.html', time=now, day=day, silent=silent)


@app.route('/set_manual', methods=['POST'])
def set_manual_route():
    form_date = dict(request.form)
    print("form data:", form_date)

    mode_value = request.form.get('mode')
    print("picked mode:", mode_value)

    if mode_value is None:
        return "You didn't check nothing!", 400

    value = mode_value == 'silent'
    set_manual(value)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

