# pyPANEL & pyCHAT - for pyBOT remote - management

Install [RethinkDB - https://www.rethinkdb.com/docs/install/ ](https://www.rethinkdb.com/docs/install/) and RUN: "rethinkdb --bind all"
=======

For initialize the RethinkDB database: Run before:

python main.py --setup
======================

deps
====

- Flask==0.12.2
- Flask-SocketIO==2.9.2
- greenlet==0.4.12
- rethinkdb==2.3.0.post6


For try with ipython
====================

```python
import rethinkdb as r
from datetime import datetime

conn = r.connect(host='localhost', port=28015, db='chat')

n = 0
new_chat = None
def ins():
    """Insert a new chat"""
    global n
    n = n + 1
    data = {'name':'RethinkDB', 'message':'(%d .-) FROM SERVER' % n, 'created':str(datetime.now(r.make_timezone('00:00')))}
    new_chat = r.table("chats").insert([ data ]).run(conn)

def drop():
    """Delete all chats (truncate)"""
    r.db('chat').table('chats').delete().run(conn)

drop()
ins()
```
