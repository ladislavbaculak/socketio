import asyncio
import socketio
import time

sio = socketio.AsyncClient()
response_messsage = f'Sending Response {time.time()}!'


@sio.event
async def send_response(response_message):
    '''After connecting to the room client wait x seconds and send
    message to the room.'''
    await sio.emit("getting_response", response_message)


@sio.event
async def message_from_client(msg):
    print(msg)
    # return msg["sid"]


@sio.event
async def connect():
    '''Connect and print "connection established" message to client.'''
    print('connection established')


@sio.event
async def disconnect():
    '''Disconnect message when server disconnect client'''
    print('disconnected from server')


async def main():
    await sio.connect('http://localhost:8080')
    await sio.send_response(response_messsage)
    await sio.wait()


if __name__ == '__main__':    
    asyncio.run(main())