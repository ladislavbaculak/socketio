from aiohttp import web
import socketio
import time

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
response_messsage = f'Sending Response {time.time()}!'


@sio.event
async def connect(sid, environ):
    '''Connected and print connected message'''
    print(sid, 'Connected')


@sio.event
async def disconnect(sid):
    '''Unconnect and print unconnected message'''
    print(sid, 'Connected')


@sio.event
async def message_to_rabbitmq(sid, message):
    print(sid, message)
    await sio.send(response_messsage, to=sid)


if __name__ == '__main__':
    web.run_app(app)
