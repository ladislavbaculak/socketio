from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
a_count = 0
b_count = 0


async def index(request):
    """Serve the client-side application."""
    with open('static/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.event
async def connect(sid, environ):
    '''When client connects, print his SID. If client name in header don\'t
    match, requested by server, disconnect the client.'''
    username = environ.get('HTTP_USERNAME')
    print(sid, 'Connected Under:', username)
    async with sio.session(sid) as session:
        session['Username'] = username
    if username != '123':
        print(sid, 'Disconnected, Username:', username)
        return False


async def rooms_disconnecting(sid):
    '''When client is disconnected, room counter is decremented
    and message with actual count emited to particular room.'''
    global a_count
    global b_count
    room = (sio.rooms(sid))
    if 'A' in room:
        a_count -= 1
        await sio.emit('room_count', {'count': a_count, 'room': 'A'}, to='A')
    elif 'B' in room:
        b_count -= 1
        await sio.emit('room_count', {'count': b_count, 'room': 'B'}, to='B')


@sio.event
async def disconnect(sid):
    '''When client disconnect, print his SID.'''
    await rooms_disconnecting(sid)
    async with sio.session(sid) as session:
        print(sid, 'Disconnected, Username:', session['Username'])
    await sio.disconnect(sid)


@sio.event
async def message(sid, message):
    '''Message send to the room by client.'''
    await sio.emit('message', {'msg': message, 'sid': sid},  to='A')


@sio.event
async def rooms(sid, data):
    '''When a client connects to the server and selects the room the server
    adds that client into a selected room and, sends back the client
    confirmation message then increases the number of connections.
    The actual count of connections is emitted to the particular room.
    '''
    global a_count
    global b_count
    if data['room'] == 'A':
        sio.enter_room(sid, 'A')
        await sio.emit('status_room', {'status': 'You Are Connected To: A Room.'}, to=sid)
        a_count += 1
        await sio.emit('room_count', {'count': a_count, 'room': 'A'}, to='A')
    elif data['room'] == 'B':
        sio.enter_room(sid, 'B')
        await sio.emit('status_room', {'status': 'You Are Connected To: B Room.'}, to=sid)
        b_count += 1
        await sio.emit('room_count', {'count': b_count, 'room': 'B'}, to='B')


app.router.add_static('/static', 'static')
app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app)
