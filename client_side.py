import asyncio
import socketio
import random
import sys

sio = socketio.AsyncClient()
f_messsage = 'Hello There!'


def room_select():
    '''When client connect, client select the room to connect.'''
    room = str()
    while room != 'A' or room != 'B':
        room = (input('What Room You Want To Enter? 1.)A 2.)B: ')).upper()
        if room == 'A' or room == 'B':
            break
    return room


@sio.event
async def send_message():
    '''After connecting to the room client wait x seconds and send
    message to the room.'''
    await sio.sleep(random.randint(1, 10))
    await sio.send(f_messsage)


@sio.event
async def message(msg):
    '''Print a message sended into the room by connected client.'''
    print(f'{msg["msg"]} FROM {msg["sid"]}')


@sio.event
async def connect():
    '''Connect to the selected room and print "connection established" message
    to client.'''
    print('connection established')
    await sio.emit('rooms', {'room': room_select()})


@sio.event
async def disconnect():
    '''Disconnect message when server disconnect client'''
    print('disconnected from server')


@sio.event
async def status_room(status):
    '''Print a message "You are connected to: X room" '''
    print(status['status'])


@sio.event
async def room_count(count):
    '''Print number of clients connected to a room.'''
    print(f"{count['count']} Client(s) Connected to: {count['room']} ")


async def main(username):
    await sio.connect('http://localhost:8080', headers={'Username': username})
    await send_message()
    await sio.wait()


if __name__ == '__main__':
    try:
        asyncio.run(main(str(sys.argv[1] if len(sys.argv) > 1 else None)))
    except Exception:
        print('Disconnected')
