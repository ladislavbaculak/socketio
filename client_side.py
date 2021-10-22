import asyncio
from logging import exception
import socketio
import random

sio = socketio.AsyncClient()
method_userid = {"Method":"GET",
                 "user_id": 1234,
                 "data": {},
                }


@sio.event
async def send_message():
    '''Emit message to the rabbitmq with the request'''
    await sio.emit("message_to_rabbitmq", method_userid)


@sio.event
async def message(msg):
    '''Print a message sended back from rabbitMQ.'''
    print(msg)


@sio.event
async def connect():
    '''Connect and print "connection established" message.'''
    print('Connection Established')


@sio.event
async def disconnect():
    '''Disconnect and print "disconnected from server" message.'''
    print('disconnected from server')


async def main():
    await sio.connect('http://localhost:8080')
    while True:
        try:
            await send_message()
            await sio.sleep(random.randint(1,3))
        except KeyboardInterrupt:
            print('Disconnect!')    
            break
    await sio.wait()


if __name__ == '__main__':
    asyncio.run(main())
