


from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('wins.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS wins
                  (username TEXT PRIMARY KEY, win_count INTEGER)''')

conn.commit()

@app.route('/wins/<username>', methods=['POST', 'GET'])
def manage_wins(username):
    if request.method == 'POST':
        data = request.get_json()

        if data is None or 'username' not in data:
            return jsonify({'error': 'Invalid data format'}), 400

        cursor.execute('SELECT * FROM wins WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.execute('UPDATE wins SET win_count = win_count + 1 WHERE username = ?', (username,))
        else:
            cursor.execute('INSERT INTO wins (username, win_count) VALUES (?, 1)', (username,))

        conn.commit()
        return jsonify({'message': 'Win added successfully'})

    elif request.method == 'GET':
        cursor.execute('SELECT win_count FROM wins WHERE username = ?', (username,))
        win_count = cursor.fetchone()

        if win_count is None:
            return jsonify({'error': 'Username not found'}), 404

        return jsonify({'username': username, 'win_count': win_count[0]})

if __name__ == '__main__':
    #app.run(debug=True)
    app.run


