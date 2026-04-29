from flask import Flask, render_template, request, redirect, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = 'secretkey'

# ---------- DATABASE SETUP ----------
def get_db():
    return sqlite3.connect('evoting.db')

def init_db():
    if not os.path.exists('evoting.db'):
        conn = get_db()
        cur = conn.cursor()

        # Voters Table
        cur.execute('''CREATE TABLE voters (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT UNIQUE,
                        password TEXT,
                        has_voted INTEGER DEFAULT 0,
                        is_admin INTEGER DEFAULT 0
                    )''')

        # Candidates Table
        cur.execute('''CREATE TABLE candidates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        votes INTEGER DEFAULT 0
                    )''')

        # Add Admin
        cur.execute("INSERT INTO voters (name, email, password, is_admin) VALUES (?, ?, ?, ?)",
                    ('Admin', 'admin@gmail.com', 'admin123', 1))

        # Add Normal Users
        users = [
            ('Dheekshith', 'dheekshith@gmail.com', 'dheekshith1234'),
            ('Bharat', 'bharat@gmail.com', 'bharat1234'),
            ('Ashok', 'ashok@gmail.com', 'ashok1234'),
            ('Lohit', 'lohit@gmail.com', 'lohit1234')
        ]
        cur.executemany("INSERT INTO voters (name, email, password) VALUES (?, ?, ?)", users)

        # Add Candidates
        candidates = [('Candidate A',), ('Candidate B',), ('Candidate C',)]
        cur.executemany("INSERT INTO candidates (name) VALUES (?)", candidates)

        conn.commit()
        conn.close()

init_db()


# ---------- ROUTES ----------
@app.route('/')
def home():
    return redirect('/login')


# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, password, has_voted, is_admin FROM voters WHERE email = ? AND password = ?", (email, password))
        voter = cur.fetchone()
        conn.close()

        if voter:
            session['voter_id'] = voter[0]
            session['email'] = voter[2]
            session['name'] = voter[1]
            session['is_admin'] = voter[5]

            if voter[5] == 1:
                return redirect('/results')
            else:
                return redirect('/vote')
        else:
            message = "Invalid email or password!"

    return render_template('login.html', message=message)


# ---------- VOTING ----------
@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'email' not in session:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT has_voted FROM voters WHERE email = ?", (session['email'],))
    has_voted = cur.fetchone()[0]

    # If already voted
    if has_voted:
        conn.close()
        return render_template('vote.html', already_voted=True)

    # Handle vote submission
    if request.method == 'POST':
        candidate_name = request.form.get('candidate')
        if candidate_name:
            # Update candidate vote count
            cur.execute("UPDATE candidates SET votes = votes + 1 WHERE name = ?", (candidate_name,))
            # Mark voter as voted
            cur.execute("UPDATE voters SET has_voted = 1 WHERE email = ?", (session['email'],))
            conn.commit()
            conn.close()
            return render_template('vote.html', success=True, message="Your vote has been recorded successfully!")

    conn.close()
    return render_template('vote.html')


# ---------- RESULTS (ADMIN) ----------
@app.route('/results')
def results():
    if 'email' not in session or session.get('is_admin') != 1:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT name, votes FROM candidates")
    data = cur.fetchall()
    conn.close()

    labels = [row[0] for row in data]
    votes = [row[1] for row in data]

    return render_template('results.html', labels=labels, votes=votes)


# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
