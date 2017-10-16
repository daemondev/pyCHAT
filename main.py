from flask import Flask, g, render_template, make_response, request, redirect, url_for, jsonify, abort
from flask_socketio import SocketIO, send, emit
from threading import Thread
import rethinkdb as r
from rethinkdb import RqlRuntimeError, RqlDriverError
import json
from datetime import datetime
import argparse

#import eventlet
#eventlet.monkey_patch(socket=True, select=True)
#from eventlet import tpool

app = Flask(__name__)

socketio = SocketIO(app, logger=True, engineio_logger=True)
#socketio = SocketIO(app, logger=True, engineio_logger=True,  ping_timeout=30)

global thread
thread = None

global main_thread
main_thread = None

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

######################################################################################

@socketio.on("add_new_chat")
def addNewChat(data):
    chatInput = data
    chatInput['created'] = datetime.now(r.make_timezone('00:00'))

    conn = r.connect(host='localhost', port=28015, db='chat')
    new_chat = r.table("chats").insert([ chatInput ]).run(conn)

    chatInput['created'] = str(chatInput['created'])

    #chatInput = {'new_val':{'name':'ADMIN', 'message':'FROM SERVER', 'created':str(datetime.now(r.make_timezone('00:00')))}}

    socketio.emit('ws', chatInput)
    #return make_response('success!', 201) ### Not needed

######################################################################################
def watch_chats():
    #while 1:
    #socketio.sleep(1)
    print('Watching db for new chats!')
    conn = r.connect(host='localhost', port=28015,db='chat')
    feed = r.table("chats").changes().run(conn)
    print('##########################\nin BUCLE WHILE\n#####################')
    for chat in feed:
        chat['new_val']['created'] = str(chat['new_val']['created'])
        #global make_response

        socketio.emit('new_chat', chat)
        #return make_response('success!', 201)
######################################################################################

def main_thread_worker():
    print('##########################\nin main thread')
    while 1:
        print('##########################\nin BUCLE WHILE\n#####################')
        socketio.sleep(1)
        #the following emit works fine

        conn = r.connect(host='localhost', port=28015,db='chat')
        feed = r.table("chats").changes().run(conn)
        print('DB Updated!!!')
        for chat in feed:
            chat['new_val']['created'] = str(chat['new_val']['created'])
            socketio.emit('new_chat', chat)
            #return make_response('success!', 201)

if __name__ == "__main__":
    #https://github.com/miguelgrinberg/python-socketio/issues/16
    #https://github.com/miguelgrinberg/Flask-SocketIO/issues/462
    #https://flask-socketio.readthedocs.io/en/latest/#flask_socketio.SocketIO.emit
    #https://github.com/miguelgrinberg/Flask-SocketIO/issues/117
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
        """
        if thread is None:
            thread = Thread(target=watch_chats)
            thread.setDaemon(True)
            thread.start() #"""

        #"""
        #if main_thread is None:
        #main_thread = socketio.start_background_task(target=watch_chats)
            #main_thread = socketio.start_background_task(target=main_thread_worker) #"""

        socketio.run(app, host='0.0.0.0', port=8000, debug=True)

"""
import rethinkdb as r
from datetime import datetime

conn = r.connect(host='localhost', port=28015,db='chat')
r.db('chat').table('chats').delete().run(conn)

n = 0
new_chat = None
def ins():
    global n
    n = n + 1
    data = {'name':'ADMIN', 'message':'m(%d) - FROM SERVER' % n++, 'created':str(datetime.now(r.make_timezone('00:00')))}
    new_chat = r.table("chats").insert([ data ]).run(conn)

def el():
    r.db('chat').table('chats').delete().run(conn)
"""

"""
def listen():
    while True:
        watch_chats()
        eventlet.sleep(5)

eventlet.spawn(watch_chats) ###"""
#eventlet.spawn(listen) ###"""
