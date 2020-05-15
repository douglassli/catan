from server_controller.waiting_room import Room
from server_controller.message_values import InTypes, FieldNames
import random
import json


class CatanServer:
    def __init__(self):
        self.games = {}
        self.client_ids = set()
        self.rooms = {}

    async def consumer_handler(self, websocket, path):
        async for message in websocket:
            await self.consumer(websocket, json.loads(message))

    async def consumer(self, websocket, msg):
        if FieldNames.TYPE not in msg or not InTypes.is_member(msg[FieldNames.TYPE]):
            print("Malformed message: {}".format(msg))
            return

        msg_object = InTypes(msg[FieldNames.TYPE]).create_msg_object(msg, websocket)
        await self.handle_message(msg_object)

    async def handle_message(self, msg_obj):
        if not msg_obj.is_valid(self.rooms):
            print("Invalid message: {}".format(msg_obj.msg))
        else:
            room = self.create_room() if msg_obj.msg_type == InTypes.CREATE_ROOM else self.rooms[msg_obj.msg[FieldNames.ROOM_ID]]
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
