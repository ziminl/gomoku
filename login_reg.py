


from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__, template_folder='templates')

conn = sqlite3.connect('wins.db', check_same_thread=False)
cursor = conn.cursor()

#read(final.sql
#fsql = open("final.sql", "r")
#adadad = (fsql.read())
#cursor.execute('''+adadad+''')

cursor.execute('''CREATE TABLE IF NOT EXISTS wins
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  win_count INTEGER)''')

conn.commit()


@app.route('/register/<username>/<password>', methods=['POST'])
    data = request.get_json()
    cursor.execute('SELECT * FROM wins WHERE username = ?', (username,))
    existing_user = cursor.fetchone()

    if existing_user: #if there is in db -> no
        return "The account is already in"
        return jsonify({'message': 'The account is already in'})
    else:
        # Insert the new user into the database
        cursor.execute('INSERT INTO wins (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        #return "Account registered successfully"
        return jsonify({'message': 'Account added successfully'})



@app.route('/login/<username>/<password>', methods=['POST'])
#if there is in db -> ok
#if there isnt in db -> error (didnt register or wrong input)
def login(username, password):
    data = request.get_json()
    cursor.execute('SELECT * FROM wins WHERE username = ?', (username,))
    user = cursor.fetchone()
    if user:
        stored_password_hash = user['password']
        if (password == password#tlqkf):
            return "Login successful"
        else:
            return "Password is incorrect"
    else:
        return "Username not found"

@app.route('/wins/<username>', methods=['POST', 'GET'])
def manage_wins(username):
    if request.method == 'POST':
        data = request.get_json()

        cursor.execute('SELECT * FROM wins WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.execute('UPDATE wins SET win_count = win_count + 1 WHERE username = ?', (username,))
        else: #need to return error'
            #delete this one.
            #cursor.execute('INSERT INTO wins (username, win_count) VALUES (?, 1)', (username,))

        conn.commit()

        return jsonify({'message': 'Win added successfully'})

    elif request.method == 'GET':
        cursor.execute('SELECT win_count FROM wins WHERE username = ?', (username,))
        win_count = cursor.fetchone()

        if win_count is None:
            return jsonify({'error': 'Username not found'}), 404

        return jsonify({'username': username, 'win_count': win_count[0]})

@app.route('/', methods=['GET'])
def main_page():
    cursor.execute('SELECT username, win_count FROM wins ORDER BY win_count DESC')
    all_wins = cursor.fetchall()

    return render_template('main_page.html', wins=all_wins)

if __name__ == '__main__':
    app.run(debug=True)
