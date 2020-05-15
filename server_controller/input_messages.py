import server_controller.catan_server as cs


class InputMessage:
    def __init__(self, msg, websocket):
        self.msg = msg
        self.websocket = websocket

    def is_valid(self, rooms):
        room_id = self.msg[cs.ROOM_ID]
        plyr_id = self.msg[cs.PLAYER_ID]
        return room_id in rooms and rooms[room_id].has_plyr_id(plyr_id)

    async def handle_message(self, rooms):
        if not self.is_valid(rooms):
            print("Invalid message: {}".format(self.msg))
        else:
            await self.handler(rooms[self.msg[cs.ROOM_ID]] if cs.ROOM_ID in self.msg else None)

    async def handler(self, room):
        pass


class CreateRoomMsg(InputMessage):
    def __init__(self, msg, websocket, room_generator):
        super().__init__(msg, websocket)
        self.generate_room = room_generator

    def is_valid(self, rooms):
        return self.msg[cs.NAME].isalnum()

    async def handler(self, room):
        await self.generate_room().add_player(self.websocket, self.msg[cs.NAME])


class JoinRoomMsg(InputMessage):
    def is_valid(self, rooms):
        room_id = self.msg[cs.ROOM_ID]
        name = self.msg[cs.NAME]
        return room_id in rooms and name.isalnum() and rooms[room_id].is_name_available(name)

    async def handler(self, room):
        await room.add_player(self.websocket, self.msg[cs.NAME])


class ReadyMsg(InputMessage):
    async def handler(self, room):
        await room.mark_ready(self.msg[cs.PLAYER_ID])


class StartGameMsg(InputMessage):
    def is_valid(self, rooms):
        return super().is_valid(rooms) and rooms[self.msg[cs.ROOM_ID]].is_room_ready()

    async def handler(self, room):
        await room.start_game()


class StartSettleSelectMsg(InputMessage):
    async def handler(self, room):
        await room.start_settle_select(self.msg[cs.PLAYER_ID])


class StartRoadSelectMsg(InputMessage):
    async def handler(self, room):
        await room.start_road_select(self.msg[cs.PLAYER_ID])


class SettleBuiltMsg(InputMessage):
    async def handler(self, room):
        await room.settle_built(self.msg[cs.PLAYER_ID], self.msg[cs.ROW], self.msg[cs.COL])


class RoadBuiltMsg(InputMessage):
    async def handler(self, room):
        await room.road_built(self.msg[cs.PLAYER_ID], self.msg[cs.ROW], self.msg[cs.COL])


class EndTurnMsg(InputMessage):
    async def handler(self, room):
        await room.end_turn(self.msg[cs.PLAYER_ID])