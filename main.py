from flask import Flask, g, render_template, make_response, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, send, emit
from threading import Thread
import rethinkdb as r
from rethinkdb import RqlRuntimeError
import json
from datetime import datetime
import argparse

app = Flask(__name__)
socketio = SocketIO(app)
global thread
thread = None

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='secret!',
    DB_HOST='db',
    DB_PORT=28015,
    DB_NAME='chat'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def init_db():
    #conn = r.connect(app.config['DB_HOST'], app.config['DB_PORT'])
    conn = r.connect(host='localhost', port=28015)
    try:
        r.db_create(app.config['DB_NAME']).run(conn)
        r.db(app.config['DB_NAME']).table_create('chats').run(conn)
        r.db(app.config['DB_NAME']).table('chats').index_create('created').run(conn)
        print('Database setup completed. Now run the app without --setup.')
    except RqlRuntimeError:
        print('App database already exists. Run the app without --setup.')
    finally:
        conn.close()

@app.before_request
def before_request():
    try:
        g.db_conn = r.connect(host='localhost', port=28015,db='chat')
    except RqlDriverError:
        abort(503, "No database connection could be established.")

@app.teardown_request
def teardown_request(exception):
    try:
        g.db_conn.close()
    except AttributeError:
        pass

@app.route('/chats/', methods=['POST'])
def create_chat():
    data = json.loads(request.data)
    data['created'] = datetime.now(r.make_timezone('00:00'))
    if data.get('name') and data.get('message'):
        new_chat = r.table("chats").insert([ data ]).run(g.db_conn)
        return make_response('success!', 201)
    return make_response('invalid chat', 401)

@app.route('/', methods=['GET'])
def list_shows():
    chats = list(r.table("chats").order_by(index=r.desc('created')).limit(20).run(g.db_conn))
    return render_template('chats.html', chats=chats)

def watch_chats():
    print('Watching db for new chats!')
    conn = r.connect(host='localhost', port=28015,db='chat')
    feed = r.table("chats").changes().run(conn)
    print('DB Updated!!!')
    for chat in feed:
        chat['new_val']['created'] = str(chat['new_val']['created'])
        socketio.emit('new_chat', chat)


if __name__ == "__main__":
    # Set up rethinkdb changefeeds before starting server
    #https://www.rethinkdb.com/docs/cookbook/javascript/
    #https://stackoverflow.com/questions/30715780/reql-date-and-time-queries
    #https://github.com/rethinkdb/rethinkdb/issues/3740
    #https://github.com/rethinkdb/rethinkdb/issues/6285
    #https://github.com/rethinkdb/rethinkdb/issues/997
    parser = argparse.ArgumentParser(description='Run the Flask todo app')
    parser.add_argument('--setup', dest='run_setup', action='store_true')

    args = parser.parse_args()
    if args.run_setup:
        init_db()
    else:
        if thread is None:
            thread = Thread(target=watch_chats)
            thread.start()
        socketio.run(app, host='0.0.0.0', port=8000)
