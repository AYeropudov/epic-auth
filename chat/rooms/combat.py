import datetime
import json
import time
from uuid import uuid4
import socketio
import requests
from clickhouse_driver import Client
from .redis_client import r

clientCH = Client.from_url('clickhouse://default:passwordHash@clickhouse-server:9000/default')


class CombatNamespace(socketio.AsyncNamespace):

    def on_connect(self, sid, environ):

        print('Connected to battle room ', sid)
        pass

    def on_disconnect(self, sid):
        user = r.get(sid)
        user = json.loads(user)
        r.delete(user.get('username'))
        r.delete(sid)
        print('Diconnected from chat room ', sid)
        pass

    async def on_battle(self, sid, data):
        current_user = r.get(sid)
        user = json.loads(current_user)
        query_id = str(uuid4())
        UUID = clientCH.execute('SELECT generateUUIDv4()')
        UUID = UUID[0][0].__str__()
        clientCH.execute(
            'INSERT INTO combats_tbl(ID, user_id, combatants, created_at) VALUES', [{
                "ID": UUID,
                "user_id": user.get('id'),
                "combatants": [user.get('id')],
                "created_at": datetime.datetime.now()}
            ],
            query_id=query_id)
        self.enter_room(sid, "cmb_{}".format(UUID))
        await self.emit('message', {"room": "cmb_{}".format(UUID)})

    def on_sign_in(self, sid, data):
        current_user = r.get(sid)
        if current_user is None:
            auth = requests.get('http://flaskapp:5000/api/me', headers={'auth': data.get('auth')})
            user = auth.json()
            r.set(sid, json.dumps(user))
            r.set(user.get('username'), sid)
            current_user = user

        # self.enter_room(sid, "cmb_{}".format(query_id))

    async def on_message(self, sid, data):
        current_user = r.get(sid)
        user = json.loads(current_user)
        await self.emit('message', {"id": time.time_ns(), "from": [user.get("username")], "to": data.get("to"), "message": data.get("message")})
