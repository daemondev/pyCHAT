import aiohttp_jinja2
import jinja2
from aiohttp import web
import engineio


import aiohttp_debugtoolbar
from aiohttp_debugtoolbar import toolbar_middleware_factory

import rethinkdb as r
from rethinkdb import RqlRuntimeError, RqlDriverError

eio = engineio.AsyncServer()
#app = web.Application()


app = web.Application(middlewares=[toolbar_middleware_factory])
aiohttp_debugtoolbar.setup(app)

eio.attach(app)


#aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('templates'))
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
conn = r.connect(host='localhost', port=28015, db='chat')

@aiohttp_jinja2.template('aiochats.html')
async def index(request):
    """Serve the client-side application."""
    #with open('index.html') as f:
        #return web.Response(text='Hello', content_type='text/html')

    chats = list(r.table("chats").order_by(index=r.desc('created')).limit(20).run(conn))

    #return {'chats':{'name':'Richar','message':'Hello AIOHTTP'}}
    return {'chats': dict(chats)}
    #return dict(chats)


#@eio.on('message')
async def addNewChat(sid, data):
    chatInput = data
    chatInput['created'] = datetime.now(r.make_timezone('00:00'))

    conn = r.connect(host='localhost', port=28015, db='chat')
    new_chat = r.table("chats").insert([ chatInput ]).run(conn)

    chatInput['created'] = str(chatInput['created'])

    await eio.send('ws', chatInput)





async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
    print('websocket connection closed')
    return ws


@eio.on('connect')
def connect(sid, environ):
    print("connect ", sid)

@eio.on('message')
async def message(sid, data):
    print("message ", data)
    await eio.send(sid, data)

import socket
def get_local_ip_addr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

@eio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

#app.router.add_static('/static/', path=str(project_root / 'static'),name='static')

#app.router.add_static('/static', 'static')
app.router.add_static('/static', 'static', name='static')
app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app)
    #web.run_app(app, port=8800)

#http://steelkiwi.com/blog/an-example-of-a-simple-chat-written-in-aiohttp/
#https://github.com/aio-libs/sockjs
#https://www.rethinkdb.com/docs/config-file/
#https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
