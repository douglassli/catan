from socket_server.waiting_room import Room
import socket_server.message_values as mv
import websockets
import random
import json


class CatanServer:
    def __init__(self):
        self.rooms = {}

    async def consumer_handler(self, websocket, path):
        try:
            async for message in websocket:
                await self.consumer(websocket, json.loads(message))
        except websockets.ConnectionClosedError:
            print("Connection Closed:")
            print("    Local addr: {}".format(websocket.local_address))
            print("    Remote addr: {}".format(websocket.remote_address))

    async def consumer(self, websocket, msg):
        print("IN: {}".format(msg))
        if mv.TYPE not in msg or not mv.InTypes.is_member(msg[mv.TYPE]):
            print("Malformed message: {}".format(msg))
            return

        msg_object = mv.InTypes(msg[mv.TYPE]).create_msg_object(msg, websocket)
        await self.handle_message(msg_object)

    async def handle_message(self, msg_obj):
        if not msg_obj.is_valid(self.rooms):
            print("Invalid message: {}".format(msg_obj.msg))
        else:
            room = self.create_room() if msg_obj.msg_type == mv.InTypes.CREATE_ROOM else self.rooms[msg_obj.msg[mv.ROOM_ID]]
            await msg_obj.handler(room)

    def generate_room_id(self):
        room_id = random.randint(100000, 999999)
        while room_id in self.rooms:
            room_id = random.randint(100000, 999999)
        return room_id

    def create_room(self):
        room_id = self.generate_room_id()
        room = Room(room_id)
        self.rooms[room.room_id] = room
        return room
