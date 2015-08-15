# all the imports
import sqlite3
import json
from contextlib import closing

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'

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
    if session.get('logged_in'):
        cur = g.db.execute('select text from entries where username="{0}" order by id desc'.format(session.get('username')))
        entries = [dict(text=entry[0]) for entry in cur.fetchall()]
        return render_template('index.html', entries=entries, username=session.get('username'))
    else:
        return render_template('index.html')
        
@app.route('/api/notes', methods=['GET'])
def get_notes():
    if session.get('logged_in'):
        cur = g.db.execute('select text from entries where username="{0}" order by id desc'.format(session.get('username')))
        return json.dumps(cur.fetchall())
    
@app.route('/api/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (username, text) values (?, ?)', 
                    [session.get('username'), request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return 'OK'
    
@app.route('/api/dump', methods=['POST'])
def dump_data():
    if request.method == 'POST' and session.get('logged_in'):
        pass
    
    
@app.route('/api/login', methods=['POST'])
def login():
    error = None
    if request.method == 'POST':
        cur = g.db.execute('SELECT EXISTS(SELECT 1 FROM users WHERE username="{0}" LIMIT 1)'.format(request.json['username']))
        if cur.fetchall()[0][0] == 1:
            cur = g.db.execute('select text from entries where username="{0}" order by id desc'.format(request.json['username']))
            result = {'result': 'EXISTS'}
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
            result = {'result': 'NEW'}
            return jsonify(result)

@app.route('/api/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)