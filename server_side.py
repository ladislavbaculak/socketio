from aiohttp import web
import socketio
import time

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
response_messsage = f'Sending Response {time.time()}!'


@sio.event
async def connect(sid, environ):
    '''Connect and print "connection established" message.'''
    print('Connection Established', sid)


@sio.event
async def disconnect(sid):
    '''Disconnect and print "disconnected from server" message.'''
    print('disconnected from server', sid)


@sio.event
async def message_to_rabbitmq(sid, message):
    '''Message that was send from client is printed and response 
    message is send back to the client and recognized by sid.
    '''
    print(sid, message)
    await sio.send(response_messsage, to=sid)


if __name__ == '__main__':
    web.run_app(app)
