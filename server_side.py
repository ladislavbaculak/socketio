from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


@sio.event
async def connect(sid, environ):
    '''Connected and print connected message'''
    print(sid, 'Connected')


@sio.event
async def disconnect(sid):
    '''Unconnect and print unconnected message'''
    await sio.disconnect(sid)


@sio.event
async def message_to_rabbitmq(sid, message):
    await sio.emit('message_from_client', {'msg': message, 'sid': sid})


if __name__ == '__main__':
    web.run_app(app)
