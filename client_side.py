import asyncio
import socketio


sio = socketio.AsyncClient()
method_userid = {"Method":"GET", "user_id": 1234}


@sio.event
async def send_message():
    await sio.emit("message_to_rabbitmq", method_userid)


@sio.event
async def message(msg):
    '''Print a message sended into the room by connected client.'''
    print(f'{msg["msg"]} FROM {msg["sid"]}')


@sio.event
async def connect():
    '''Connect and print "connection established" message.'''
    print('connection established')


@sio.event
async def disconnect():
    '''Disconnect message when server disconnect client'''
    print('disconnected from server')


async def main():
    await sio.connect('http://localhost:8080')
    await send_message()
    await sio.wait()


if __name__ == '__main__':
    asyncio.run(main())
