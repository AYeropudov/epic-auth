import json
import time

import socketio
import requests
from .redis_client import r


class ChatNamespace(socketio.AsyncNamespace):

    def on_connect(self, sid, environ):
        print('Connected to chat room ', sid)
        pass

    def on_disconnect(self, sid):
        user = r.get(sid)
        user = json.loads(user)
        r.delete(user.get('username'))
        r.delete(sid)
        print('Diconnected from chat room ', sid)
        pass

    def on_my_event(self, sid, data):
        self.emit('my_response', data)

    def on_sign_in(self, sid, data):
        current_user = r.get(sid)
        if current_user is None:
            auth = requests.get('http://flaskapp:5000/api/me', headers={'auth': data.get('auth')})
            user = auth.json()
            r.set(sid, json.dumps(user))
            r.set(user.get('username'), sid)

    async def on_message(self, sid, data):
        current_user = r.get(sid)
        user = json.loads(current_user)
        await self.emit('message', {"id": time.time_ns(), "from": [user.get("username")], "to": data.get("to"), "message": data.get("message")})
