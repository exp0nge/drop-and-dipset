# all the imports
import sqlite3
import json
from contextlib import closing

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = '309cd3800aacbd003ac36199fa537295'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
    
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()    

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        
@app.route('/')
def index():
    if request.cookies.get('session'):
        session['logged_in'] = True
    if session.get('logged_in'):
        cur = g.db.execute('select text from entries where username="{0}" order by id desc'.format(session.get('username')))
        entries = [dict(text=entry[0]) for entry in cur.fetchall()]
        return render_template('index.html', entries=entries)
    else:
        return render_template('index.html')
        
@app.route('/api/notes', methods=['GET'])
def get_notes():
    if session.get('logged_in'):
        cur = g.db.execute('select text, date, id from entries where username="{0}" order by id desc'.format(session.get('username')))
        return json.dumps(cur.fetchall())
    else:
        abort(401)
    
@app.route('/api/add', methods=['POST'])
def add_note():
    if not session.get('logged_in'):
        abort(401)
    else:
        g.db.execute('insert into entries (username, text, date) values (?, ?, ?)', 
            [session.get('username'), request.json['content'], request.json['date']])
        g.db.commit()
        flash('New entry was successfully posted')
        return jsonify({'status': 'OK'})

@app.route('/api/delete/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    if not session.get('logged_in'):
        abort(401)
    else:
        print note_id
        g.db.execute('DELETE FROM entries WHERE id="{0}"'.format(note_id))
        g.db.commit()
        return jsonify({'status': 'OK'})

@app.route('/api/login', methods=['POST'])
def login():
    error = None
    if request.method == 'POST':
        cur = g.db.execute('SELECT EXISTS(SELECT 1 FROM users WHERE username="{0}" LIMIT 1)'.format(request.json['username']))
        if cur.fetchall()[0][0] == 1:
            cur = g.db.execute('select text from entries where username="{0}" order by id desc'.format(request.json['username']))
            result = {'result': 'EXISTS', 'username': request.json['username']}
            result['data'] = [entry[0] for entry in cur.fetchall()]
            session['entries'] = result['data']
            session['logged_in'] = True
            session['username'] = request.json['username']
            flash('Log successfully')
            return jsonify(result)
        else:
            g.db.execute('insert into users (username) values (?)', [request.json['username']])
            g.db.commit()
            session['logged_in'] = True
            session['username'] = request.json['username']
            flash('new {0} user created!'.format(session['username']))
            result = {'result': 'NEW', 'username': request.json['username']}
            return jsonify(result)

@app.route('/api/logout')
def logout():
    session.clear()
    return 'LOGGED_OUT'
    
@app.route('/api/logstatus', methods=['GET'])
def log_status():
    if session.get('logged_in'):
        return jsonify({
            'status': 'TRUE', 
            'username': session.get('username')})
    else:
        return jsonify({'status': 'FALSE'})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)