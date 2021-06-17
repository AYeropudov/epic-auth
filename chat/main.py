from aiohttp import web
import socketio

from rooms import ChatNamespace, CombatNamespace
import pydevd_pycharm


sio = socketio.AsyncServer()
sio.register_namespace(ChatNamespace('/chat'))
sio.register_namespace(CombatNamespace('/battle'))

app = web.Application()
sio.attach(app)


@sio.event
def connect(sid):
    print("connect ", sid)

@sio.event
async def chat_message(sid, data):
    print("message ", data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    pydevd_pycharm.settrace('192.168.255.1', port=37259, stdoutToServer=True, stderrToServer=True)
    web.run_app(app, port=5678)
