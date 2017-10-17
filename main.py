from flask import Flask, g, render_template, make_response, request, redirect, url_for, jsonify, abort, Response
from flask_socketio import SocketIO, send, emit
from threading import Thread
import rethinkdb as r
from rethinkdb import RqlRuntimeError, RqlDriverError
import json
from datetime import datetime
import argparse
from functools import wraps
#from flask_sslify import SSLify

from OpenSSL import SSL
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('key.pem')
context.use_certificate_file('cert.pem')


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated




app = Flask(__name__)
#sslify = SSLify(app)
socketio = SocketIO(app)
global thread
thread = None

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='apeponkopy!',
    DB_HOST='db',
    DB_PORT=28015,
    DB_NAME='chat'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def init_db():
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

@app.route('/secret-page')
@requires_auth
def secret_page():
    return render_template('admin.html')

@app.before_request
def before_request():
    try:
        g.db_conn = r.connect(host='localhost', port=28015, db='chat')
    except RqlDriverError:
        abort(503, "No database connection could be established. Try: python main.py --setup in CLI")

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
    print('\n#################################\n###>>> Watching db for new chats!\n#################################\n\n')
    conn = r.connect(host='localhost', port=28015, db='chat')
    feed = r.table("chats").changes().run(conn)
    for chat in feed:
        chat['new_val']['created'] = str(chat['new_val']['created'])
        socketio.emit('new_chat', chat)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='pyCHAT')
    parser.add_argument('--setup', dest='run_setup', action='store_true')

    args = parser.parse_args()

    if args.run_setup:
        init_db()
    else:
        #"""
        if thread is None:
            thread = Thread(target=watch_chats)
            thread.start() #"""
        #CERT_FILE = "cert2.pem"
        #KEY_FILE = "key2.pem"
        #context(CERT_FILE, KEY_FILE,)
        #socketio.run(app, host='0.0.0.0', port=8000, ssl_context='adhoc')
        socketio.run(app, host='0.0.0.0', port=8000)
        #socketio.run(app, host='0.0.0.0', port=8000, ssl_context=context)

        #from cert_creator import *
        #socketio.run(app, certfile=CERT_FILE, keyfile=KEY_FILE, port=8000)

#http://eventlet.net/doc/modules/wsgi.html#ssl
